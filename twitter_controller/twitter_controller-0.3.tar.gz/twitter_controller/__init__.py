from twitter_controller.Person import Person
from twitter_controller.PersonAnalyzer import PersonAnalyzer
from twitter_controller.Plotter import Factor, Plotter
from twitter_controller.TwitterDownloader import TwitterDownloader, TwitterDownloaderException
from twitter_controller.Text import Text
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Invalid number of arguments')
        exit(1)
    p = Person(sys.argv[1])

    a = PersonAnalyzer(p)

    a.full_analyze()

    a.plot_all()
