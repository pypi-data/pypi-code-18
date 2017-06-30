# import numpy

__version__ = "0.9.2"


def main():
    import argparse
    from .simulation import SoilSimulation
    from . import settings

    parser = argparse.ArgumentParser(description='Run a SOIL simulation')
    parser.add_argument('file', type=str,
                        nargs="?",
                        default='simulation.yml',
                        help='file containing the simulation configuration.')

    args = parser.parse_args()

    for config in settings.load(args.file):
        print("Using config(s): {config[name]}".format(config=config))

        sim = SoilSimulation.from_config(config)
        sim.run_simulation()
        sim.dump_data()


if __name__ == '__main__':
    main()
