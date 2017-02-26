# coding: utf-8

import os
from django.conf import settings

# Admin Site Title
ADMIN_TITLE = getattr(settings, "FERRAMENTAS_ADMIN_TITLE", 'Sistema sispag')

# Admin Prefix
ADMIN_URL = getattr(settings, "FERRAMENTAS_ADMIN_URL", 'admin')

