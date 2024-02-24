import os
from utils.table_processing import get_cell_coordinates_by_row, apply_ocr
import easyocr
import sys
import json
import logging
from utils.logger import setup_logging
from args.table_reader_args import parse_args


def table_reader(
    img_path, json_path, languages=["en"], output_path="./outputs/parsed_tables"
):
    try:
        logging.info("✨ Sentinel Table Reader has started...")

        reader = easyocr.Reader(languages)

        logging.debug("✔️  EasyOCR Model loaded.")
        logging.debug(f"🟡 Model Language: {languages}")

        # load json file
        with open(json_path, "r") as json_file:
            cells = json.load(json_file)
            logging.debug("✔️ JSON file loaded")

        cell_coordinates = get_cell_coordinates_by_row(cells)

        # this needs to run only once to load the model into memory
        data = apply_ocr(img_path, cell_coordinates, reader)

        # save output as a json file
        if json:
            image_name, image_ext = os.path.splitext(os.path.basename(img_path))

            os.makedirs(output_path, exist_ok=True)

            with open(f"{output_path}/{image_name}.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

            logging.debug(f"✔️  json file created.")

        for row_data in data.values():
            logging.info(row_data)

    except FileNotFoundError as e:
        logging.error(f"file was not found: {e}")

    except KeyboardInterrupt:
        logging.critical("\nExiting...")
        sys.exit(0)

    except Exception as e:
        logging.error(f"There was an issue when reading table: {e}")
        raise e


if __name__ == "__main__":
    args = parse_args()

    # Set up logging based on the command-line argument
    setup_logging(args.log_level)

    # Example usage:
    table_reader(args.img_path, args.json_path, args.languages)
