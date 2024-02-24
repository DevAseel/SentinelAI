from pdf_to_images_converter import convert_pdf_to_images
from tables_scanner import TablesScanner
from tables_marker import TableMarker
from tables_cropper import TableCropper
from table_constructor import table_constructor
from table_reader import table_reader
from json_to_markdown_convertor import json_to_markdown_table
from utils.logger import setup_logging
import logging
import argparse
import sys
from config import SETTINGS


def parse_args():
    parser = argparse.ArgumentParser(description="Extract and parse tables from pdfs.")
    parser.add_argument(
        "--log-level",
        dest="log_level",
        default="INFO",
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    parser.add_argument(
        "--pdf-name", dest="pdf_name", required=True, help="Specify the PDF file name"
    )
    return parser.parse_args()


def main(pdf_name):
    try:
        # start by converting pdf to images and saving the number of pages
        number_of_pages = convert_pdf_to_images(pdf_name)

        # start scanning for tables
        number_of_tables_detected = 0
        scanned_tables_data = []
        for i in range(number_of_pages):
            # instantiate the tables scanner class
            tables_scanner = TablesScanner(
                img_path=f"./outputs/images/{pdf_name}_page_{i+1}.png",
                model_name=SETTINGS.table_detection_model_repository,
                json=True,
            )
            scanning_results = tables_scanner.scan_tables()
            number_of_tables = scanning_results["tables detected"]

            for data in scanning_results["data"]:
                if data["score"] >= SETTINGS.table_detection_score_threshold:
                    scanned_tables_data.append(
                        {"page_number": i + 1, "number_of_tables": number_of_tables}
                    )
                    number_of_tables_detected += 1

        # start marking tables
        for table_data in scanned_tables_data:
            # instantiate the table marker class
            TableMarker(
                img_path=f"./outputs/images/{pdf_name}_page_{table_data['page_number']}.png",
                json_path=f"./outputs/scanned_tables_json/{pdf_name}_page_{table_data['page_number']}.json",
            ).visualize_detected_tables()

            # start cropping the marked tables
            TableCropper(
                img_path=f"./outputs/images/{pdf_name}_page_{table_data['page_number']}.png",
                json_path=f"./outputs/scanned_tables_json/{pdf_name}_page_{table_data['page_number']}.json",
                padding=SETTINGS.table_crop_padding,
            ).apply()

            for j in range(table_data["number_of_tables"]):
                # construct each table for each pdf
                table_constructor(
                    img_path=f"./outputs/tables/{pdf_name}_page_{table_data['page_number']}_cropped_table_{j}.png",
                    model_name=SETTINGS.table_transformer_model_repository,
                    device=SETTINGS.device_type,
                    json=True,
                )
                # read each table
                table_reader(
                    img_path=f"./outputs/tables/{pdf_name}_page_{table_data['page_number']}_cropped_table_{j}.png",
                    json_path=f"./outputs/constructed_tables_json/{pdf_name}_page_{table_data['page_number']}_cropped_table_{j}.json",
                    languages=SETTINGS.table_reader_languages,
                )
                # save as markdown
                json_to_markdown_table(
                    json_path=f"./outputs/parsed_tables/{pdf_name}_page_{table_data['page_number']}_cropped_table_{j}.json"
                )

    except KeyboardInterrupt:
        logging.critical("\nExiting...")
        sys.exit(0)

    except Exception as e:
        logging.error(f"there was an error processing the pdf: {e}")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()

    # set up colorful logging based on the command-line argument
    setup_logging(args.log_level.upper())

    main(pdf_name=args.pdf_name)
