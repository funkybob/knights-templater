import pathlib

import pytest

from knights.loader import TemplateLoader


@pytest.fixture(scope='module')
def test_loader() -> TemplateLoader:
    return TemplateLoader(
        [
            pathlib.Path(__file__).parent / 'templates',
        ],
    )
