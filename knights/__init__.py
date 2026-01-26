from . import loader
from .compiler import kompile


def render(source: str, context: dict | None = None, loader: loader.TemplateLoader | None = None) -> str:
    return kompile(source, loader=loader)(context or {})
