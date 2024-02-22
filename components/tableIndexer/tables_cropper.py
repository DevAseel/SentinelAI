import argparse
from PIL import Image
import os
import logging
import sys
import json
from utils.logger import setup_logging


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
        default="INFO",
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    return parser.parse_args()


class TableCropper:
    def __init__(
        self,
        img_path,
        json_path,
        tokens=[],
        class_thresholds={"table": 0.5, "table rotated": 0.5, "no object": 10},
        padding=10,
        output_dir="./outputs/tables",
    ):
        self.img_path = img_path
        self.json_path = json_path
        self.tokens = tokens
        self.class_thresholds = class_thresholds
        self.padding = padding
        self.output_dir = output_dir

    def crop_table(self, objects):
        try:
            logging.info("✨ Sentinel Table Cropper has started...")
            table_crops = []
            for obj in objects:
                if obj["score"] < self.class_thresholds[obj["label"]]:
                    continue

                cropped_table = {}

                bbox = obj["bbox"]
                bbox = [
                    bbox[0] - self.padding,
                    bbox[1] - self.padding,
                    bbox[2] + self.padding,
                    bbox[3] + self.padding,
                ]
                image = Image.open(self.img_path).convert("RGB")
                cropped_img = image.crop(bbox)

                table_tokens = [
                    token
                    for token in self.tokens
                    if self.iob(token["bbox"], bbox) >= 0.5
                ]
                for token in table_tokens:
                    token["bbox"] = [
                        token["bbox"][0] - bbox[0],
                        token["bbox"][1] - bbox[1],
                        token["bbox"][2] - bbox[0],
                        token["bbox"][3] - bbox[1],
                    ]

                # If table is predicted to be rotated, rotate cropped image and tokens/words:
                if obj["label"] == "table rotated":
                    cropped_img = cropped_img.rotate(270, expand=True)
                    for token in table_tokens:
                        bbox = token["bbox"]
                        bbox = [
                            cropped_img.size[0] - bbox[3] - 1,
                            bbox[0],
                            cropped_img.size[0] - bbox[1] - 1,
                            bbox[2],
                        ]
                        token["bbox"] = bbox

                cropped_table["image"] = cropped_img
                cropped_table["tokens"] = table_tokens

                table_crops.append(cropped_table)

            return table_crops
        except KeyboardInterrupt:
            logging.critical("\nExiting...")
            sys.exit(0)
        except Exception as e:
            logging.error(f"There was an issue when cropping tables: {e}")
            raise e

    def iob(self, bbox1, bbox2):
        # Implement your IOB (Intersection over Bounding Box) calculation here
        # This function is a placeholder and should be replaced with the actual calculation
        pass

    def apply(self):
        # load json file
        if os.path.exists(self.json_path):
            with open(self.json_path, "r") as json_file:
                det_tables = json.load(json_file)
                logging.debug("✔️ JSON file loaded")
        else:
            logging.error(f"File not found: {self.json_path}")
            sys.exit(1)

        tables_crops = self.crop_table(det_tables["data"])

        # Provide a file path for save, not just a directory
        os.makedirs(self.output_dir, exist_ok=True)

        for index, table in enumerate(tables_crops):
            cropped_table = table["image"].convert("RGB")
            # Save with a unique filename based on the index
            file_name = os.path.splitext(os.path.basename(self.img_path))[0]
            output_filename = f"{file_name}_cropped_table_{index}.png"
            output_path = os.path.join(self.output_dir, output_filename)
            cropped_table.save(output_path)

        logging.info("✔️ Table cropped. output: {}".format(self.output_dir))


if __name__ == "__main__":
    args = parse_args()

    # Set up logging based on the command-line argument
    setup_logging(args.log_level.upper())

    # Example usage:
    table_cropper = TableCropper(
        args.img_path, args.json_path, args.tokens, args.class_thresholds, args.padding
    )

    table_cropper.apply()
