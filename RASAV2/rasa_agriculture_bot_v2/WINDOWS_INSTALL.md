# Windows Installation Guide for RASA Agriculture Chatbot

This guide provides specific instructions for installing the RASA Agriculture Chatbot on Windows systems, addressing common installation issues.

## Prerequisites

- Python 3.8 or 3.9 (recommended for best compatibility)
- Visual C++ Build Tools (required for some Python packages)

## Installation Steps

### 1. Install Visual C++ Build Tools

Some Python packages require compilation. Install the Visual C++ build tools:

1. Download the [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Run the installer and select "C++ build tools" 
3. Complete the installation

### 2. Create a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install the requirements
pip install -r requirements.txt
```

### 4. Troubleshooting Common Issues

#### Issue: Error installing blis or other Cython packages

If you encounter errors with blis or other Cython-based packages:

```bash
# Install a pre-built wheel for spaCy
pip install spacy==3.4.4

# Download a small English model
python -m spacy download en_core_web_sm
```

#### Issue: TensorFlow installation problems

If TensorFlow installation fails:

```bash
# Install a specific version known to work on Windows
pip install tensorflow==2.8.0
```

## Starting the Bot

After successful installation:

1. Train the model:
```bash
rasa train
```

2. Start the action server (in a separate terminal):
```bash
rasa run actions
```

3. Start the RASA server:
```bash
rasa run --enable-api --cors "*"
```

4. For interactive testing:
```bash
rasa shell
```

## Additional Resources

- [RASA Installation Guide](https://rasa.com/docs/rasa/installation/)
- [Windows-specific Python Package Issues](https://wiki.python.org/moin/WindowsCompilers)
