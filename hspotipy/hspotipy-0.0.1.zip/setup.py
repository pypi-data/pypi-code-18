from setuptools import setup, find_packages

install_requires = [
    'spotipy',
]

setup(
    name = "hspotipy",
    version = "0.0.1",
    include_package_data=True,
    author='HSpotipy Contributors',
    author_email='dhsig552@163.com',
    url = "https://github.com/zsdonghao/hspotipy" ,
    license = "apache" ,
    packages = find_packages(),
    install_requires=install_requires,
    # scripts=['tutorial_mnist.py'],
    description = "Spotify Music API",
    keywords = "Music, Spotipy",
    platform=['any'],
)
