import os
from utils.table_processing import get_cell_coordinates_by_row, apply_ocr
import easyocr
import sys
import json
import logging
import argparse
from utils.logger import setup_logging


def parse_args():
    parser = argparse.ArgumentParser(
        description="read the content of the table by passing the json file which contains the cells details"
    )
    parser.add_argument(
        "--img-path",
        dest="img_path",
        required=True,
        help="Specify the path to the input image",
    )
    parser.add_argument(
        "--json-path",
        dest="json_path",
        required=True,
        help="Specify the path of the json file containing the cells result",
    )
    parser.add_argument(
        "--languages",
        dest="languages",
        nargs="+",
        default=["en"],
        help="an array of langauges that has to be supported to read the document. Example: ['en']",
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        default="INFO",
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    return parser.parse_args()


def table_reader(img_path, json_path, languages=["en"]):
    try:
        reader = easyocr.Reader(languages)

        # load json file
        if os.path.exists(json_path):
            try:
                with open(json_path, "r") as json_file:
                    cells = json.load(json_file)
                    logging.debug("✔️ JSON file loaded")

            except Exception as e:
                logging.error(f" There was an error loading the json file: {e}")
                sys.exit(1)

        else:
            logging.error(f"File not found: {json_path}")
            sys.exit(1)

        cell_coordinates = get_cell_coordinates_by_row(cells)
        # this needs to run only once to load the model into memory

        data = apply_ocr(img_path, cell_coordinates, reader)

        for row, row_data in data.items():
            logging.info(row_data)

    except KeyboardInterrupt:
        logging.critical("\nExiting...")
        sys.exit(0)

    except Exception as e:
        logging.error(f"There was an issue when reading table: {e}")
        raise e


if __name__ == "__main__":
    args = parse_args()

    # Set up logging based on the command-line argument
    setup_logging(args.log_level.upper())

    # Example usage:
    table_reader(args.img_path, args.json_path, args.languages)
