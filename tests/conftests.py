import pytest
from main import create_app


@pytest.fixture
def app():
    app, api = create_app()
    return app
