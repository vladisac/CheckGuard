__author__ = 'nero_luci'

from distutils.core import setup
try:
    import py2exe
except ImportError:
    print("You must have py2exe module installed")
    exit()

setup(console=['CheckGuard.py'], requires=['watchdog', 'py2exe'])
