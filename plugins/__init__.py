import os
import importlib


def import_att(root_dots, root_path):

    root_dir = os.path.dirname(root_path)

    for path in os.listdir(root_dir):

        fullpath = os.path.join(root_dir, path)
        name, ext = os.path.splitext(path)

        if (os.path.isdir(fullpath) or ext == '.py') and name[:2] != '__':
            importlib.import_module(root_dots + '.' + name)
