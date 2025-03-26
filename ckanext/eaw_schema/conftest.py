import pytest
import requests

def pytest_addoption(parser):
    parser.addoption(
        "--no-skips", action="store_true", default=False, help="disable skip marks"
    )

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if config.getoption("--no-skips"):
        # Disable skip marks
        def no_skip(*args, **kwargs):
            return

        # Replacing the skip function with the no-op function
        pytest.skip = no_skip

@pytest.fixture
def request_code():
    def _request_code(url):
        return requests.get(url).status_code

    return _request_code
