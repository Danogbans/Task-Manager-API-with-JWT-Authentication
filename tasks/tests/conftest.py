import os
import django
import pytest
from django.conf import settings

@pytest.fixture(scope="session", autouse=True)
def setup_django():
    """Ensures Django is set up before running tests."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
    django.setup()