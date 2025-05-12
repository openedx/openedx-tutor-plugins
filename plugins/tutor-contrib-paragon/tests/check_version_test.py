"""
Tutor paragon plugin tests
"""

from tutorparagon import __about__

def test_version_exists():
    assert hasattr(__about__, "__version__")
    assert isinstance(__about__.__version__, str)
    assert __about__.__version__ != ""
