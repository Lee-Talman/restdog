import logging
import os
import shutil
import time
import argparse

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="restdog.log",
    filemode="a",
    level=logging.INFO,
    format='%(asctime)s : %(message)s',
)

def clone_directory(source, dest, file_types):
    global logger

    if not os.path.exists(dest):
        os.makedirs(dest)
        logger.info(f"Cloned directory: {dest}")

    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        dest_item = os.path.join(dest, item)
        if os.path.isdir(source_item):
            clone_directory(source_item, dest_item, file_types)
            logger.info(f"Cloned directory: {dest_item}")
        elif any(source_item.endswith(ext) for ext in file_types):
            shutil.copy2(source_item, dest_item)
            # Truncate item name and move to new path
            dest_trunc = os.path.join(dest, truncate(item, 18))
            shutil.move(dest_item, dest_trunc)
            logger.info(f"Cloned file: {source_item} to {dest_trunc}")

def truncate(item, max_length):
    # Truncate longer item names and replace whitepace with underscores
    if len(item) > max_length:
        item = item.replace(' ', '_')
        item = item[:max_length]
    return item

def main(source, dest, interval, file_types):
    global logger

    while True:
        start = f"Cloning files from {source} to {dest}"
        print(start)
        logger.info(start)
        clone_directory(source, dest, file_types)

        wait = f"Waiting for {interval} seconds before next clone."
        print(wait)
        logger.info(wait)

        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Duplicate file modifications to a local directory, or over the web via REST API.")
    parser.add_argument("source", type=str, help="local source directory to watch files")
    parser.add_argument("dest", type=str, help="local destination directory or API endpoint")
    # parser.add_argument("--api", action="store_true", default=False, help="send to an API endpoint (default: False)")
    parser.add_argument("--interval", type=int, default=1800, help="update interval in seconds (default: 1800)")
    parser.add_argument(
        "--file_types",
        type=str,
        nargs="+",
        default=[".csv", ".xls", ".xlsx", ".xlsm"],
        help="whitespace-separated list of watched file types (default: .csv .xls .xlsx .xlsm)",
    )

    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"Source path {args.source} does not exist.")
        exit(1)
    if not os.path.isdir(args.source):
        print(f"Source path {args.source} is not a directory.")
        exit(1)

    main(args.source, args.dest, args.interval, args.file_types)