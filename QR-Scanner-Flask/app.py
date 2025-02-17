from flask import Flask, render_template, request
import cv2
import numpy as np
from pyzbar.pyzbar import decode

app = Flask(__name__)

def decode_barcode(frame):
    barcodes = decode(frame)
    results = []
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        results.append({"data": barcode_data, "type": barcode_type})
    return results

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    file = request.files["file"]
    file_bytes = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    barcodes = decode_barcode(frame)
    return {"barcodes": barcodes}

if __name__ == "__main__":
    app.run(debug=True)
