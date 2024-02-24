import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Mark tables in an image using the json file generated from table_scanner method"
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        default="info",
        help="Set the logging level (debug, info, warning, error, critical)",
        choices=["debug", "info", "warning", "error", "critical"],
    )
    parser.add_argument(
        "--img-path",
        dest="img_path",
        required=True,
        help="Specify the path of the image which contains the table you want to mark",
    )
    parser.add_argument(
        "--json-path",
        dest="json_path",
        required=True,
        help="set the path of the json file containing marking information from table_scanner method",
    )
    parser.add_argument(
        "--output-path",
        dest="output_path",
        default="./outputs/marked_tables",
        help="set the output path for the marked image",
    )
    return parser.parse_args()
