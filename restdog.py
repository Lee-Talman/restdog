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
    format="%(asctime)s : %(message)s",
)


def clone_directory(source, dest, max_length, file_types):
    global logger

    if not os.path.exists(dest):
        os.makedirs(dest)
        logger.info(f"Cloned directory: {dest}")

    for file in os.listdir(source):
        source_file = os.path.join(source, file)
        dest_file = os.path.join(dest, file)
        if os.path.isdir(source_file):
            clone_directory(source_file, dest_file, max_length, file_types)
            logger.info(f"Cloned directory: {dest_file}")
        elif any(source_file.endswith(ext) for ext in file_types):
            shutil.copy2(source_file, dest_file)
            # Truncate file name and move to new path (only works on Windows!)
            file_basename = os.path.basename(source_file)
            file_name, file_ext = os.path.splitext(file_basename)
            if len(file_name) > max_length:
                file_name = file_name[:max_length]
                file_name = file_name.rstrip()
                file_name = file_name.replace(" ", "_")
                file_name_short = file_name + file_ext
                dest_short = os.path.join(dest, file_name_short)
                shutil.move(dest_file, dest_short)
                logger.info(f"Cloned file: {source_file} to {dest_short}")
            else:
                logger.info(f"Cloned file: {source_file} to {dest}")
            

def main(source, dest, interval, max_length, file_types):
    global logger

    while True:
        start = f"Cloning files from {source} to {dest}"
        print(start)
        logger.info(start)
        clone_directory(source, dest, max_length, file_types)

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
    parser.add_argument("--max_length", type=int, default=24, help="Maximum file name length (default: 24)")
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

    main(args.source, args.dest, args.interval, args.max_length, args.file_types)
