# KrishiAI - RAG Module

KrishiAI is a Retrieval Augmented Generation (RAG) module designed to provide information and assistance related to agriculture. It leverages a knowledge base built from PDF documents to answer user queries and includes a placeholder for image-based plant disease detection.

## Table of Contents

- [Features](#features)

- [Project Structure](#project-structure)

- [Setup and Installation](#setup-and-installation)

- [Usage](#usage)

- [Image-based Disease Detection (Placeholder)](#image-based-disease-detection-placeholder)

## Features

- **Agricultural Q&A:** Answers user questions based on information extracted from provided PDF documents related to agriculture.

- **Retrieval Augmented Generation (RAG):** Utilizes a RAG architecture to fetch relevant information before generating responses.

- **Vector Store:** Employs ChromaDB for efficient storage and retrieval of document embeddings.

- **Language Model Integration:** Integrates with OpenRouter for large language model capabilities.

- **Web Interface:** Provides a simple web-based chat interface for user interaction.

- **Placeholder Image Analysis:** Includes a basic placeholder for image-based plant disease detection, demonstrating where such functionality would be integrated.

## Project Structure

The project is organized into the following directories and files:

```
RAG Module/
├── Data/                     # Contains PDF documents used for the knowledge base
│   ├── farmerbook.pdf
│   ├── final.pdf
│   ├── handbook_01_rice_cultivation.pdf
│   ├── IndianAgriculture.pdf
│   └── KrishiAI.pdf
├── config/                   # Configuration files
│   └── neo4j_config.yaml     # Neo4j database configuration (currently not used in the provided code)
├── static/                   # Static web assets (CSS, JavaScript, images)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── index.js
│   ├── background.jpg
│   ├── background2.jpg
│   ├── background3.jpg
│   ├── interface.png
│   ├── logo.png
│   ├── logo1.jpeg
│   ├── logo2.jpeg
│   ├── robo.png
│   └── user.png
├── templates/                # HTML templates for the web interface
│   ├── index.html
│   └── modified_index.html
├── app_tf_free.py            # Main Flask application, handles web routes and integrates RAG and image analysis
├── chat1.py                  # Functions for PDF text extraction, text splitting, and vector store initialization
├── chat2.py                  # Functions for setting up the RetrievalQA chain with the language model
├── requirements.txt          # Python dependencies
└── README.md                 # This README file
```

## Setup and Installation

To set up and run the KrishiAI RAG Module, follow these steps:

1. **Clone the repository .**

1. **Install Python Dependencies present in requirements.txt file:**
It is highly recommended to use a virtual environment to manage dependencies.

1. **Prepare PDF Data:**
Place your agricultural PDF documents in the `Data/` directory. The provided `app_tf_free.py` is configured to load the following PDFs:

- `handbook_01_rice_cultivation.pdf`

- `farmerbook.pdf`

- `final.pdf`

- `IndianAgriculture.pdf`

- `KrishiAI.pdf`

1. **Run the Flask Application:**
python app_tf_free.py

## Usage

Once the Flask application is running, open your web browser and navigate to `http://127.0.0.1:5000`

- **Text-based Q&A:** Type your agricultural questions into the chat interface and press Enter or click the send button. KrishiAI will retrieve relevant information from the loaded PDF documents and provide an answer.

- **Image-based Disease Detection:** You can upload an image of a plant to simulate disease detection. The current implementation uses a placeholder function that randomly assigns a disease or 'Healthy' status and provides generic advice. To use this feature, click the image upload button in the interface and select an image file (PNG, JPG, JPEG).

## Image-based Disease Detection 

The `app_tf_free.py` includes a `predict_disease` endpoint that accepts image uploads. The `analyze_plant_image_placeholder` function simulates disease detection.

## Configuration

- **OpenRouter API Key:** The `chat2.py` file uses an OpenRouter API key for the language model integration. You will need to replace the placeholder API key with your own valid key from OpenRouter.

## File Descriptions

This section provides a detailed overview of each significant file within the KrishiAI RAG Module, explaining its purpose and functionality.

### `app_tf_free.py`

This is the main Flask application file that orchestrates the web interface, handles user requests, and integrates the RAG capabilities with the image analysis placeholder. It defines the routes for the web application, including the home page (`/`), the chat endpoint (`/ask`), and the image prediction endpoint (`/predict_disease`). Key functionalities include:

- **Flask Application Setup:** Initializes the Flask app and configures the upload folder for images.

- **RAG Model Integration:** Loads PDF documents, extracts text, initializes the vector store (ChromaDB), and sets up the retrieval-augmented generation chain using `chat1.py` and `chat2.py`.

- **Chat Endpoint (****`/ask`****):** Processes text-based queries from the user, passes them to the RAG chain, and returns the generated agricultural information. It also includes predefined responses for specific queries.

- **Image Prediction Endpoint (****`/predict_disease`****):** Handles image uploads, performs a placeholder analysis for plant disease detection using `analyze_plant_image_placeholder`, and returns simulated disease information.



### `chat1.py`

This file is responsible for the data preparation and vector store initialization components of the RAG system. Its primary functions are:

- **`fetch_website_content(url)`****:** (Currently unused in `app_tf_free.py` but available) A utility function to fetch content from a given URL.

- **`extract_pdf_text(pdf_file)`****:** Extracts all text content from a specified PDF file using `PyPDF2`.

- **`split_text(text, chunk_size, chunk_overlap)`****:** Divides large blocks of text into smaller, manageable chunks using `RecursiveCharacterTextSplitter` from `langchain.text_splitter`. This is crucial for efficient retrieval in the RAG process.

- **`initialize_vector_store(contents)`****:** Takes a list of text contents (from PDFs), splits them into chunks, generates embeddings for these chunks using `SentenceTransformerEmbeddings` (specifically "all-MiniLM-L6-v2"), and stores them in a ChromaDB vector store. This vector store is then used by the RAG chain to find relevant information.

### `chat2.py`

This file focuses on setting up and configuring the Retrieval-Augmented Generation (RAG) chain, which combines the language model with the vector store for intelligent question answering. Its main component is:

- **`setup_retrieval_qa(db)`****:** This function takes the initialized ChromaDB vector store (`db`) as input and configures a `RetrievalQA` chain. It defines:
  - **Retriever:** Converts the ChromaDB into a retriever, enabling it to fetch relevant documents based on a similarity score threshold.
  - **Language Model (LLM):** Initializes `ChatOpenAI` (configured to use OpenRouter with a specific model like "openai/gpt-3.5-turbo") as the underlying language model for generating responses.
  - **Prompt Template:** Defines the system prompt for the LLM, instructing it to act as "KrishiAI," answer agriculture-related questions in simple words, keep answers concise (under 100 words), and explicitly state when information is not available in the provided context. It uses placeholders for `context` (retrieved documents) and `question` (user query).
  - **Chain Type:** Uses the `stuff` chain type, which concatenates all retrieved documents and passes them to the LLM as context.
  - **Verbose Mode:** Enabled for detailed logging during the chain's execution.

### `requirements.txt`

This file lists all the Python packages and their specific versions required to run the KrishiAI RAG Module. It ensures that all necessary dependencies are installed, preventing compatibility issues. Users should install these dependencies using `pip install -r requirements.txt`.

### `config/neo4j_config.yaml`

This YAML file contains configuration details for connecting to a Neo4j graph database, including URI, username, and password. Although present in the project structure, the current `app_tf_free.py` does not actively use this configuration. It serves as a placeholder for potential future integration with a Neo4j database for more complex knowledge graph functionalities.

### `Data/` Directory

This directory is the repository for all PDF documents that form the knowledge base for the RAG system. The `app_tf_free.py` specifically loads the PDF files found here to extract text and create embeddings for the vector store. The presence of these files is critical for the RAG module's ability to answer agricultural questions.

### `static/` Directory

This directory holds all static web assets required for the Flask application's user interface. It is further organized into subdirectories:

- **`static/css/style.css`****:** Contains the Cascading Style Sheets (CSS) rules that define the visual presentation and layout of the web pages, ensuring a consistent and appealing user interface.

- **`static/js/index.js`****:** Contains JavaScript code that adds interactivity and dynamic behavior to the web pages, such as handling chat messages, sending requests to the backend, and managing image uploads.

- **Image Files (****`.jpg`****, ****`.png`****, ****`.jpeg`****):** Includes various image assets like `background.jpg`, `interface.png`, `logo.png`, `robo.png`, and `user.png`. These images are used for the visual design of the web interface, including backgrounds, logos, and chat avatars.

### `templates/` Directory

This directory contains the HTML template files that define the structure and content of the web pages served by the Flask application. Flask uses these templates to render dynamic web content.

- **`templates/index.html`****:** The primary HTML template for the main chat interface.

- **`templates/modified_index.html`****:** An alternative or updated version of the `index.html` template, which `app_tf_free.py` is configured to use as the default landing page.

