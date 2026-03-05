from pathlib import Path
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

img_path = Path(__file__).parent / "test.jpg"

results = model(str(img_path))

for r in results:
    r.show()