import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Crop tables in an image based on detected objects."
    )
    parser.add_argument(
        "--img-path",
        dest="img_path",
        required=True,
        help="Specify the path to the input image",
    )
    parser.add_argument(
        "--tokens",
        dest="tokens",
        default=[],
        help="Specify tokens for cropping",
    )
    parser.add_argument(
        "--class-thresholds",
        dest="class_thresholds",
        default={"table": 0.5, "table rotated": 0.5, "no object": 10},
        help="Specify class thresholds",
    )
    parser.add_argument(
        "--padding",
        dest="padding",
        type=int,
        default=10,
        help="Specify padding for cropping",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default="./outputs/tables/",
        help="Specify the output directory for cropped tables",
    )
    parser.add_argument(
        "--json-path",
        dest="json_path",
        required=True,
        help="Specify the path of the json file containing the scan results",
    )

    parser.add_argument(
        "--log-level",
        dest="log_level",
        default="info",
        help="Set the logging level (debug, info, warning, error, critical)",
        choices=["debug", "info", "warning", "error", "critical"],
    )

    return parser.parse_args()
