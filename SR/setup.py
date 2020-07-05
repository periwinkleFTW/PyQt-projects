from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [], include_files = ['/Users/andreyfrol/PycharmProjects/qt-projects/venv/lib/python3.8/site-packages/PySide2/QtCore.abi3.so'])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main_app.py', base=base, targetName = 'SimpleReport')
]

setup(name='SimpleReport',
      version = '0.1',
      description = 'My App',
      options = dict(build_exe = buildOptions),
      executables = executables)