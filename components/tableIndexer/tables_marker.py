import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Patch
from PIL import Image
import time
import logging
from utils.logger import setup_logging
import os
import argparse
import json


def parse_args():
    parser = argparse.ArgumentParser(
        description="Mark tables in an image using the json file generated from table_scanner method"
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        default="INFO",
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    parser.add_argument(
        "--img-path",
        dest="img_path",
        required=True,
        help="Specify the path of the image which contains the table you want to mark",
    )
    parser.add_argument(
        "--json-path",
        dest="json_path",
        required=True,
        help="set the path of the json file containing marking information from table_scanner method",
    )
    parser.add_argument(
        "--output-path",
        dest="output_path",
        default="./outputs/marked_tables",
        help="set the output path for the marked image",
    )
    return parser.parse_args()


class TableMarker:
    def __init__(self, img_path, json_path, output_path):
        self.img_path = img_path
        self.json_path = json_path
        self.output_path = output_path

    def fig2img(self, fig):
        """Convert a Matplotlib figure to a PIL Image and return it"""
        import io

        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        img = Image.open(buf)
        return img

    def visualize_detected_tables(self):
        start_time = time.time()

        logging.info("✨ Sentinel Table Marker has started...")

        try:
            img = Image.open(self.img_path)

            logging.debug("✔️  Image loaded.")

            plt.imshow(img, interpolation="lanczos")
            fig = plt.gcf()
            fig.set_size_inches(20, 20)
            ax = plt.gca()

            with open(self.json_path, "r") as json_file:
                tables_data = json.load(json_file)

            for table in tables_data["data"]:
                bbox = table["bbox"]

                if table["label"] == "table":
                    facecolor = (1, 0, 0.45)
                    edgecolor = (1, 0, 0.45)
                    alpha = 0.3
                    linewidth = 2
                    hatch = "//////"
                elif table["label"] == "table rotated":
                    facecolor = (0.95, 0.6, 0.1)
                    edgecolor = (0.95, 0.6, 0.1)
                    alpha = 0.3
                    linewidth = 2
                    hatch = "//////"
                else:
                    continue

                rect = patches.Rectangle(
                    bbox[:2],
                    bbox[2] - bbox[0],
                    bbox[3] - bbox[1],
                    linewidth=linewidth,
                    edgecolor="none",
                    facecolor=facecolor,
                    alpha=0.1,
                )
                ax.add_patch(rect)
                rect = patches.Rectangle(
                    bbox[:2],
                    bbox[2] - bbox[0],
                    bbox[3] - bbox[1],
                    linewidth=linewidth,
                    edgecolor=edgecolor,
                    facecolor="none",
                    linestyle="-",
                    alpha=alpha,
                )
                ax.add_patch(rect)
                rect = patches.Rectangle(
                    bbox[:2],
                    bbox[2] - bbox[0],
                    bbox[3] - bbox[1],
                    linewidth=0,
                    edgecolor=edgecolor,
                    facecolor="none",
                    linestyle="-",
                    hatch=hatch,
                    alpha=0.2,
                )
                ax.add_patch(rect)

            plt.xticks([], [])
            plt.yticks([], [])

            legend_elements = [
                Patch(
                    facecolor=(1, 0, 0.45),
                    edgecolor=(1, 0, 0.45),
                    label="Table",
                    hatch="//////",
                    alpha=0.3,
                ),
                Patch(
                    facecolor=(0.95, 0.6, 0.1),
                    edgecolor=(0.95, 0.6, 0.1),
                    label="Table (rotated)",
                    hatch="//////",
                    alpha=0.3,
                ),
            ]
            plt.legend(
                handles=legend_elements,
                bbox_to_anchor=(0.5, -0.02),
                loc="upper center",
                borderaxespad=0,
                fontsize=10,
                ncol=2,
            )
            plt.gcf().set_size_inches(10, 10)
            plt.axis("off")
            img_name, img_ext = os.path.splitext(os.path.basename(self.img_path))
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
            plt.savefig(
                f"{self.output_path}/marked_{img_name}.png",
                bbox_inches="tight",
                dpi=150,
            )
            end_time = time.time()
            elapsed_time = end_time - start_time
            output = {
                "process time": f"{elapsed_time:.2f}s",
                "output path": self.output_path,
            }
            logging.info(f"{json.dumps(output, indent=2)}")

            return output

        except KeyboardInterrupt:
            logging.critical("\nExiting...")
            sys.exit(0)

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            sys.exit(1)


if __name__ == "__main__":
    args = parse_args()

    # Set up logging based on the command-line argument
    setup_logging(args.log_level.upper())

    # Example usage:
    table_marker = TableMarker(args.img_path, args.json_path, args.output_path)

    table_marker.visualize_detected_tables()
