from utils.logger import setup_logging
import logging
import json
import sys
import os
from args.json_to_markdown_convertor_args import parse_args


def json_to_markdown_table(json_path, output_dir="./outputs/markdown"):
    logging.info("✨ Sentinel JSON to Markdown Convertor is starting...")

    # Load json file
    try:
        with open(json_path, "r") as json_file:
            data = json.load(json_file)
    except Exception as e:
        logging.error(f"There was an issue when loading the json file: {e}")
        sys.exit(1)

    # Find the maximum number of columns
    if not data:
        return

    max_columns = max(len(row) for row in data.values())
    # Create header row
    header = f"| {' | '.join(data['0'])} |\n"
    separator = f"| {' | '.join(['---'] * max_columns)} |\n"

    # Create data rows
    rows = []
    for idx in range(1, len(data)):
        row = f"| {' | '.join(data[str(idx)])} |\n"
        rows.append(row)

    markdown = header + separator + "".join(rows)

    # Check if the output directory exists, create it if not
    os.makedirs(output_dir, exist_ok=True)

    # Build the full path for the output Markdown file using the input JSON file name
    json_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_md_path = os.path.join(output_dir, f"{json_filename}.md")

    # Write the markdown to the specified output file
    try:
        with open(output_md_path, "w") as output_file:
            output_file.write(markdown)
        logging.debug(f"Markdown content saved to {output_md_path}")
    except Exception as e:
        logging.error(f"There was an issue when saving the Markdown content: {e}")
        sys.exit(1)

    logging.info(markdown)


if __name__ == "__main__":
    args = parse_args()

    # Set up logging based on the command-line argument
    setup_logging(args.log_level)

    # Example usage:
    table_detector = json_to_markdown_table(args.json_path)
