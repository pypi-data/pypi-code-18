from cx_Freeze import setup,Executable

includefiles = ['sancompt.ui', 'calculations.py', 'image/v1.png','image/sec2.png','image/v0.png','image/v2.png','image/v3.png','image/v4.png','image/v5.png','image/v6.png','image/v7.png','image/beam.png','image/sancomp.ico','image/sancomp.png','nucleo-elasticidade.dat', 'face-elasticidade-poisson.dat']
includes = []
excludes = ['Tkinter']
packages = []

setup(
    name = 'Sancomp',
    version = '1.2',
    description = 'A Sandwich Composite Analysis Software',
    author = 'Douglas Rodrigues',
    author_email = 'rodriguesdouglas@ufrgs.br',
    options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}}, 
    executables = [Executable('sancomp.py', base = "Win32GUI", shortcutName="Sancomp", shortcutDir="DesktopFolder")]
)