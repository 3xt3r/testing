# NDR/DPI OSS composition scanner

Файлы:

- `ndr_dpi_oss_db.json` — база из 114 OSS-компонентов с fingerprints.
- `ndr_dpi_scan.py` — сканер stripped ELF, каталогов с бинарями и исходников.
- scanner не запускает исследуемый ELF: для dynamic dependencies используются `readelf`/`objdump`, а не `ldd`.
- для `stripped` ELF дополнительно анализируется dynamic symbol table (`nm -D -C`/`readelf --dyn-syms`), которая часто сохраняет имена импортируемых функций.

## Один stripped ELF

```bash
python3 ndr_dpi_scan.py ./dpi -o dpi_report
```

Откройте `dpi_report/report.html`.

## Распакованный продукт

```bash
python3 ndr_dpi_scan.py /opt/product -o product_report
```

## Результаты

- `report.html` — читаемый отчёт с evidence и архитектурными слоями.
- `report.json` — полный машиночитаемый результат.
- `components.csv` — сводная таблица компонентов.
- `final_components.xlsx` — финальная Excel-таблица с компонентами, confidence, score, версиями, evidence и решением по включению в SBOM.
- `dynamic_dependencies.csv` — ELF `DT_NEEDED`.
- `source_paths.txt` — пути исходников, восстановленные из строк.
- `candidate_sbom.cdx.json` — CycloneDX 1.6 только для `CONFIRMED_DYNAMIC` и `HIGH`.

## Confidence

- `CONFIRMED_DYNAMIC` — библиотека найдена в ELF `DT_NEEDED`.
- `HIGH` — несколько независимых сильных fingerprints; возможен статически встроенный/производный код.
- `MEDIUM` — вероятный компонент, требуется ручная проверка.
- `LOW` — слабая эвристика; не считать доказательством SBOM.
- `TRACE` — очень слабый след; по умолчанию скрыт. Включается `--include-traces`.

## Важное ограничение

Статически встроенный C/C++ компонент нельзя надёжно доказать только набором строк.
Для официального SBOM проверяйте версию, происхождение кода, build metadata, source paths и несколько независимых fingerprint-групп.


## XLSX output

Для автоматического создания `final_components.xlsx` установите:

```bash
pip install XlsxWriter
```

Если XlsxWriter не установлен, scanner продолжит работу и создаст остальные JSON/CSV/HTML отчёты.
