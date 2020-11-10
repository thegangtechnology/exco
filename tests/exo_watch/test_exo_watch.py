import time

from exco.exco_watch import ExcoWatch, ExcoWatchHandler
from unittest.mock import patch
from os.path import join, dirname
import sys


@patch("time.sleep", side_effect=InterruptedError)
def test_exo_watch(mocked_sleep, capfd):
    # given
    fname = join(dirname(__file__), '../../sample/test/everything/everything_template.xlsx')
    ExcoWatch.run(path=fname)
    out, _ = capfd.readouterr()
    assert 'Quitting' in out


def test_handler(capfd):
    fname = join(dirname(__file__), '../../sample/test/everything/everything_template.xlsx')
    handler = ExcoWatchHandler(path=fname)
    time.sleep(1.1)
    handler.on_modified(None)
    out, err = capfd.readouterr()
    assert 'Latest' in out


def test_handler_double_fire(capfd):
    """Firing handler right after creation should not create output"""
    fname = join(dirname(__file__), '../../sample/test/everything/everything_template.xlsx')
    handler = ExcoWatchHandler(path=fname)
    handler.on_modified(None)
    out, err = capfd.readouterr()
    assert 'Latest' not in out


def test_handler_bad_input(capfd):
    fname = join(dirname(__file__), '../../sample/test/bad_template.xlsx')
    handler = ExcoWatchHandler(path=fname)
    time.sleep(1.1)
    handler.on_modified(None)
    out, err = capfd.readouterr()
    assert 'B10' in err


@patch("time.sleep", side_effect=InterruptedError)
def test_main(mocked_sleep, capfd):
    fname = join(dirname(__file__), '../../sample/test/everything/everything_template.xlsx')
    with patch.object(sys, 'argv', ['exo_watch', fname]):
        ExcoWatch.main()
        out, err = capfd.readouterr()
        assert 'Quitting' in out
