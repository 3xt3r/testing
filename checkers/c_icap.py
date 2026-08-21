# -*- coding: utf-8 -*-
import os
import re
from checkers.base_checker import BaseChecker

class Cicap(BaseChecker):
    VENDOR = "c-icap_project"
    PRODUCT = "c-icap"
    LINK_SOURCE = "https://github.com/c-icap/c-icap-server.git"

    SOURCE_FILENAME_PATTERNS = [
        r"(^|/)configure\.ac$",
        # Реальный c-icap-server НЕ хранит версию литералом в configure.ac —
        # там AC_INIT([c_icap], m4_normalize(m4_include([VERSION.m4]))), то
        # есть версия подключается из отдельного файла VERSION.m4. Это
        # основной источник версии; сам configure.ac разбирается только как
        # fallback (см. RX_AC_INIT ниже) — вдруг форк/старая версия хранит
        # версию прямо в AC_INIT.
        r"(^|/)VERSION\.m4$",
        # Дополнительный источник: include/c-icap-conf.h содержит
        # C_ICAP_HEX_VERSION — упакованную hex-версию. Это реальный
        # заголовочный файл с версией, поэтому он надёжнее, чем
        # configure.ac/VERSION.m4 (хотя и требует декодирования).
        r"(^|/)include/c-icap-conf\.h$",
    ]

    CONTAINS_PATTERNS = [
        r"Copyright\s*\(C\)\s*(?:\d{4}(?:-\d{4})?\s+)?Christos\s+Tsantilas",
        r"Can\s+not\s+execute\s+ci_command_register_action",
        r"AC_INIT\(\s*\[?c.icap\]?",
    ]

    # Основной источник: VERSION.m4 — обычно один литерал версии в файле
    # (исторически бывает как "1.7.0", так и старый 6-значный формат вроде
    # "030606rc1" — оставляем в результате как есть, без нормализации).
    RX_VERSION_M4 = re.compile(
        r"([0-9]{1,4}(?:\.[0-9]+){1,3}[A-Za-z0-9]*|[0-9]{6}[A-Za-z0-9]*)"
    )

    # Fallback: некоторые форки/старые версии инлайнят версию прямо в
    # AC_INIT([c_icap], [x.y.z]) без m4_include — если так, ловим и это.
    RX_AC_INIT = re.compile(
        r"AC_INIT\(\s*\[?c.icap\]?\s*,\s*\[([0-9]+(?:\.[0-9]+){1,3})\]",
        re.IGNORECASE,
    )

    # Упакованная hex-версия в include/c-icap-conf.h:
    #   #define C_ICAP_HEX_VERSION 0x000000050005
    # Формат: 0x0000MMmmpppp (major, minor, patch — по 4 hex-цифры).
    # Декодируем по формуле из build/c_icap_version.awk:
    #   major = (hex >> 32) & 0xFFFF
    #   minor = (hex >> 16) & 0xFFFF
    #   patch = hex & 0xFFFF
    # Пример: 0x000000050005 -> major=0, minor=5, patch=5 -> "0.5.5"
    RX_HEX_VERSION = re.compile(
        r"#\s*define\s+C_ICAP_HEX_VERSION\s+0x([0-9A-Fa-f]{12})"
    )

    def _decode_hex_version(self, hex_str: str):
        """Декодировать 12-значную hex-строку в версию major.minor.patch."""
        try:
            val = int(hex_str, 16)
        except ValueError:
            return None
        major = (val >> 32) & 0xFFFF
        minor = (val >> 16) & 0xFFFF
        patch = val & 0xFFFF
        return f"{major}.{minor}.{patch}"

    def check_file_versions_only(self, content: str, path: str):
        if not self.match_source_filename(path):
            return []
        s = content or ""
        src_abs = os.path.abspath(path)
        base = os.path.basename(path)

        if base.upper() == "VERSION.M4":
            m = self.RX_VERSION_M4.search(s)
            if m:
                return [self.make_result(m.group(1), src_abs, extra={"version_source_abs": src_abs})]
            return []

        # include/c-icap-conf.h — реальный исходный код с hex-версией.
        # Это самый надёжный сигнал, поэтому обрабатываем его первым.
        if base == "c-icap-conf.h":
            m = self.RX_HEX_VERSION.search(s)
            if m:
                ver = self._decode_hex_version(m.group(1))
                if ver:
                    return [self.make_result(ver, src_abs, extra={"version_source_abs": src_abs})]
            return []

        m = self.RX_AC_INIT.search(s)
        if not m:
            return []
        return [self.make_result(m.group(1), src_abs, extra={"version_source_abs": src_abs})]

    def check_meta(self, directory: str):
        # include/c-icap-conf.h в приоритете — это реальный исходный код
        # с упакованной hex-версией. Декодируем по формуле из
        # build/c_icap_version.awk (ground truth).
        conf_h = os.path.join(directory, "include", "c-icap-conf.h")
        if os.path.isfile(conf_h):
            try:
                with open(conf_h, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except OSError:
                text = ""
            m = self.RX_HEX_VERSION.search(text)
            if m:
                ver = self._decode_hex_version(m.group(1))
                if ver:
                    return [self.make_result(ver, os.path.abspath(conf_h), extra={
                        "version_source_file": os.path.relpath(conf_h, directory),
                        "origin": "meta:include/c-icap-conf.h",
                    })]

        # VERSION.m4 — второй по надёжности: это то, что реально
        # подключается в AC_INIT в апстриме.
        version_m4 = os.path.join(directory, "VERSION.m4")
        if os.path.isfile(version_m4):
            try:
                with open(version_m4, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except OSError:
                text = ""
            m = self.RX_VERSION_M4.search(text)
            if m:
                return [self.make_result(m.group(1), os.path.abspath(version_m4), extra={
                    "version_source_file": os.path.relpath(version_m4, directory),
                    "origin": "meta:VERSION.m4",
                })]

        # configure.ac — fallback для форков, где версия инлайнена напрямую.
        full = os.path.join(directory, "configure.ac")
        if not os.path.isfile(full):
            return []
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception:
            return []
        m = self.RX_AC_INIT.search(text)
        if not m:
            return []

        return [self.make_result(m.group(1), os.path.abspath(full), extra={
            "version_source_file": os.path.relpath(full, directory),
            "origin": "meta:configure.ac",
        })]