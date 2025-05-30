# # app.py
# from flask import Flask, render_template, request, jsonify
# from chat1 import fetch_website_content, extract_pdf_text, initialize_vector_store
# from chat2 import llm, setup_retrieval_qa


# app = Flask(__name__)

# # Example URLs and PDF files
# # urls = ["https://mospi.gov.in/4-agricultural-statistics"]   #"https://desagri.gov.in/",
# pdf_files = ["Data/handbook_01_rice_cultivation.pdf","Data/farmerbook.pdf","Data/final.pdf","Data/IndianAgriculture.pdf","Data/krishiAI.pdf"]

# # Fetch content from websites
# # website_contents = [fetch_website_content(url) for url in urls]

# # Extract text from PDF files
# pdf_texts = [extract_pdf_text(pdf_file) for pdf_file in pdf_files]

# # Combine all content into chunks
# # all_contents = website_contents + pdf_texts
# all_contents = pdf_texts

# # Initialize the vector store
# db = initialize_vector_store(all_contents)

# # Set up the RetrievalQA chain
# chain = setup_retrieval_qa(db)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/ask', methods=['POST'])
# def ask():
#     query = request.form['messageText'].strip().lower()
#     query = query.lower().strip()

#     if query in ["who is your dady","who developed you", "who created you", "who made you"]:
#         return jsonify({"answer": " Born from code, raised by data, and fueled by farm wisdom. All thanks to the legend himself Mr. Madhav. I call him Dad, but you can call him my creator."})
    
#     elif query in ["Tell me about KrishiAI"]:
#         return jsonify({"answer": "KrishiAI is an artificial intelligence program designed to provide information and assistance related to agriculture, specifically focusing on topics like cultivation"})
    
#     response = chain(query)
#     return jsonify({"answer": response['result']})

# if __name__ == "__main__":
#     app.run(debug=True)


# app.py
import os
import io
from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

from chat1 import extract_pdf_text, initialize_vector_store # Removed fetch_website_content as it wasn't used
from chat2 import setup_retrieval_qa # Removed llm import as setup_retrieval_qa handles it

app = Flask(__name__)

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MODEL_URL = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4" # Placeholder - ideally find a PlantVillage specific model
IMAGE_SHAPE = (224, 224)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Load Models ---
# Load Text RAG Model
pdf_files = ["Data/handbook_01_rice_cultivation.pdf","Data/farmerbook.pdf","Data/final.pdf","Data/IndianAgriculture.pdf","Data/krishiAI.pdf"]
pdf_texts = [extract_pdf_text(pdf_file) for pdf_file in pdf_files]
all_contents = pdf_texts
db = initialize_vector_store(all_contents)
text_chain = setup_retrieval_qa(db)

# Load Image Classification Model
print(f"Loading image model from: {MODEL_URL}")
image_classifier_model = hub.KerasLayer(MODEL_URL, input_shape=IMAGE_SHAPE+(3,))
print("Image model loaded.")

# --- Helper Functions ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize(IMAGE_SHAPE)
    img = np.array(img)/255.0 # Normalize to [0,1]
    return img

# Placeholder for disease details - replace with actual data
DISEASE_INFO = {
    "Example Disease 1": {
        "crop": "Example Crop A",
        "symptoms": "Shows yellow spots on leaves, wilting.",
        "treatment": "Apply fungicide X, ensure proper drainage."
    },
    "Example Disease 2": {
        "crop": "Example Crop B",
        "symptoms": "Brown patches, leaf curling.",
        "treatment": "Use pest resistant varieties, apply neem oil."
    },
    "Healthy": {
        "crop": "Unknown",
        "symptoms": "The plant appears to be healthy.",
        "treatment": "Maintain good agricultural practices."
    }
    # Add more entries based on the actual model's classes
}

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

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
            img = preprocess_image(img_bytes)
            img_batch = np.expand_dims(img, axis=0) # Add batch dimension

            # Get predictions
            predictions = image_classifier_model.predict(img_batch)
            # Assuming the model outputs probabilities for classes, get the top prediction
            # You'll need to map the predicted index to a class name based on your model
            # This requires knowing the class labels the TF Hub model was trained on.
            # For a generic ImageNet model, this won't be plant diseases directly.
            # *** Placeholder: Replace with actual class mapping ***
            predicted_index = np.argmax(predictions[0])
            # Placeholder class names - replace with actual classes from the model
            class_names = list(DISEASE_INFO.keys()) # Use keys from our placeholder dict
            if predicted_index < len(class_names):
                 predicted_class_name = class_names[predicted_index]
            else:
                 predicted_class_name = "Unknown Disease"

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
    # Make sure to create the Data directory if it doesn't exist relative to app.py
    if not os.path.exists("Data"):
        print("Warning: 'Data' directory not found. PDF loading might fail if paths are relative.")
        # Consider creating it or ensuring absolute paths are used in pdf_files list

    # Ensure the model is loaded before starting the app
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True) # Listen on all interfaces

