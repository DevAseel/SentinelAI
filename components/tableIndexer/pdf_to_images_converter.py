import os
import time
from pathlib import Path
from pdf2image import convert_from_path
from utils.logger import setup_logging
import logging
import sys
from args.pdf_to_images_converter_args import parse_args


def convert_pdf_to_images(pdf_name, output_directory="./outputs/images"):
    if not pdf_name.lower().endswith(".pdf"):
        pdf_name += ".pdf"
    pdf_path = Path("./pdfs") / pdf_name
    output_directory = Path(output_directory)

    os.makedirs(output_directory, exist_ok=True)
    logging.info("✨ Sentinel PDF to Images Converter is starting...")

    start_time = time.time()

    try:
        pdf_to_images = convert_from_path(pdf_path)
        if pdf_name.lower().endswith(".pdf"):
            pdf_name = pdf_name[:-4]
        for idx in range(len(pdf_to_images)):
            img_name = f"{pdf_name}_page_{idx + 1}.png"
            output_path = output_directory / img_name
            pdf_to_images[idx].save(output_path, "PNG")
            logging.debug(f"📄{img_name} ✔️")
        end_time = time.time()
        elapsed_time = end_time - start_time

        logging.info(
            f"🔥Successfully converted PDF to images, output folder is: {output_directory}"
        )
        logging.debug(f"⏱ Time taken: {elapsed_time:.2f} seconds")

        return len(pdf_to_images)

    except KeyboardInterrupt:
        logging.critical("\nExiting...")
        sys.exit(0)

    except Exception as e:
        logging.error(f"❌ Error converting PDF: {e}")


if __name__ == "__main__":
    args = parse_args()

    # Set up colorful logging based on the command-line argument
    setup_logging(args.log_level)

    # Example usage:
    convert_pdf_to_images(
        pdf_name=args.pdf_name, output_directory=args.output_directory
    )
