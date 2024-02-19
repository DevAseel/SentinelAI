import argparse
from utils.logger import setup_logging
import logging
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert parsed table from json format to markdown format"
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        default="INFO",
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    parser.add_argument(
        "--json-path",
        dest="json_path",
        required=True,
        help="Set the path of the parsed json table",
    )

    return parser.parse_args()


def json_to_markdown_table(json_path):
    logging.info("✨ Sentinel JSON to Markdown Convertor is starting...")

    # Load json file
    try:
        with open(json_path, "r") as json_file:
            data = json.load(json_file)
    except Exception as e:
        logging.error(f"There was an issue when loading the json file: {e}")
        sys.exit(1)

    # Find the maximum number of columns
    max_columns = max(len(row) for row in data.values())

    # Create header row
    header = "| " + " | ".join(data["0"]) + " |\n"
    separator = "| " + " | ".join(["---"] * max_columns) + " |\n"

    # Create data rows
    rows = ""
    for idx in range(1, len(data)):
        rows += "| " + " | ".join(data[str(idx)]) + " |\n"

    markdown = header + separator + rows

    logging.info(markdown)

    return markdown


if __name__ == "__main__":
    args = parse_args()

    # Set up logging based on the command-line argument
    setup_logging(args.log_level.upper())

    # Example usage:
    table_detector = json_to_markdown_table(args.json_path)
