from flask import Flask, render_template, request
import os
import base64
from PIL import Image
from predict import predict_image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it does not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():

    prediction = None
    image_path = None
    filepath = None

    if request.method == "POST":

        # -------- Case 1: Image uploaded from file --------
        if "file" in request.files:

            file = request.files["file"]

            if file and file.filename != "":
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)

        # -------- Case 2: Image captured from camera --------
        if filepath is None and "camera_image" in request.form:

            img_data = request.form["camera_image"]

            if img_data != "":
                img_data = img_data.split(",")[1]
                img_bytes = base64.b64decode(img_data)

                filepath = os.path.join(app.config["UPLOAD_FOLDER"], "camera_image.png")

                with open(filepath, "wb") as f:
                    f.write(img_bytes)

        # -------- Fix image format (RGB + Resize) --------
        if filepath:

            img = Image.open(filepath).convert("RGB")   # remove alpha channel
            img = img.resize((256, 256))                # match model input size
            img.save(filepath)

            # -------- Run prediction --------
            with open(filepath, "rb") as f:
                label, confidence = predict_image(f)

            prediction = f"{label} ({confidence:.2f}%)"
            image_path = filepath

    return render_template(
        "index.html",
        prediction=prediction,
        image_path=image_path
    )


if __name__ == "__main__":
    app.run(debug=True)