"""n8pushover.py
A quick implementation of the Pushover API in Python, using an envvar or the
keyring module (desktop) or Pythonista's keychain module (iOS) to store
credentials.

Usage:
    from n8scripts.n8pushover import push
    push("It's alive!")
    push("This one has a title.", title="My awesome title.")
"""

import __main__
import argparse
import http
import os.path
import typing
import urllib.parse
import urllib.request


def get_credentials() -> typing.Tuple[str, str]:
    """Get Pushover user and api_token."""
    try:
        user = os.environ['PUSHOVER_USER']
        api_token = os.environ['PUSHOVER_API_TOKEN']
    except KeyError:
        try:
            # Pythonista for iOS
            import keychain
        except ImportError:
            import keyring as keychain

        user = keychain.get_password('pushover', 'user')
        api_token = keychain.get_password('pushover', 'api_token')
    return user, api_token


def push(message, user: str = None, api_token: str = None, device: str = None,
         title: str = None, url: str = None, url_title: str = None,
         priority: str = None, timestamp: str = None, sound: str = None) \
                 -> typing.Union[http.client.HTTPResponse, typing.BinaryIO]:
    """Pushes the notification.

    API Reference: https://pushover.net/api

    Args:
        message: Your message
        user: The user/group key (not e-mail address) of your user (or you),
              viewable when logged into our dashboard (often referred to as
              USER_KEY in our documentation and code examples)
        api_token: Your application's API token
        device: Your user's device name to send the message directly to that
                device, rather than all of the user's devices
        title: Your message's title, otherwise your app's name is used
        url: A supplementary URL to show with your message
        url_title: A title for your supplementary URL, otherwise just the URL
                   is shown
        priority: Send as:1 to always send as a quiet notification, 1 to
                  display as high--priority and bypass the user's quiet
                  hours, or 2 to also require confirmation from the user
        timestamp: A Unix timestamp of your message's date and time to
                   display to the user, rather than the time your message is
                   received by our API
        sound: The name of one of the sounds supported by device clients to
               override the user's default sound choice

    Returns:
        HTTP response from API call
    """
    if user is None or api_token is None:
        user, api_token = get_credentials()

    api_url = 'https://api.pushover.net/1/messages.json'

    if title is None:
        if getattr(__main__, "__file__", None):
            title = os.path.basename(__main__.__file__)
        else:
            title = "n8scripts"

    payload_dict = {
        'token': api_token,
        'user': user,
        'message': message,
        'device': device,
        'title': title,
        'url': url,
        'url_title': url_title,
        'priority': priority,
        'timestamp': timestamp,
        'sound': sound
    }
    payload = urllib.parse.urlencode(
            {k: v for k, v in payload_dict.items() if v})

    with urllib.request.urlopen(api_url, data=payload.encode()) as resp:
        return resp


def cli() -> None:
    """Collect command line args and run push."""
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            argument_default=argparse.SUPPRESS)
    parser.add_argument('message', help="Your message")
    parser.add_argument('-u', '--user',
                        help=("The user/group key (not e-mail address) of "
                              "your user (or you)"))
    parser.add_argument('-a', '--api-token',
                        help="Your application's API token")
    parser.add_argument('-d', '--device',
                        help=("Your user's device name to send the message "
                              "directly to that device, rather than all of "
                              "the user's devices (multiple devices may be "
                              "separated by a comma)"))
    parser.add_argument('-t', '--title',
                        help=("Your message's title, otherwise your app's "
                              "name is used"))
    parser.add_argument('-k', '--url',
                        help="A supplementary URL to show with your message")
    parser.add_argument('-l', '--url_title',
                        help=("A title for your supplementary URL, otherwise "
                              "just the URL is shown"))
    parser.add_argument('-p', '--priority',
                        help=("Send as -2 to generate no notification/alert, "
                              "-1 to always send as a quiet notification, 1 "
                              "to display as high-priority and bypass the "
                              "user's quiet hours, or 2 to also require "
                              "confirmation from the user"))
    parser.add_argument('-m', '--timestamp',
                        help=("A Unix timestamp of your message's date and "
                              "time to display to the user, rather than the "
                              "time your message is received by our API"))
    parser.add_argument('-s', '--sound',
                        help=("The name of one of the sounds supported by "
                              "device clients to override the user's default "
                              "sound choice"))
    namespace = parser.parse_args()
    args = {k: v for k, v in vars(namespace).items() if v}
    push(**args)


if __name__ == '__main__':
    cli()
