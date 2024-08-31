from flask import Flask, request, jsonify
import cv2
import re
from pyzbar.pyzbar import decode

app = Flask(__name__)

def decode_qr_code(image_path):
    img = cv2.imread(image_path)
    decoded_objects = decode(img)

    if not decoded_objects:
        return {"error": "No QR code detected in the image."}

    qr_data = decoded_objects[0].data.decode('utf-8')

    # Extract relevant information using regular expressions
    reference_id = re.search(r'Reference ID: ([\w-]+)', qr_data)
    address = re.search(r'Address: (.*)', qr_data)
    pincode = re.search(r'\b\d{6}\b', qr_data)
    post_office = re.search(r'Post Office: (.*)', qr_data)
    district = re.search(r'District: (.*)', qr_data)
    state = re.search(r'State: (.*)', qr_data)

    output = {}
    if reference_id:
        output["Reference ID"] = reference_id.group(1)
    if address:
        output["Address"] = address.group(1)
    if pincode:
        output["Pincode"] = pincode.group()
    if post_office:
        output["Post Office"] = post_office.group(1)
    if district:
        output["District"] = district.group(1)
    if state:
        output["State"] = state.group(1)

    return output

@app.route('/decode', methods=['POST'])
def decode_qr():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the uploaded file to a temporary location
    file_path = "./uploaded_image.png"
    file.save(file_path)
    
    # Decode the QR code from the image
    result = decode_qr_code(file_path)
    
    # Return the decoded information as JSON
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
