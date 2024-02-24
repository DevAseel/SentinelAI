import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert PDF to Images with logging level control."
    )
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
    parser.add_argument(
        "--output-directory",
        dest="output_directory",
        default="./outputs/images",
        help="Specify the output directory for images",
    )
    return parser.parse_args()
