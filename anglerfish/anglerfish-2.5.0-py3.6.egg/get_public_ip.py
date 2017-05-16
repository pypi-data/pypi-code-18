#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Get current public IP as string."""


from ipaddress import ip_address
from urllib.request import urlopen


def get_public_ip():
    """Get current public IP as string."""
    return ip_address(urlopen("https://api.ipify.org").read().decode("utf-8"))


def is_online():
    """Check if we got internet conectivity."""
    try:
        get_public_ip()
    except Exception:
        return False
    else:
        return True
