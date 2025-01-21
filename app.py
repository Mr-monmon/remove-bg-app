from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image
import base64
import io

app = Flask(__name__)

@app.route('/', methods=['POST'])
def remove_background():
    try:
        data = request.get_json()
        base64_image = data.get('image')
        image_bytes = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Remove background
        output = remove(image)
        
        # Convert back to base64
        buffered = io.BytesIO()
        output.save(buffered, format="PNG")
        processed_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({'processedImage': processed_image})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
