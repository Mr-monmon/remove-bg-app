from flask import Flask, request, jsonify
from rembg import remove
from io import BytesIO
import base64
from PIL import Image
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Background Removal API is running!"

@app.route('/remove-background', methods=['POST'])
def remove_bg():
    try:
        data = request.get_json()
        image_data = data.get('image')
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400

        # Decode the base64 string
        img_data = base64.b64decode(image_data.split(',')[1])
        img = Image.open(BytesIO(img_data))

        # Remove the background using rembg
        result = remove(img)

        # Convert the result to a base64 string
        buffered = BytesIO()
        result.save(buffered, format="PNG")
        result_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return jsonify({"image": f"data:image/png;base64,{result_base64}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use the port provided by Render, or default to 5000
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
