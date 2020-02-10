import pytest
import responses as rsps

import pypokedex


@pytest.fixture
def responses():
    pypokedex.get.cache_clear()
    with rsps.RequestsMock() as requests_mock:
        yield requests_mock
