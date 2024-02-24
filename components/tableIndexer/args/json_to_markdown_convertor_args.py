import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert parsed table from json format to markdown format"
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        default="info",
        help="Set the logging level (debug, info, warning, error, critical)",
        choices=["debug", "info", "warning", "error", "critical"],
    )

    parser.add_argument(
        "--json-path",
        dest="json_path",
        required=True,
        help="Set the path of the parsed json table",
    )

    return parser.parse_args()
