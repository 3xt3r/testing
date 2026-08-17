#!/usr/bin/env python3
import argparse, csv, fnmatch, html, json, os, re, shutil, subprocess
from collections import defaultdict
from pathlib import Path

TEXT_EXTS = {
    ".c",".cc",".cpp",".cxx",".h",".hh",".hpp",".hxx",".rs",".go",".py",
    ".java",".kt",".js",".ts",".cmake",".txt",".conf",".cfg",".ini",".yaml",
    ".yml",".json",".xml",".proto",".rules",".rule",".pac",".spicy"
}
SOURCE_PATH_RE = re.compile(
    r'(?:(?:/[A-Za-z0-9_.+@:-]+)+|(?:[A-Za-z]:\\(?:[^\\\x00\r\n]+\\)*[^\\\x00\r\n]+))'
    r'\.(?:cpp|cxx|cc|hpp|hxx|hh|spicy|proto|java|c|h|rs|go|py|kt|js|ts|pac)',
    re.I
)

def run_tool(args):
    try:
        p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                           text=True, errors="replace", timeout=60)
        return p.stdout if p.returncode == 0 else ""
    except Exception:
        return ""

def is_elf(path):
    try:
        with open(path, "rb") as f:
            return f.read(4) == b"\x7fELF"
    except Exception:
        return False

def is_probably_text(path):
    if path.suffix.lower() in TEXT_EXTS:
        return True
    try:
        with open(path, "rb") as f:
            data = f.read(4096)
        if not data:
            return False
        if b"\x00" in data:
            return False
        printable = sum((32 <= b < 127) or b in (9,10,13) for b in data)
        return printable / len(data) > 0.85
    except Exception:
        return False

def python_strings(path, min_len=4):
    items=[]
    try:
        data=path.read_bytes()
    except Exception:
        return items
    start=None
    for i,b in enumerate(data):
        if 32 <= b <= 126:
            if start is None: start=i
        else:
            if start is not None and i-start >= min_len:
                items.append((start, data[start:i].decode("ascii","ignore")))
            start=None
    if start is not None and len(data)-start >= min_len:
        items.append((start, data[start:].decode("ascii","ignore")))
    return items

def extract_strings(path):
    if shutil.which("strings"):
        raw=run_tool(["strings","-a","-n","4","-t","x",str(path)])
        items=[]
        for line in raw.splitlines():
            m=re.match(r"^\s*([0-9a-fA-F]+)\s+(.*)$",line)
            if m:
                try: items.append((int(m.group(1),16),m.group(2)))
                except Exception: pass
        if items:
            return items
    return python_strings(path)

def get_needed(path):
    if not is_elf(path):
        return []
    deps=[]
    if shutil.which("readelf"):
        raw=run_tool(["readelf","-d",str(path)])
        deps += re.findall(r"\(NEEDED\).*?\[([^\]]+)\]", raw)
    if not deps and shutil.which("objdump"):
        raw=run_tool(["objdump","-p",str(path)])
        for line in raw.splitlines():
            m=re.match(r"\s*NEEDED\s+(\S+)",line)
            if m: deps.append(m.group(1))
    return sorted(set(deps))

def get_comment(path):
    if is_elf(path) and shutil.which("readelf"):
        return run_tool(["readelf","-p",".comment",str(path)])[:10000]
    return ""

def get_dyn_symbols(path):
    """Return demangled dynamic symbol text where possible. Useful even for stripped ELF."""
    if not is_elf(path):
        return []
    symbols=[]
    if shutil.which("nm"):
        raw=run_tool(["nm","-D","-C",str(path)])
        for line in raw.splitlines():
            parts=line.strip().split(None,2)
            if len(parts) >= 2:
                symbols.append(parts[-1])
    elif shutil.which("readelf"):
        raw=run_tool(["readelf","--dyn-syms","-W",str(path)])
        for line in raw.splitlines():
            m=re.match(r"\s*\d+:\s+[0-9a-fA-F]+\s+\d+\s+\S+\s+\S+\s+\S+\s+\S+\s+(.+)$",line)
            if m:
                symbols.append(m.group(1).strip())
    return sorted(set(symbols))

def build_literal_index(db):
    idx=defaultdict(list)
    literals=set()
    for c in db["components"]:
        spec=int(c.get("specificity",50))
        weights={
            "project_marker":max(8,round(spec*0.80)),
            "function":max(5,round(spec*0.55)),
            "source_marker":max(4,round(spec*0.45)),
            "string":max(2,round(spec*0.25)),
        }
        for field,kind in [
            ("project_markers","project_marker"),
            ("functions","function"),
            ("source_markers","source_marker"),
            ("strings","string"),
        ]:
            for literal in c.get(field,[]):
                if literal:
                    idx[literal.lower()].append((c["name"],kind,weights[kind],literal))
                    literals.add(literal)
    alt="|".join(re.escape(x) for x in sorted(literals,key=lambda x:(-len(x),x.lower())))
    return idx, re.compile(alt,re.I) if alt else None

def build_function_index(db):
    idx=defaultdict(list)
    literals=set()
    for c in db["components"]:
        spec=int(c.get("specificity",50))
        weight=max(12,round(spec*0.70))
        for literal in c.get("functions",[]):
            if literal:
                idx[literal.lower()].append((c["name"],weight,literal))
                literals.add(literal)
    alt="|".join(re.escape(x) for x in sorted(literals,key=lambda x:(-len(x),x.lower())))
    return idx, re.compile(alt,re.I) if alt else None

def add_ev(store, component, kind, weight, value, file, location="", context=""):
    key=(kind,value.lower(),str(file),str(location))
    if key in store[component]["_keys"]:
        return
    store[component]["_keys"].add(key)
    store[component]["evidence"].append({
        "kind":kind,"weight":int(weight),"value":value,"file":str(file),
        "location":str(location),"context":context[:400]
    })

def scan_path(target, db, include_traces=False):
    by_name={c["name"]:c for c in db["components"]}
    literal_idx,literal_rx=build_literal_index(db)
    function_idx,function_rx=build_function_index(db)
    findings=defaultdict(lambda:{"evidence":[],"_keys":set(),"versions":set(),"files":set()})
    dynamic_rows=[]
    source_paths=set()
    files_scanned=binaries_scanned=text_files_scanned=0

    files=[target] if target.is_file() else [p for p in target.rglob("*") if p.is_file()]

    for path in files:
        files_scanned += 1
        try: size=path.stat().st_size
        except Exception: continue
        text=is_probably_text(path)
        elf=is_elf(path)

        if elf or (not text and size>0):
            binaries_scanned += 1
            deps=get_needed(path)
            for dep in deps:
                matched=[]
                for c in db["components"]:
                    for pat in c.get("library_patterns",[]):
                        if fnmatch.fnmatch(dep.lower(),pat.lower()):
                            add_ev(findings,c["name"],"dynamic_library",100,dep,path,"DT_NEEDED",dep)
                            findings[c["name"]]["files"].add(str(path))
                            matched.append(c["name"])
                dynamic_rows.append({"file":str(path),"library":dep,"matched_components":", ".join(sorted(set(matched)))})

            # Dynamic symbol table often survives stripping. Treat function hits here
            # as stronger evidence than the same token found in an arbitrary string.
            if function_rx:
                for sym in get_dyn_symbols(path):
                    for m in function_rx.finditer(sym):
                        for comp,weight,canonical in function_idx.get(m.group(0).lower(),[]):
                            add_ev(findings,comp,"dynamic_symbol",min(95,weight+15),canonical,path,"DYNSYM",sym)
                            findings[comp]["files"].add(str(path))

            string_items=extract_strings(path)
            for off,s in string_items:
                for sp in SOURCE_PATH_RE.findall(s):
                    source_paths.add(sp)
                if literal_rx:
                    for m in literal_rx.finditer(s):
                        for comp,kind,weight,canonical in literal_idx.get(m.group(0).lower(),[]):
                            add_ev(findings,comp,kind,weight,canonical,path,hex(off),s)
                            findings[comp]["files"].add(str(path))
            comment=get_comment(path)
            if comment and literal_rx:
                for m in literal_rx.finditer(comment):
                    for comp,kind,weight,canonical in literal_idx.get(m.group(0).lower(),[]):
                        add_ev(findings,comp,kind,weight,canonical,path,".comment",comment)
                        findings[comp]["files"].add(str(path))

            candidates=[n for n,f in findings.items() if str(path) in f["files"]]
            if candidates and string_items:
                joined="\n".join(s for _,s in string_items)
                for name in candidates:
                    for vrx in by_name[name].get("version_regex",[]):
                        try:
                            for vm in re.finditer(vrx,joined):
                                ver=vm.group(1)
                                findings[name]["versions"].add(ver)
                                add_ev(findings,name,"version",20,ver,path,"strings",vm.group(0))
                        except re.error:
                            pass

        elif text and size <= 16*1024*1024:
            text_files_scanned += 1
            try:
                with open(path,"r",encoding="utf-8",errors="ignore") as f:
                    for ln,line in enumerate(f,1):
                        if literal_rx:
                            for m in literal_rx.finditer(line):
                                for comp,kind,weight,canonical in literal_idx.get(m.group(0).lower(),[]):
                                    bonus=8 if kind in ("function","source_marker","project_marker") else 3
                                    add_ev(findings,comp,"source_"+kind,min(100,weight+bonus),canonical,path,ln,line.strip())
                                    findings[comp]["files"].add(str(path))
                        for sp in SOURCE_PATH_RE.findall(line):
                            source_paths.add(sp)
            except Exception:
                pass

    caps={
        "dynamic_library":100,
        "project_marker":100,"source_project_marker":100,
        "function":120,"source_function":140,"dynamic_symbol":140,
        "source_marker":90,"source_source_marker":110,
        "string":40,"source_string":50,
        "version":40
    }
    results=[]
    for name,f in findings.items():
        c=by_name[name]
        sums=defaultdict(int)
        normalized=set()
        has_dynamic=False
        for e in f["evidence"]:
            sums[e["kind"]]+=e["weight"]
            nk=e["kind"].replace("source_","")
            if nk=="dynamic_symbol": nk="function"
            normalized.add(nk)
            has_dynamic |= e["kind"]=="dynamic_library"
        score=min(300,sum(min(v,caps.get(k,80)) for k,v in sums.items()))
        independent=len(normalized)

        if has_dynamic:
            conf="CONFIRMED_DYNAMIC"
            interpretation="Подтверждённая динамическая зависимость ELF (DT_NEEDED)."
        elif score>=150 and independent>=3:
            conf="HIGH"
            interpretation="Высокая вероятность встроенного/статически слинкованного либо производного кода."
        elif score>=90 and independent>=2:
            conf="MEDIUM"
            interpretation="Вероятный компонент; требуется ручная проверка происхождения и версии."
        elif score>=40:
            conf="LOW"
            interpretation="Слабое эвристическое совпадение; не включать в официальный SBOM без дополнительного evidence."
        else:
            conf="TRACE"
            interpretation="След/общая строка; практически не является доказательством компонента."

        if conf=="TRACE" and not include_traces:
            continue
        results.append({
            "name":name,"aliases":c.get("aliases",[]),"category":c["category"],
            "description_ru":c["description_ru"],"specificity":c["specificity"],
            "score":score,"confidence":conf,"interpretation":interpretation,
            "versions":sorted(f["versions"]),"files":sorted(f["files"]),
            "evidence":sorted(f["evidence"],key=lambda x:(-x["weight"],x["kind"],x["value"]))
        })

    order={"CONFIRMED_DYNAMIC":0,"HIGH":1,"MEDIUM":2,"LOW":3,"TRACE":4}
    results.sort(key=lambda r:(order.get(r["confidence"],9),-r["score"],r["name"].lower()))
    return {
        "target":str(target),
        "summary":{
            "files_scanned":files_scanned,"binaries_scanned":binaries_scanned,
            "text_files_scanned":text_files_scanned,"components_found":len(results),
            "confirmed_dynamic":sum(r["confidence"]=="CONFIRMED_DYNAMIC" for r in results),
            "high":sum(r["confidence"]=="HIGH" for r in results),
            "medium":sum(r["confidence"]=="MEDIUM" for r in results),
            "low":sum(r["confidence"]=="LOW" for r in results),
        },
        "architecture":infer_architecture(results),
        "components":results,
        "dynamic_dependencies":dynamic_rows,
        "source_paths":sorted(source_paths)
    }

def infer_architecture(results):
    cats=defaultdict(list)
    for r in results:
        if r["confidence"] in ("CONFIRMED_DYNAMIC","HIGH","MEDIUM"):
            cats[r["category"]].append(r["name"])
    groups=[
      ("Packet capture / fast I/O",{"packet_capture","packet_processing","ebpf_xdp","rdma","network_primitives"},"Слой захвата/ускоренной обработки сетевых пакетов."),
      ("DPI / protocol analysis",{"dpi_ids_engine","dpi_library","network_security_monitor","protocol_analysis","protocol_parser","protocol_parser_generator","fingerprinting"},"DPI/IDS/NSM или протокольный анализ."),
      ("Signature / content analysis",{"pattern_matching","content_detection","content_fingerprinting","file_analysis"},"Сигнатурный поиск и анализ payload/files."),
      ("Enrichment",{"ip_enrichment","dns_protocol"},"IP/DNS enrichment."),
      ("Messaging / event pipeline",{"messaging","serialization"},"Межпроцессный/межсервисный event pipeline."),
      ("Storage / state",{"storage"},"Локальное состояние/metadata storage."),
      ("ML / behavioral analytics",{"ml_analytics"},"ML/аналитический слой."),
      ("ICS / IoT protocol support",{"ics_protocol","iot_protocol"},"OT/ICS/IoT протокольный слой.")
    ]
    layers=[]
    for title,group,note in groups:
        names=sorted({n for cat in group for n in cats.get(cat,[])})
        if names: layers.append({"layer":title,"components":names,"note":note})
    if len(layers)>=4 and any(l["layer"]=="DPI / protocol analysis" for l in layers):
        overall="Набор компонентов похож на многослойную NDR/DPI/IDS архитектуру."
    elif any(l["layer"]=="DPI / protocol analysis" for l in layers):
        overall="Есть существенные признаки DPI/IDS/протокольного анализа."
    elif any(l["layer"]=="Packet capture / fast I/O" for l in layers):
        overall="Есть packet-processing слой, но DPI/NDR назначение пока не доказано."
    else:
        overall="Недостаточно специфичных признаков для уверенного вывода об архитектуре."
    return {"overall":overall,"layers":layers}

def write_outputs(report,outdir):
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    (outdir/"source_paths.txt").write_text("\n".join(report["source_paths"]),encoding="utf-8")

    with open(outdir/"components.csv","w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f)
        w.writerow(["component","confidence","score","category","versions","files","top_evidence","interpretation"])
        for r in report["components"]:
            top="; ".join(f'{e["kind"]}:{e["value"]}' for e in r["evidence"][:8])
            w.writerow([r["name"],r["confidence"],r["score"],r["category"],", ".join(r["versions"]),
                        "; ".join(r["files"]),top,r["interpretation"]])
    with open(outdir/"dynamic_dependencies.csv","w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=["file","library","matched_components"])
        w.writeheader(); w.writerows(report["dynamic_dependencies"])

    sbom_components=[]
    for r in report["components"]:
        if r["confidence"] not in ("CONFIRMED_DYNAMIC","HIGH"):
            continue
        c={"type":"library","name":r["name"],
           "properties":[
              {"name":"ndr-dpi-scanner:confidence","value":r["confidence"]},
              {"name":"ndr-dpi-scanner:score","value":str(r["score"])}
           ]}
        if r["versions"]: c["version"]=r["versions"][0]
        sbom_components.append(c)
    bom={"bomFormat":"CycloneDX","specVersion":"1.6","version":1,"components":sbom_components}
    (outdir/"candidate_sbom.cdx.json").write_text(json.dumps(bom,indent=2,ensure_ascii=False),encoding="utf-8")

    def esc(x): return html.escape(str(x))
    def badge(conf):
        color={"CONFIRMED_DYNAMIC":"#166534","HIGH":"#1d4ed8","MEDIUM":"#a16207","LOW":"#9a3412","TRACE":"#6b7280"}.get(conf,"#6b7280")
        return f'<span style="background:{color};color:white;padding:2px 8px;border-radius:10px;font-size:12px">{esc(conf)}</span>'

    cards="".join(f'<div class="card"><b>{esc(k.replace("_"," ").title())}</b><div class="num">{v}</div></div>' for k,v in report["summary"].items())
    layers="".join(f'<div class="layer"><b>{esc(l["layer"])}</b><br>{esc(", ".join(l["components"]))}<br><small>{esc(l["note"])}</small></div>' for l in report["architecture"]["layers"])
    rows=[]; details=[]
    for i,r in enumerate(report["components"]):
        top="; ".join(f'{e["kind"]}: {e["value"]}' for e in r["evidence"][:4])
        rows.append(f'<tr><td><a href="#c{i}">{esc(r["name"])}</a></td><td>{badge(r["confidence"])}</td><td>{r["score"]}</td><td>{esc(r["category"])}</td><td>{esc(", ".join(r["versions"]) or "—")}</td><td>{esc(top)}</td></tr>')
        evrows=[]
        for e in r["evidence"]:
            evrows.append(f'<tr><td>{esc(e["kind"])}</td><td>{e["weight"]}</td><td><code>{esc(e["value"])}</code></td><td>{esc(e["file"])}</td><td>{esc(e["location"])}</td><td><code>{esc(e["context"])}</code></td></tr>')
        details.append(
            f'<section id="c{i}"><h3>{esc(r["name"])} {badge(r["confidence"])}</h3>'
            f'<p>{esc(r["description_ru"])}</p><p><b>Score:</b> {r["score"]} &nbsp; <b>Версии:</b> {esc(", ".join(r["versions"]) or "не определена")}</p>'
            f'<p>{esc(r["interpretation"])}</p>'
            '<table><thead><tr><th>Evidence</th><th>Weight</th><th>Value</th><th>File</th><th>Location</th><th>Context</th></tr></thead>'
            f'<tbody>{"".join(evrows)}</tbody></table></section>'
        )
    dynrows="".join(f'<tr><td>{esc(x["file"])}</td><td><code>{esc(x["library"])}</code></td><td>{esc(x["matched_components"]) or "—"}</td></tr>' for x in report["dynamic_dependencies"])
    paths="<br>".join(f"<code>{esc(x)}</code>" for x in report["source_paths"][:500]) or "—"

    doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>NDR/DPI scan report</title>
<style>
body{{font-family:Arial,sans-serif;margin:28px;color:#111827;background:#f8fafc}}
h1,h2,h3{{color:#111827}} .cards{{display:flex;flex-wrap:wrap;gap:10px}}
.card{{background:white;border:1px solid #e5e7eb;border-radius:10px;padding:12px 16px;min-width:130px}}
.num{{font-size:26px;font-weight:bold;margin-top:4px}}
.layer{{background:white;border-left:4px solid #64748b;padding:10px 14px;margin:8px 0}}
table{{border-collapse:collapse;width:100%;background:white;margin:10px 0 24px}}
th,td{{border:1px solid #e5e7eb;padding:7px;vertical-align:top;text-align:left;font-size:13px}}
th{{background:#f1f5f9}} code{{font-size:12px;word-break:break-all}}
section{{margin-top:34px}} .notice{{background:#fff7ed;border:1px solid #fed7aa;padding:12px;border-radius:8px}}
</style></head><body>
<h1>NDR/DPI composition triage</h1>
<p><b>Target:</b> <code>{esc(report["target"])}</code></p>
<div class="notice">CONFIRMED_DYNAMIC основан на ELF DT_NEEDED. HIGH/MEDIUM — эвристика и требуют ручной проверки перед включением в официальный SBOM.</div>
<h2>Summary</h2><div class="cards">{cards}</div>
<h2>Architecture inference</h2><p><b>{esc(report["architecture"]["overall"])}</b></p>{layers or "<p>Специфичные слои не определены.</p>"}
<h2>Detected components</h2>
<table><thead><tr><th>Component</th><th>Confidence</th><th>Score</th><th>Category</th><th>Version</th><th>Top evidence</th></tr></thead><tbody>{"".join(rows)}</tbody></table>
<h2>ELF dynamic dependencies</h2>
<table><thead><tr><th>File</th><th>DT_NEEDED</th><th>Mapped component</th></tr></thead><tbody>{dynrows}</tbody></table>
<h2>Recovered source paths</h2><div>{paths}</div>
<h2>Evidence details</h2>{"".join(details)}
</body></html>"""
    (outdir/"report.html").write_text(doc,encoding="utf-8")

def main():
    ap=argparse.ArgumentParser(description="Heuristic NDR/DPI OSS composition scanner")
    ap.add_argument("target",help="Binary file or directory")
    ap.add_argument("--db",default=str(Path(__file__).with_name("ndr_dpi_oss_db.json")))
    ap.add_argument("-o","--outdir",default="ndr_dpi_report")
    ap.add_argument("--include-traces",action="store_true")
    args=ap.parse_args()
    target=Path(args.target).resolve()
    db=json.loads(Path(args.db).read_text(encoding="utf-8"))
    report=scan_path(target,db,args.include_traces)
    outdir=Path(args.outdir)
    write_outputs(report,outdir)
    print(json.dumps(report["summary"],indent=2,ensure_ascii=False))
    print("\nArchitecture:",report["architecture"]["overall"])
    print("\nTop components:")
    for r in report["components"][:20]:
        ver=",".join(r["versions"]) if r["versions"] else "-"
        print(f"  {r['confidence']:17} score={r['score']:3}  {r['name']:<20} version={ver}")
    print("\nReport:",outdir/"report.html")
    print("JSON:  ",outdir/"report.json")
    print("CSV:   ",outdir/"components.csv")
    print("SBOM:  ",outdir/"candidate_sbom.cdx.json")

if __name__=="__main__":
    main()
