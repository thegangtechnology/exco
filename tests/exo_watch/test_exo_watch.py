import time

from exco.exco_watch import ExcoWatch, ExcoWatchHandler
from unittest.mock import patch
from os.path import join, dirname


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
    s = handler.on_modified(None)
    out, err = capfd.readouterr()
    print(s)
    print(out)
    print(err)
    assert 'Latest' in out
