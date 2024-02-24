from transformers import TableTransformerForObjectDetection
import torch
from torchvision import transforms
from PIL import Image, ImageDraw
from utils.img_processing import MaxResize, outputs_to_objects
from transformers import TableTransformerForObjectDetection
from utils.logger import setup_logging
import logging
import os
import json as js
import sys
from args.table_constructor_args import parse_args


def table_constructor(
    img_path,
    model_name,
    device,
    output_directory="./outputs/constructed_tables",
    json=False,
    json_path="./outputs/constructed_tables_json",
):
    try:
        logging.info("✨ Sentinel Table Constructor has started...")

        model = TableTransformerForObjectDetection.from_pretrained(model_name)

        logging.debug("✔️  Model Loaded")
        logging.debug(f"🟡 Model name: {model_name}")
        logging.debug(f"🟡 Device type: {device}")

        image = Image.open(img_path).convert("RGB")

        logging.debug("✔️  Image Loaded")

        structure_transform = transforms.Compose(
            [
                MaxResize(1000),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )

        pixel_values = structure_transform(image).unsqueeze(0)
        pixel_values = pixel_values.to(device)

        with torch.no_grad():
            outputs = model(pixel_values)

        structure_id2label = model.config.id2label
        structure_id2label[len(structure_id2label)] = "no object"

        cells = outputs_to_objects(outputs, image.size, structure_id2label)
        draw = ImageDraw.Draw(image)

        for cell in cells:
            draw.rectangle(cell["bbox"], outline="red")
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            file_name = os.path.splitext(os.path.basename(img_path))[0]
            output_filename = f"{file_name}_constructed.png"
            output_path = os.path.join(output_directory, output_filename)
            image.save(output_path)

        if json:
            image_name, image_ext = os.path.splitext(os.path.basename(img_path))

            os.makedirs(json_path, exist_ok=True)

            with open(f"{json_path}/{image_name}.json", "w") as json_file:
                js.dump(cells, json_file, indent=4)
                logging.debug(f"✔️  json file created.")

        logging.info("✔️  Table constructed.")
        logging.info(f"{js.dumps(cells, indent=2)}")

        return cells

    except KeyboardInterrupt:
        logging.critical("\nKeyboardInterrupt: Exiting...")
        sys.exit(0)

    except Exception as e:
        logging.error(f"There was an error running the file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()

    # Set up logging based on the command-line argument
    setup_logging(args.log_level)

    # Example usage:

    table = table_constructor(
        args.img_path,
        args.model_name,
        args.device,
        args.output_directory,
        args.json,
        args.json_path,
    )
