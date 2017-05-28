from distutils.core import setup

setup(
    name="aisnakes",
    version="1.0",
    scripts=["aisnakes", "config.py", "brains.py", "snakes.py"],
    install_requires=["numpy", "arcade"],

    author= "JanKaifer",
    author_email="kaifer741@gmail.com",
    description="Snakes learning to live with one vs all perceptrons",
    keywords=["snake", "ai", "perceptron", "machine", "learning", "cool", "useless"],
    url="https://github.com/JanKaifer/AISnakes"
)
