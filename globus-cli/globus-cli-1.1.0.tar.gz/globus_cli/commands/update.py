import atexit
import click

from globus_cli.safeio import safeprint
from globus_cli.version import get_versions
from globus_cli.parsing import common_options, HiddenOption


@click.command('update', help='Update the Globus CLI to its latest version')
@common_options(no_format_option=True, no_map_http_status_option=True)
@click.option('--yes', is_flag=True,
              help='Automatically say "yes" to all prompts')
# hidden options to fetch branches or tags from GitHub. One turns this mode
# on or off, and the other is used to set a non-master target
# --development-version implies --development
@click.option('--development', is_flag=True, cls=HiddenOption)
@click.option('--development-version', cls=HiddenOption, default=None)
def update_command(yes, development, development_version):
    """
    Executor for `globus update`
    """
    # enforce that pip MUST be installed
    # Why not just include it in the setup.py requirements? Mostly weak
    # reasons, but it shouldn't matter much.
    # - if someone has installed the CLI without pip, then they haven't
    #   followed our install instructions, so it's mostly a non-issue
    # - we don't want to have `pip install -U globus-cli` upgrade pip -- that's
    #   a little bit invasive and easy to do by accident on modern versions of
    #   pip where `--upgrade-strategy` defaults to `eager`
    # - we may want to do distributions in the future with dependencies baked
    #   into a package, but we'd never want to do that with pip. More changes
    #   would be needed to support that use-case, which we've discussed, but
    #   not depending directly on pip gives us a better escape hatch
    # - if we depend on pip, we need to start thinking about what versions we
    #   support. In point of fact, that becomes an issue as soon as we add this
    #   command, but not being explicit about it lets us punt for now (maybe
    #   indefinitely) on figuring out version requirements. All of that is to
    #   say: not including it is bad, and from that badness we reap the rewards
    #   of procrastination and non-explicit requirements
    # - Advanced usage, like `pip install -t` can produce an installed version
    #   of the CLI which can't import its installing `pip`. If we depend on
    #   pip, anyone doing this is forced to get two copies of pip, which seems
    #   kind of nasty (even if "they're asking for it")
    try:
        import pip
    except ImportError:
        safeprint("`globus update` requires pip. "
                  "Please install pip and try again")
        click.get_current_context().exit(1)

    # --development-version implies --development
    development = development or (development_version is not None)

    # if we're running with `--development`, then the target version is a
    # tarball from GitHub, and we can skip out on the safety checks
    if development:
        # default to master
        development_version = development_version or "master"
        target_version = (
            "https://github.com/globus/globus-cli/archive/{}"
            ".tar.gz#egg=globus-cli"
            ).format(development_version)
    else:
        # lookup version from PyPi, abort if we can't get it
        latest, current = get_versions()
        if latest is None:
            safeprint('Failed to lookup latest version. Aborting.')
            click.get_current_context().exit(1)

        # in the case where we're already up to date, do nothing and exit
        if current == latest:
            safeprint('You are already running the latest version: {}'
                      .format(current))
            return

        # if we're up to date (or ahead, meaning a dev version was installed)
        # then prompt before continuing, respecting `--yes`
        else:
            safeprint(('You are already running version {0}\n'
                       'The latest version is           {1}')
                      .format(current, latest))
            if not yes and (
                    not click.confirm('Continue with the upgrade?',
                                      default=True)):
                click.get_current_context().exit(1)

        # if we make it through to here, it means we didn't hit any safe (or
        # unsafe) abort conditions, so set the target version for upgrade to
        # the latest
        target_version = 'globus-cli=={}'.format(latest)

    # print verbose warning/help message, to guide less fortunate souls who hit
    # Ctrl+C at a foolish time, lose connectivity, or don't invoke with `sudo`
    # on a global install of the CLI
    safeprint(
        ("The Globus CLI will now update itself.\n"
         "In the event that an error occurs or the update is interrupted, we "
         "recommend uninstalling and reinstalling the CLI.\n"
         "Update Target: {}\n").format(target_version))

    # register the upgrade activity as an atexit function
    # this ensures that most library teardown (other than whatever libs might
    # jam into atexit themselves...) has already run, and therefore protects us
    # against most potential bugs resulting from upgrading click while a click
    # command is running
    #
    # NOTE: there is a risk that we will see bugs on upgrade if the act of
    # doing a pip upgrade install changes state on disk and we (or a lib we
    # use) rely on that via pkg_resources, lazy/deferred imports, or good
    # old-fashioned direct inspection of `__file__` and the like DURING an
    # atexit method. Anything outside of atexit methods remains safe!
    @atexit.register
    def do_upgrade():
        pip.main(['install', '--upgrade', target_version])
