import os
import time

from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np


app = Flask(__name__)

# =========================
# UPLOAD SETTINGS
# =========================

UPLOAD_FOLDER = os.path.join("assets", "uploads")

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

# Create upload folder if it does not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# CHECK ALLOWED FILE
# =========================

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================
# WASTE ANALYSIS
# =========================

def analyze_waste(image_path):

    image = Image.open(image_path).convert("RGB")

    # Resize image
    image = image.resize((200, 200))

    # Convert to NumPy array
    img = np.array(image)

    # Average RGB values
    avg_color = img.mean(axis=(0, 1))

    red = float(avg_color[0])
    green = float(avg_color[1])
    blue = float(avg_color[2])

    brightness = (red + green + blue) / 3

    # Color variation
    color_variation = float(img.std())

    # =========================
    # SIMPLE CLASSIFICATION
    # =========================

    if brightness > 210 and color_variation < 35:

        waste_type = "Paper"
        category = "Recyclable"
        confidence = 87
        disposal = (
            "Place it in the paper recycling bin. "
            "Keep paper dry and remove plastic or non-paper materials."
        )
        description = (
            "The image appears to contain a light-colored "
            "paper-like material."
        )

    elif green > red * 1.15 and green > blue * 1.10:

        waste_type = "Organic"
        category = "Compostable"
        confidence = 84
        disposal = (
            "Place it in the organic waste or compost bin. "
            "Avoid mixing it with plastic or metal waste."
        )
        description = (
            "The image has strong green or organic visual "
            "characteristics."
        )

    elif red > blue * 1.20 and red > green * 1.10:

        waste_type = "Plastic"
        category = "Recyclable"
        confidence = 72
        disposal = (
            "Place it in the recyclable plastic waste bin. "
            "Clean the container before recycling when possible."
        )
        description = (
            "The image contains visual characteristics "
            "that may indicate plastic waste."
        )

    elif color_variation > 70:

        waste_type = "Mixed Waste"
        category = "Non-Recyclable / Mixed"
        confidence = 76
        disposal = (
            "Separate recyclable and organic materials "
            "before disposing of the remaining waste."
        )
        description = (
            "The image contains multiple different visual "
            "regions and may represent mixed waste."
        )

    else:

        waste_type = "Other"
        category = "Check Manually"
        confidence = 55
        disposal = (
            "Check the item manually and place it in "
            "the appropriate waste bin."
        )
        description = (
            "The system could not confidently identify "
            "a specific waste category."
        )

    return {
        "waste_type": waste_type,
        "category": category,
        "confidence": confidence,
        "disposal_method": disposal,
        "description": description
    }


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# DETECT WASTE
# =========================

@app.route("/detect", methods=["POST"])
def detect():

    # Check if image exists
    if "image" not in request.files:

        return render_template(
            "index.html",
            error="Please select an image."
        )

    file = request.files["image"]

    # Check empty filename
    if file.filename == "":

        return render_template(
            "index.html",
            error="Please select an image."
        )

    # Check file extension
    if not allowed_file(file.filename):

        return render_template(
            "index.html",
            error="Only JPG, JPEG, PNG and WEBP images are allowed."
        )

    try:

        # Secure original filename
        original_name = secure_filename(file.filename)

        # Create unique filename
        filename = (
            str(int(time.time() * 1000))
            + "_"
            + original_name
        )

        # Full file path
        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        # Save uploaded image
        file.save(filepath)

        # Analyze image
        result = analyze_waste(filepath)

        # URL used by browser to display image
        image_path = "/uploads/" + filename

        return render_template(
            "result.html",
            result=result,
            image_path=image_path
        )

    except Exception as e:

        return render_template(
            "index.html",
            error="Error analyzing image: " + str(e)
        )


# =========================
# SERVE UPLOADED IMAGES
# =========================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )