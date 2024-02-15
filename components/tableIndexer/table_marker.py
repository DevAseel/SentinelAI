import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Patch
from PIL import Image
import time


class TableMarker:
    def __init__(self, img_path, objects):
        self.img_path = img_path
        self.objects = objects

    def fig2img(self, fig):
        """Convert a Matplotlib figure to a PIL Image and return it"""
        import io

        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        img = Image.open(buf)
        return img

    def visualize_detected_tables(self, out_path=None):
        start_time = time.time()

        print("✨ Sentinel Table Marker has started...")

        img = Image.open(self.img_path)

        print("✔️ Image loaded.")

        plt.imshow(img, interpolation="lanczos")
        fig = plt.gcf()
        fig.set_size_inches(20, 20)
        ax = plt.gca()

        for table in self.objects:
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

        if out_path is not None:
            plt.savefig(out_path, bbox_inches="tight", dpi=150)
        end_time = time.time()
        elapsed_time = end_time - start_time
        return {"process time": f"{elapsed_time:.2f}s", "output path": self.img_path}


if __name__ == "__main__":
    # Example usage:
    import os

    img_path = "./outputs/images/test_page_9.png"
    file_name = os.path.basename(img_path)
    det_tables = [
        {
            "label": "table",
            "score": 0.9987866282463074,
            "bbox": [
                157.6197509765625,
                1110.42919921875,
                1410.814453125,
                1244.0068359375,
            ],
        },
        {
            "label": "table",
            "score": 0.9981938004493713,
            "bbox": [
                160.2030029296875,
                1473.4356689453125,
                1410.72607421875,
                1912.1654052734375,
            ],
        },
    ]

    table_marker = TableMarker(img_path, det_tables)

    print(
        table_marker.visualize_detected_tables(
            out_path=f"./outputs/marked_tables/marked_{file_name}"
        )
    )
