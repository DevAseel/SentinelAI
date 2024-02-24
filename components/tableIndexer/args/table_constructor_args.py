import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Construct tables by defining rows for detected tables."
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
        help="Specify the path of the cropped table",
    )
    parser.add_argument(
        "--model-name",
        dest="model_name",
        default="microsoft/table-structure-recognition-v1.1-all",
        help="Specify the path of the cropped table",
    )
    parser.add_argument(
        "--device",
        dest="device",
        default="cpu",
        help="Specify the device type to load the model (cpu, cuda, mkldnn, opengl, opencl, ideep, hip, msnpu",
        choices=["cpu", "cuda", "mkldnn", "opengl", "opencl", "ideep", "hip", "msnpu"],
    )
    parser.add_argument(
        "--output-directory",
        dest="output_directory",
        default="./outputs/constructed_tables",
        help="Specify the output directory for images",
    )
    parser.add_argument(
        "--json", dest="json", action="store_true", help="Save output as a json file"
    )
    parser.add_argument(
        "--json-path",
        dest="json_path",
        default="./outputs/constructed_tables_json",
        help="output directory for the json file",
    )
    return parser.parse_args()
