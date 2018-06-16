import os


def import_att(root_dots, root_path):  # att = All The Things!

    root_dir = os.path.basename(
        os.path.dirname(root_path)
    )

    for name in os.listdir(root_dir):
        __import__(root_dots + '.' + name)

