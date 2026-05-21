"""Local compatibility shim for FastAPI's optional annotated_doc dependency."""

from __future__ import annotations


class Doc(str):
    """Minimal runtime-compatible stand-in used only for import satisfaction."""

    def __new__(cls, value: str = "", *args, **kwargs):  # type: ignore[override]
        return super().__new__(cls, value)
