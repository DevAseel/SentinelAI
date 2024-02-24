import sys
import time
from transformers import AutoModelForObjectDetection
import torch
from torchvision import transforms
from PIL import Image
from utils.logger import setup_logging
from utils.img_processing import MaxResize, outputs_to_objects
import logging
import json
import os
from args.tables_scanner_args import parse_args


class TablesScanner:
    def __init__(
        self,
        img_path,
        model_name="microsoft/table-transformer-detection",
        json=False,
        json_path="./outputs/scanned_tables_json",
    ):
        self.img_path = img_path
        self.model_load_time = 0
        self.model_name = model_name
        self.model = self.load_model()
        self.json = json
        self.json_path = json_path

    def load_model(self):
        start_time = time.time()
        logging.info("✨ Sentinel Tables Scanner is starting...")
        try:
            model = AutoModelForObjectDetection.from_pretrained(
                self.model_name, revision="no_timm"
            )
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model.to(device)
            end_time = time.time()
            self.model_load_time = end_time - start_time

            logging.debug("✔️  Model loaded.")
            return model

        except KeyboardInterrupt:
            logging.critical("\nExiting...")
            sys.exit(0)

        except Exception as e:
            logging.error(f"There was an error when loading the model: {e}")
            # Handle the exception as needed, e.g., return a default model or re-raise the exception
            raise e

    def scan_tables(self):
        start_time = time.time()
        try:
            image = Image.open(self.img_path).convert("RGB")

            logging.debug("✔️  Image loaded.")

            width, height = image.size

            transform = transforms.Compose(
                [
                    MaxResize(800),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
                ]
            )

            pixel_values = transform(image).unsqueeze(0)
            pixel_values = pixel_values.to(self.model.device)

            with torch.no_grad():
                outputs = self.model(pixel_values)

            id2label = self.model.config.id2label
            id2label[len(id2label)] = "no object"
            objects = outputs_to_objects(outputs, image.size, id2label)

            end_time = time.time()
            elapsed_time = end_time - start_time

            output = {
                "tables detected": len(objects),
                "model load time": f"{self.model_load_time:.2f}s",
                "process duration": f"{elapsed_time:.2f}s",
                "data": objects,
            }
            if json:
                image_name, image_ext = os.path.splitext(
                    os.path.basename(self.img_path)
                )

                os.makedirs(self.json_path, exist_ok=True)

                with open(f"{self.json_path}/{image_name}.json", "w") as json_file:
                    json.dump(output, json_file, indent=4)

                logging.debug(f"✔️  json file created")

            logging.info(f"{json.dumps(output, indent=2)}")

            return output

        except KeyboardInterrupt:
            logging.critical("\nExiting...")
            sys.exit(0)

        except Exception as e:
            logging.error(f"There was an issue when scanning for tables: {e}")
            raise e


if __name__ == "__main__":
    args = parse_args()

    # Set up logging based on the command-line argument
    setup_logging(args.log_level)

    # Example usage:
    table_detector = TablesScanner(args.img_path)
    table_detector.scan_tables()
