from transformers import TableTransformerForObjectDetection
import torch
from torchvision import transforms
from PIL import Image, ImageDraw
from utils.img_processing import MaxResize, outputs_to_objects
import os
import matplotlib.pyplot as plt


class TableTransformer:
    def __init__(self, model_path, device="cuda"):
        self.model = TableTransformerForObjectDetection.from_pretrained(model_path)
        self.model.to(device)
        self.device = device

    def recognize_structure(self, image_path):
        image = Image.open(image_path).convert("RGB")

        structure_transform = transforms.Compose(
            [
                MaxResize(1000),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )

        pixel_values = structure_transform(image).unsqueeze(0)
        pixel_values = pixel_values.to(self.device)

        with torch.no_grad():
            outputs = self.model(pixel_values)

        structure_id2label = self.model.config.id2label
        structure_id2label[len(structure_id2label)] = "no object"

        cells = outputs_to_objects(outputs, image.size, structure_id2label)
        return cells

    def visualize_cells(self, image_path, cells):
        img = Image.open(image_path).convert("RGB")
        img_visualized = img.copy()
        draw = ImageDraw.Draw(img_visualized)

        for cell in cells:
            draw.rectangle(cell["bbox"], outline="red")

        return img_visualized

    def save_visualized_image(self, img, output_path):
        img.save(output_path)

    def plot_results(self, cells, class_to_visualize, image_path):
        if class_to_visualize not in self.model.config.id2label.values():
            raise ValueError("Class should be one of the available classes")

        plt.figure(figsize=(16, 10))
        img = Image.open(image_path).convert("RGB")

        plt.imshow(img)
        ax = plt.gca()

        for cell in cells:
            score = cell["score"]
            bbox = cell["bbox"]
            label = cell["label"]

            if label == class_to_visualize:
                xmin, ymin, xmax, ymax = tuple(bbox)

                ax.add_patch(
                    plt.Rectangle(
                        (xmin, ymin),
                        xmax - xmin,
                        ymax - ymin,
                        fill=False,
                        color="red",
                        linewidth=3,
                    )
                )
                text = f'{cell["label"]}: {score:0.2f}'
                ax.text(
                    xmin,
                    ymin,
                    text,
                    fontsize=15,
                    bbox=dict(facecolor="yellow", alpha=0.5),
                )
                plt.axis("off")

        output_folder = os.path.join("outputs", "transformed_tables")
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, "transformed_result.png")
        plt.savefig(output_path, bbox_inches="tight", dpi=150)
        plt.close()


if __name__ == "__main__":
    model_path = "microsoft/table-structure-recognition-v1.1-all"
    image_path = "./outputs/tables/cropped_table.png"

    table_transformer = TableTransformer(model_path)
    recognized_cells = table_transformer.recognize_structure(image_path)
    visualized_image = table_transformer.visualize_cells(image_path, recognized_cells)
    output_path = os.path.join("outputs", "transformed_tables", "visualized_image.png")
    table_transformer.save_visualized_image(visualized_image, output_path)

    table_transformer.plot_results(
        recognized_cells, class_to_visualize="table row", image_path=image_path
    )

    def get_cell_coordinates_by_row(table_data):
        # Extract rows and columns
        rows = [entry for entry in table_data if entry["label"] == "table row"]
        columns = [entry for entry in table_data if entry["label"] == "table column"]

        # Sort rows and columns by their Y and X coordinates, respectively
        rows.sort(key=lambda x: x["bbox"][1])
        columns.sort(key=lambda x: x["bbox"][0])

        # Function to find cell coordinates
        def find_cell_coordinates(row, column):
            cell_bbox = [
                column["bbox"][0],
                row["bbox"][1],
                column["bbox"][2],
                row["bbox"][3],
            ]
            return cell_bbox

        # Generate cell coordinates and count cells in each row
        cell_coordinates = []

        for row in rows:
            row_cells = []
            for column in columns:
                cell_bbox = find_cell_coordinates(row, column)
                row_cells.append({"column": column["bbox"], "cell": cell_bbox})

            # Sort cells in the row by X coordinate
            row_cells.sort(key=lambda x: x["column"][0])

            # Append row information to cell_coordinates
            cell_coordinates.append(
                {"row": row["bbox"], "cells": row_cells, "cell_count": len(row_cells)}
            )

        # Sort rows from top to bottom
        cell_coordinates.sort(key=lambda x: x["row"][1])

        return cell_coordinates

    cell_coordinates = get_cell_coordinates_by_row(recognized_cells)
    import numpy as np
    import csv
    import easyocr
    from tqdm.auto import tqdm

    reader = easyocr.Reader(
        ["en"]
    )  # this needs to run only once to load the model into memory

    def apply_ocr(cell_coordinates):
        # let's OCR row by row
        data = dict()
        max_num_columns = 0
        for idx, row in enumerate(tqdm(cell_coordinates)):
            row_text = []
        for cell in row["cells"]:
            # crop cell out of image
            cropped_table = Image.open(image_path).convert("RGB")
            cell_image = np.array(cropped_table.crop(cell["cell"]))
            # apply OCR
            result = reader.readtext(np.array(cell_image))
            if len(result) > 0:
                # print([x[1] for x in list(result)])
                text = " ".join([x[1] for x in result])
                row_text.append(text)

        if len(row_text) > max_num_columns:
            max_num_columns = len(row_text)

        data[idx] = row_text

        print("Max number of columns:", max_num_columns)

        # pad rows which don't have max_num_columns elements
        # to make sure all rows have the same number of columns
        for row, row_data in data.copy().items():
            if len(row_data) != max_num_columns:
                row_data = row_data + [
                    "" for _ in range(max_num_columns - len(row_data))
                ]
            data[row] = row_data

        return data

    data = apply_ocr(cell_coordinates)

    for row, row_data in data.items():
        print(row_data)
