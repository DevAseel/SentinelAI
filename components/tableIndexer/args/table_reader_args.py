import argparse


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
        "--json",
        dest="save the output as a json file",
        action="store_true",
        help="set the json output preference",
    )
    parser.add_argument(
        "--output-path",
        dest="specify the json path",
        default="./outputs/parsed_tables_json",
        help="set the output path of the json file",
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        default="info",
        help="Set the logging level (debug, info, warning, error, critical)",
        choices=["debug", "info", "warning", "error", "critical"],
    )

    return parser.parse_args()
