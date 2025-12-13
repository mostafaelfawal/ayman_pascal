"""Utilities to enumerate system printers (best-effort).

This tries to use `win32print` on Windows to list installed printers.
If unavailable, returns an empty list so UI can still function.
"""
from typing import List

try:
    import win32print
except Exception:
    win32print = None


def get_system_printers() -> List[str]:
    """Return a list of system printer names (Windows) or [] if unavailable."""
    if win32print is None:
        return []
    try:
        flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        printers = win32print.EnumPrinters(flags)
        return [p[2] for p in printers]
    except Exception:
        return []
