from setuptools import setup, find_packages

setup(
    name = "beatract",
    version = "1.3.5",
    author = "Hyun Joon Choi",
    author_email = "chj878194@naver.com",
    packages=['beatract'],
    url = "https://github.com/Tok-TokPlay/Tok-BeatExtractor",
    maintainer = "Hyun Joon Choi",
    description="Beat Extracting module for music",
    install_requires=[
        'audioread >= 2.0.0',
        'numpy >= 1.8.0',
        'scipy >= 0.13.0',
        'scikit-learn >= 0.14.0',
        'joblib >= 0.7.0',
        'decorator >= 3.0.0',
        'six >= 1.3',
        'resampy >= 0.1.2',
        'librosa >= 0.5.0'
    ]
)
