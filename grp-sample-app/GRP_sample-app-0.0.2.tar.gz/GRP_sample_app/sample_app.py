from GRP_sample_app.package_one.pack_one import PackOne
from GRP_sample_app.package_two.pack_two import PackTwo


def main():
    p1 = PackOne()
    p2 = PackTwo()
    p1.do()
    p2.process()


if __name__ == '__main__':
    main()
