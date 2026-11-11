import pytest

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="session")
def brower_context_args(brower_context_args):
    return {
        **brower_context_args,
        "viewport": {"width": 1280, "height": 800},
            }

@pytest.fixture
def app_base_url():
    return BASE_URL 
