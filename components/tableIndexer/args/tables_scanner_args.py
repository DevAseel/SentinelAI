import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Detect tables in an image using a pre-trained object detection model."
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
        help="Specify the path to the input image",
    )
    parser.add_argument(
        "--model-name",
        dest="the name of the model to load to be used for table detection",
        default="microsoft/table-transformer-detection",
        help="Set the table detection model",
    )
    parser.add_argument(
        "--json",
        dest="save the output as a json file",
        action="store_true",
        help="set the json output preference",
    )
    parser.add_argument(
        "--json-path",
        dest="specify the json path",
        default="./outputs/scanned_tables_json",
        help="set the output path of the json file",
    )

    return parser.parse_args()
