import argparse
import os
import time
from datetime import datetime, timedelta
from os.path import dirname
from pprint import pprint
from traceback import print_exc

import exco
from exco.exception import ExcoException
from watchdog.events import FileSystemEventHandler


class ExcoWatchHandler(FileSystemEventHandler):
    def __init__(self, path: str):
        super().__init__()
        self.path = path
        self.last_modified = self._last_fmod()  # pattern matching event doesn't work with OSX's FSEvent
        self.last_output = datetime.now()

    def _last_fmod(self):
        return os.path.getmtime(self.path)

    def run_exco(self):
        try:
            processor = exco.from_excel(self.path)
            result = processor.process_excel(self.path)
            pprint(result.to_dict())
        except (ExcoException, TypeError, LookupError, ValueError, AttributeError):
            print_exc()
        finally:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f'Latest Result At: {current_time}')

    def on_modified(self, event):
        if datetime.now() - self.last_output < timedelta(seconds=1):
            return False
        else:
            self.last_output = datetime.now()

        last_fmod = self._last_fmod()  # need this for osx :s
        if last_fmod > self.last_modified:
            self.run_exco()
        return True


class ExcoWatch:

    @classmethod
    def main(cls):

        parser = argparse.ArgumentParser(description='Continuously Watch Template and Output.')
        parser.add_argument('path', type=str,
                            help='Path to template file')

        args = parser.parse_args()
        cls.run(args.path)

    @classmethod
    def run(cls, path: str):
        """Continuously Watch and print template result to std out

            path: str
        """

        from watchdog.observers import Observer
        event_handler = ExcoWatchHandler(path=path)
        observer = Observer()
        observer.schedule(event_handler, dirname(path), recursive=True)
        event_handler.run_exco()
        observer.start()

        try:
            while True:
                time.sleep(1)
        except (InterruptedError, KeyboardInterrupt):
            print('Quitting...')
        finally:
            observer.stop()
            observer.join()
