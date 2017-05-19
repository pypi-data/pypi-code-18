import docker
import argparse


def purge_commandline():
    client = docker.from_env()

    parser = argparse.ArgumentParser(description='Purging old docker containers', prog='docker_purge.py')
    parser.add_argument('-q', action='store_true', default=False, dest='quiet',
                        help='Use -q to quietly purge. By default it runs interactively.')
    parser.add_argument('-a', action='store_true', default=False)

    args = parser.parse_args()

    purge_containers(client, args)


def purge_containers(client, args):
    quiet = args.quiet
    filter_all = args.a

    count_purges = 0

    if not filter_all:
        containers = client.containers.list(True, '', {'status': 'exited'})
        print "There are " + str(len(containers)) + " containers in Exited state."
    else:
        containers = client.containers.list(True)
        print "There are " + str(len(containers)) + " containers."

    for container in containers:
        if container.attrs['State']['Status'] == 'exited':

            if not quiet:
                delete = raw_input('Do you want to delete ' + container.attrs['Name'] + " (y/n/q) ")

                if delete == 'y':
                    client.api.remove_container(container.attrs['Id'])
                    print "Removed " + container.attrs['Name']
                    count_purges += 1

                if delete == 'q':
                    exit(0)
            else:
                client.api.remove_container(container.attrs['Id'])
                print "Removed " + container.attrs['Name']
                count_purges += 1

    if count_purges > 0:
        print str(count_purges) + " containers purged"
    else:
        print "No containers purged"
