# app_tf_free.py
import os
import io
from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
# Removed TensorFlow and TensorFlow Hub imports

from chat1 import extract_pdf_text, initialize_vector_store
from chat2 import setup_retrieval_qa

app = Flask(__name__)

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# Removed MODEL_URL and IMAGE_SHAPE as TensorFlow is not used

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Load Text RAG Model ---
pdf_files = ["Data/handbook_01_rice_cultivation.pdf","Data/farmerbook.pdf","Data/final.pdf","Data/IndianAgriculture.pdf","Data/krishiAI.pdf"]
pdf_texts = [extract_pdf_text(pdf_file) for pdf_file in pdf_files]
all_contents = pdf_texts
db = initialize_vector_store(all_contents)
text_chain = setup_retrieval_qa(db)

# --- Placeholder Image Analysis Logic (TensorFlow-Free) ---
# This is a simplified placeholder. A real-world TF-free solution might involve:
# - Basic image feature extraction (color histograms, texture) + simple classifier (e.g., scikit-learn SVM if allowed)
# - Calling an external Plant Disease API
# - A rule-based system

# Placeholder disease details - replace with actual data if using a real model/API
DISEASE_INFO = {
    "Placeholder: Leaf Spot": {
        "crop": "Various Crops",
        "symptoms": "Small, dark spots on leaves, sometimes with yellow halos.",
        "treatment": "Remove affected leaves, ensure good air circulation, consider appropriate fungicide if severe."
    },
    "Placeholder: Powdery Mildew": {
        "crop": "Various Crops",
        "symptoms": "White powdery patches on leaves, stems, and flowers.",
        "treatment": "Improve air circulation, avoid overhead watering, use resistant varieties, apply fungicide if necessary."
    },
    "Healthy": {
        "crop": "Unknown",
        "symptoms": "The plant appears to be healthy. No significant disease symptoms detected.",
        "treatment": "Maintain good agricultural practices, monitor regularly."
    }
}

def analyze_plant_image_placeholder(image_bytes):
    """Placeholder function to simulate disease detection without TensorFlow."""
    try:
        # Basic check: Try to open the image to ensure it's valid
        img = Image.open(io.BytesIO(image_bytes))
        # Simulate a prediction - in a real scenario, more complex analysis would go here
        # For this placeholder, we'll randomly pick a disease or healthy state
        possible_results = list(DISEASE_INFO.keys())
        predicted_class_name = np.random.choice(possible_results)
        return predicted_class_name
    except Exception as e:
        print(f"Error in placeholder analysis: {e}")
        return None # Indicate analysis failure

# --- Helper Functions ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Routes ---
@app.route('/')
def index():
    # Use the modified HTML file
    return render_template('modified_index.html')

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form['messageText'].strip().lower()

    if query in ["who is your dady","who developed you", "who created you", "who made you"]:
        return jsonify({"answer": " Born from code, raised by data, and fueled by farm wisdom. All thanks to the legend himself Mr. Madhav. I call him Dad, but you can call him my creator."})

    elif query in ["Tell me about KrishiAI"]:
        return jsonify({"answer": "KrishiAI is an artificial intelligence program designed to provide information and assistance related to agriculture, specifically focusing on topics like cultivation"})

    # Use the text RAG chain for text queries
    response = text_chain(query)
    return jsonify({"answer": response['result']})

@app.route('/predict_disease', methods=['POST'])
def predict_disease():
    if 'imageFile' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['imageFile']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        try:
            img_bytes = file.read()
            
            # Use the placeholder analysis function
            predicted_class_name = analyze_plant_image_placeholder(img_bytes)

            if predicted_class_name is None:
                 return jsonify({"error": "Failed to analyze image"}), 500

            # Get disease details (using placeholder mapping)
            disease_details = DISEASE_INFO.get(predicted_class_name, {
                "crop": "Unknown",
                "symptoms": "Could not identify specific disease details.",
                "treatment": "Consult an agricultural expert."
            })

            # Format response
            response_text = f"Detected: {predicted_class_name}\n"
            if disease_details["crop"] != "Unknown":
                response_text += f"Crop: {disease_details['crop']}\n"
            response_text += f"Symptoms: {disease_details['symptoms']}\n"
            response_text += f"Advice: {disease_details['treatment']}"

            return jsonify({"answer": response_text})

        except Exception as e:
            print(f"Error processing image: {e}")
            return jsonify({"error": "Failed to process image"}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == "__main__":
    if not os.path.exists("Data"):
        print("Warning: 'Data' directory not found. PDF loading might fail if paths are relative.")
    
    print("Starting Flask app (TensorFlow-Free Version)...")
    # Ensure Flask runs on 0.0.0.0 to be accessible externally if needed
    app.run(host='0.0.0.0', port=5000, debug=True)

