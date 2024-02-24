import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Extract and parse tables from pdfs.")
    parser.add_argument(
        "--log-level",
        dest="log_level",
        default="info",
        help="Set the logging level (debug, info, warning, error, critical)",
        choices=["debug", "info", "warning", "error", "critical"],
    )
    parser.add_argument(
        "--pdf-name", dest="pdf_name", required=True, help="Specify the PDF file name"
    )
    return parser.parse_args()
