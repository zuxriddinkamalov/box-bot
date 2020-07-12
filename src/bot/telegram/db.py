import os
import sys
import django
from django.core.paginator import Paginator

from aiogram.types import InputFile

import traceback

proj_path = os.path.join(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
proj_path = os.path.join(os.path.split(proj_path)[0], 'engine')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "engine.settings")
sys.path.append(proj_path)

django.setup()

import core.models as core_models
import telegram.models as telegram_models
