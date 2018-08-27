import sys
import pytest


def run_tests():
    exitcode = pytest.main(["tests.py"])
    if exitcode:
        sys.exit(exitcode)


if __name__ == "__main__":
    run_tests()
