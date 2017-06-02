import typing
from pipper import wrapper


def install(package: str):
    """ """

    if package.startswith(('http://', 'https://')):
        if wrapper.update_required(package):
            print('[INSTALLING]: "{}"'.format(package))
            return wrapper.install_wheel(package)

        data = wrapper.parse_url(package)
        print('[SKIPPED]: "{}" version {} already installed'.format(
            data['package_name'],
            data['version'].replace('-', '.')
        ))
        return None

    return None


def install_many(packages: typing.List[str]):
    """ """

    return [install(p) for p in packages]
