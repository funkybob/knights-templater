
import os.path

from .compiler import kompile

PATHS = []


def add_path(path):
    path = os.path.abspath(path)

    if path not in PATHS:
        PATHS.append(path)


def load_template(name, paths=None):
    if paths is None:
        paths = PATHS[:]

    for path in paths:
        full_name = os.path.abspath(os.path.join(path, name))
        if not full_name.startswith(path):
            continue
        try:
            with open(full_name, encoding='utf-8') as fin:
                src = fin.read()

            return kompile(src)
        except:
            import traceback
            traceback.print_exc()

    return None
