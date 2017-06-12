"""Rolca frontend settings."""
# pylint: disable=invalid-name
from django.conf import settings


frontend_color = getattr(settings, 'ROLCA_FRONTEND_COLOR', 'orange')
frontend_title = getattr(settings, 'ROLCA_FRONTEND_TITLE', 'Rolca')
