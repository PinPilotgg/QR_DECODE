import cv2
import re
import qrcode
import numpy as np
from pyzbar.pyzbar import decode

def decode_qr_code(image_path):
    img = cv2.imread(image_path)

    decoded_objects = decode(img)

    if not decoded_objects:
        return "No QR code detected in the image."

    qr_data = decoded_objects[0].data.decode('utf-8')

    reference_id = re.search(r'Reference ID: ([\w-]+)', qr_data)
    address = re.search(r'Address: (.*)', qr_data)
    pincode = re.search(r'\b\d{6}\b', qr_data)
    post_office = re.search(r'Post Office: (.*)', qr_data)
    district = re.search(r'District: (.*)', qr_data)
    state = re.search(r'State: (.*)', qr_data)
    coordinates = re.search(r'Coordinates: ([\d.]+), ([\d.]+)', qr_data)

    output = []
    if reference_id:
        output.append(f"Reference ID: {reference_id.group(1)}")
    if address:
        output.append(f"Address: {address.group(1)}")
    if pincode:
        output.append(f"Pincode: {pincode.group()}")  # Fixing the pincode extraction here
    if post_office:
        output.append(f"Post Office: {post_office.group(1)}")
    if district:
        output.append(f"District: {district.group(1)}")
    if state:
        output.append(f"State: {state.group(1)}")
    if coordinates:
        output.append(f"Latitude: {coordinates.group(1)}")
        output.append(f"Longitude: {coordinates.group(2)}")
    return "\n".join(output)

if __name__ == "__main__":
    image_path = './response_image.png'  # Update this path if the QR code image is named differently
    decoded_info = decode_qr_code(image_path)
    print(decoded_info)
