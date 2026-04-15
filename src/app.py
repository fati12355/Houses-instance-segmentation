# app.py
import os
import torch
import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
from src.model import UNet  # You'll need to create this
from src.secrets import get_config

app = Flask(__name__)

# Load model
model = None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model():
    global model
    model_path = get_config('MODEL_PATH', 'models/best_unet_model.pth')
    model = UNet()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    print(f"✅ Model loaded from {model_path}")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'device': str(device)})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Get image from URL or base64
        if 'image_url' in data:
            import requests
            response = requests.get(data['image_url'])
            image = Image.open(io.BytesIO(response.content)).convert('RGB')
        elif 'image_base64' in data:
            image_data = base64.b64decode(data['image_base64'])
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        # Preprocess image
        image = image.resize((512, 512))
        image_tensor = torch.from_numpy(np.array(image)).permute(2, 0, 1).float() / 255.0
        image_tensor = image_tensor.unsqueeze(0).to(device)
        
        # Run inference
        with torch.no_grad():
            output = model(image_tensor)
            mask = torch.sigmoid(output).squeeze().cpu().numpy()
            mask_binary = (mask > 0.5).astype(np.uint8)
        
        # Convert mask to base64 for response
        mask_img = Image.fromarray(mask_binary * 255)
        buffered = io.BytesIO()
        mask_img.save(buffered, format='PNG')
        mask_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'mask': mask_base64,
            'mask_shape': mask_binary.shape
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    load_model()
    port = int(os.getenv('API_PORT', 5000))
    host = os.getenv('API_HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=False)