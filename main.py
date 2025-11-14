from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import torch
import numpy as np
import easyocr
from ultralytics import YOLO
import shutil
import os
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from paddleocr import PaddleOCR
import re

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI is working!"}

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLOv11 model
model = YOLO("best1.pt")  # Ensure this model detects bus, car, license plate, motorcycle, and truck
# reader = easyocr.Reader(["en"])  # EasyOCR for license plate text extraction


# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# State mapping based on license plate prefixes
STATE_MAPPING = {
    'A': 'Perak', 'B': 'Selangor', 'C': 'Pahang', 'D': 'Kelantan', 'J': 'Johor',
    'K': 'Kedah', 'M': 'Melaka', 'N': 'Negeri Sembilan', 'P': 'Pulau Pinang',
    'R': 'Perlis', 'S': 'Sabah', 'T': 'Terengganu', 'W': 'Kuala Lumpur',
    'V': 'Labuan', 'Q': 'Sarawak'
}

# Directories to store processed images and cropped plates
output_dir = "static"
crop_dir = "static/crops"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(crop_dir, exist_ok=True)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Vehicle type mapping (Modify according to your trained classes)
CLASS_MAPPING = {
    0: "bus",
    1: "car",
    2: "license-plate",
    3: "motorcycle",
    4: "truck"
}

# def extract_text_from_plate(plate_image):
#     """Extract text using EasyOCR from a cropped license plate image."""
#     gray = cv2.cvtColor(plate_image, cv2.COLOR_RGB2GRAY)
#     results = reader.readtext(gray)
#
#     if results:
#         ocr_text = results[0][1]
#         first_letter = ocr_text[0] if ocr_text else ""
#         state = STATE_MAPPING.get(first_letter.upper(), "Unknown State")
#         return ocr_text, state
#     return "", "Unknown State"

# def extract_text_from_plate(plate_image):
#     """Extract text using PaddleOCR from a cropped license plate image."""
#     # Convert image to grayscale
#     gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
#
#     # Run OCR
#     result = ocr.ocr(gray, cls=True)
#
#     if not result or len(result[0]) == 0:
#         return "", "Unknown State"
#
#     # Extract text from OCR results
#     detected_texts = [res[1][0] for res in result[0]]
#
#     # Filter text: Separate letters (first row) and numbers (second row)
#     letters = []
#     numbers = []
#
#     for text in detected_texts:
#         if re.fullmatch(r"[A-Za-z]+", text):  # Match letters only
#             letters.append(text)
#         elif re.fullmatch(r"[0-9]+", text):  # Match numbers only
#             numbers.append(text)
#
#     # Combine the first row (letters) and second row (numbers)
#     plate_number = " ".join(letters) + " " + " ".join(numbers)
#
#     # Determine the state based on the first letter of the first row
#     first_letter = letters[0][0] if letters else ""
#     state = STATE_MAPPING.get(first_letter.upper(), "Unknown State")
#
#     return plate_number.strip(), state

def extract_text_from_plate(plate_image):
    """Extract text using PaddleOCR from a cropped license plate image, supporting both single-row and two-row formats."""
    # Convert image to grayscale
    gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)

    # Run OCR
    result = ocr.ocr(gray, cls=True)

    # Check if OCR detected any text
    if not result or not result[0]:  # Check if result is None or empty
        return "No Text Detected", "Unknown State"

    # Extract text from OCR result
    detected_texts = []
    for line in result[0]:  # PaddleOCR returns lines as lists of detected words
        if line and len(line) > 1:  # Ensure the line has recognized text
            text = line[1][0]  # Extract the recognized text
            detected_texts.append(text)

    # Process single-row vs two-row plate formats
    if len(detected_texts) == 1:
        plate_number = detected_texts[0]  # Single-row plate
    elif len(detected_texts) == 2:
        plate_number = detected_texts[0] + " " + detected_texts[1]  # Two-row plate: Combine rows
    else:
        plate_number = ""

    # Handle empty plate cases
    if not plate_number:
        return "No Plate Detected", "Unknown State"

    first_letter = plate_number[0] if plate_number else ""
    state = STATE_MAPPING.get(first_letter.upper(), "Unknown State")

    return plate_number, state

@app.post("/detect/")
async def detect_plate(file: UploadFile = File(...)):
    """Detect classes in the image, extract license plate text, and return results."""
    file_path = f"temp_{file.filename}"

    # Save uploaded image
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load image
    img = cv2.imread(file_path)

    # Run YOLOv11 inference
    results = model.predict(img, conf=0.4, line_width=2, save=False)

    detection_data = {"detected_classes": [], "plates": []}

    # Define colors for each class
    CLASS_COLORS = {
        0: (0, 255, 0),  # Green for bus
        1: (255, 0, 0),  # Blue for car
        2: (0, 0, 255),  # Red for license plates
        3: (255, 255, 0),  # Yellow for motorcycle
        4: (255, 165, 0)  # Orange for truck
    }

    for result in results:
        for box in result.boxes:
            if box.conf[0] >= 0.4:  # Ensure detection confidence meets threshold
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])  # Get detected class ID
                label = CLASS_MAPPING.get(class_id, "Unknown")
                color = CLASS_COLORS.get(class_id, (255, 255, 255))  # Default to white

                detection_data["detected_classes"].append({
                    "class": label,
                    "bbox": [x1, y1, x2, y2]
                })

                # If detected class is a license plate, extract the text
                if class_id == 2:
                    # Expand bounding box size (e.g., increase by 20%)
                    expand_ratio = 0.2

                    # Calculate expansion values
                    x_expand = int((x2 - x1) * expand_ratio)
                    y_expand = int((y2 - y1) * expand_ratio)

                    # Expand the bounding box while ensuring it remains within image bounds
                    x1_exp = max(0, x1 - x_expand)
                    y1_exp = max(0, y1 - y_expand)
                    x2_exp = min(img.shape[1], x2 + x_expand)
                    y2_exp = min(img.shape[0], y2 + y_expand)

                    # Crop the expanded license plate region
                    plate_crop = img[y1_exp:y2_exp, x1_exp:x2_exp]

                    # plate_crop = img[y1:y2, x1:x2]
                    plate_number, state = extract_text_from_plate(plate_crop)

                    # Save cropped license plate image
                    crop_filename = f"{crop_dir}/crop_{file.filename}"
                    cv2.imwrite(crop_filename, plate_crop)

                    detection_data["plates"].append({
                        "plate_number": plate_number,
                        "state": state,
                        "bbox": [x1, y1, x2, y2],
                        "crop_url": f"/static/crops/crop_{file.filename}"
                    })

                # Draw bounding box and label
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3)

    # Save processed image
    output_path = f"{output_dir}/processed_{file.filename}"
    cv2.imwrite(output_path, img)

    # Remove temp file
    os.remove(file_path)

    return JSONResponse(content={
        "detections": detection_data,
        "image_url": f"/static/processed_{file.filename}"
    })