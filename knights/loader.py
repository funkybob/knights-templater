
import pathlib

from .compiler import kompile

PATHS = []


class TemplateNotFound(Exception):
    pass


class TemplateLoader(dict):
    def __init__(self, paths):
        self.paths = [
            (pathlib.Path.cwd() / path).resolve()
            for path in paths
        ]

    def load(self, name, raw=False):
        for path in self.paths:
            full_path = path / name
            try:
                full_path.relative_to(path)
            except ValueError:
                # XXX Raise Suspicious Op?
                continue
            if full_path.exists() and full_path.is_file():
                with full_path.open(encoding='utf-8') as fin:
                    src = fin.read()

                return kompile(src, raw=raw, filename=str(full_path), loader=self)
        raise TemplateNotFound(name)

    def __missing__(self, key):
        self[key] = tmpl = self.load(key)
        return tmpl
