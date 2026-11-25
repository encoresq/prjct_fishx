import sys
import os

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_path()

def base_path(filename):
    return os.path.join(BASE_DIR, filename)

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, "ui", filename)
    return os.path.join(BASE_DIR, "ui", filename)
