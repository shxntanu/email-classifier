# Spam Detection Model

## Setup

1. Create and activate your virtual environment.

2. Install the dependencies:

    ```bash
    npm install
    ```

3. Install the required packages:

    ```bash
    pip install fastapi scikit-learn uvicorn imbalanced-learn nltk

    python3 -m nltk.downloader stopwords
    ```

4. In case of SSL error while downloading stopwords, run the following

    ```bash
    python3
    ```

    Then, once in the python3 shell, run the following

    ```python
    import nltk
        import ssl

        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        nltk.download()
    ```

   This will open a window where you can download the stopwords. Once downloaded, you can close the window and exit the python3 shell.

## Getting Started

To test this spam detection model, follow these steps:

1. Start the server:

    ```bash
    uvicorn spam_detection_api:app --reload --port 8001
    ```

3. You are all set 🎉
