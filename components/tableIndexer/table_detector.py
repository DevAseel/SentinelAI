from transformers import AutoModelForObjectDetection
import torch
from torchvision import transforms
from PIL import Image
import time
from utils.img_processing import MaxResize, outputs_to_objects


class TableDetector:
    def __init__(self, img_path):
        self.img_path = img_path
        self.model_load_time = 0
        self.model = self.load_model()

    print("✨ Sentinel Table Detector has started...")

    def load_model(self):
        start_time = time.time()
        model = AutoModelForObjectDetection.from_pretrained(
            "microsoft/table-transformer-detection", revision="no_timm"
        )
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        end_time = time.time()
        self.model_load_time = end_time - start_time

        print("✔️  Model loaded.")

        return model

    def detect_table(self):
        start_time = time.time()
        image = Image.open(self.img_path).convert("RGB")

        print("✔️  Image loaded.")

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
        return output


if __name__ == "__main__":
    # Example usage:
    img_path = "./outputs/images/test_page_9.png"
    table_detector = TableDetector(img_path)
    print(table_detector.detect_table())
