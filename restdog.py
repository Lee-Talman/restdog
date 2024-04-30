import argparse
import logging
import os
import shutil
import time

import requests
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers.polling import PollingObserver

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="restdog.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s : %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


class Handler(PatternMatchingEventHandler):
    def __init__(self, src_dir, dest_dir, api, patterns, ignore_directories=True, case_sensitive=False) -> None:
        super().__init__(patterns=patterns)
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        self.api = api

        global logger
        logger.info("WATCH: %s", self.src_dir)

    def get_file_info(self, src_path):
        file_name = os.path.basename(src_path)
        dest_path = os.path.join(self.dest_dir, file_name)
        return file_name, dest_path

    def copy_file(self, src_path, event_type):
        file_name, dest_path = self.get_file_info(src_path)
        shutil.copy(src_path, dest_path)

        # global logger
        logger.info("FILE %s: COPY %s TO %s", event_type, file_name, self.dest_dir)

    def send_file(self, src_path, request_type):
        file_name, dest_path = self.get_file_info(src_path)
        with open(src_path, "rb") as file:
            files = {"file": (file_name, file)}
            if request_type == "POST":
                response = requests.post(self.dest_dir, files=files)
            if request_type == "PUT":
                response = requests.put(self.dest_dir, files=files)
            if request_type == "DELETE":
                response = requests.delete(self.dest_dir, params={"file_path": dest_path})

            # global logger
            logger.info("%s REQUEST FOR %s RETURNED %s", request_type, file_name, requests.status_code)

    def delete_file(self, src_path):
        file_name, dest_path = self.get_file_info(src_path)
        if os.path.exists(dest_path):
            os.remove(dest_path)

            # global logger
            logger.info("FILE DELETED %s FROM %s", file_name, self.dest_dir)

    def on_created(self, event):
        if self.api:
            self.send_file(event.src_path, "POST")
        else:
            self.copy_file(event.src_path, "CREATED")

    def on_modified(self, event):
        if self.api:
            self.send_file(event.src_path, "PUT")
        else:
            self.copy_file(event.src_path, "MODIFIED")

    def on_deleted(self, event):
        if self.api:
            self.send_file(event.src_path, "DELETE")
        else:
            self.delete_file(event.src_path)


def parseArgs():
    parser = argparse.ArgumentParser("Duplicate file modifications to a local directory, or over the web via REST API.")
    parser.add_argument("src_dir", type=str, help="local source directory to watch files")
    parser.add_argument("dest_dir", type=str, help="local destination directory or API endpoint")
    parser.add_argument("--api", action="store_true", default=False, help="send to an API endpoint (default: False)")
    parser.add_argument("--interval", type=int, help="update interval in seconds (default: 3600)")
    parser.add_argument(
        "--file_types",
        type=str,
        nargs="+",
        default=["*.csv", "*.xls", "*.xlsx", "*.xlsm"],
        help="whitespace-separated list of watched file types (default: *.csv *.xls *.xlsx *.xlsm)",
    )
    return parser.parse_args()


def watch():
    args = parseArgs()
    event_handler = Handler(src_dir=args.src_dir, dest_dir=args.dest_dir, api=args.api, patterns=args.file_types)
    observer = PollingObserver()
    observer.schedule(event_handler, path=args.src_dir, recursive=True)
    observer.start()
    print("restdog started - check restdog.log for in-depth logging.")

    try:
        while True:
            time.sleep(args.interval)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    watch()
