from PIL import Image
import os
import time


class TableCropper:
    def __init__(self, img_path, tokens, class_thresholds, padding=10):
        self.img_path = img_path
        self.tokens = tokens
        self.class_thresholds = class_thresholds
        self.padding = padding

    def crop_table(self, objects):
        print("✨ Sentinel Table Cropper has started...")

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
                token for token in self.tokens if self.iob(token["bbox"], bbox) >= 0.5
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

    def iob(self, bbox1, bbox2):
        # Implement your IOB (Intersection over Bounding Box) calculation here
        # This function is a placeholder and should be replaced with the actual calculation
        pass


if __name__ == "__main__":
    tokens = []
    detection_class_thresholds = {"table": 0.5, "table rotated": 0.5, "no object": 10}
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
    img_path = "./outputs/images/test_page_9.png"
    table_cropper = TableCropper(img_path, tokens, detection_class_thresholds)
    tables_crops = table_cropper.crop_table(det_tables)
    # Provide a file path for save, not just a directory
    output_dir = "./outputs/tables/"
    os.makedirs(output_dir, exist_ok=True)
    cropped_table = tables_crops[0]["image"].convert("RGB")
    cropped_table.save(os.path.join(output_dir, "cropped_table.png"))
    print("✔️ Table cropped. output: ./outputs/tables")
