# CS6513_Group_Project
CS6513_Group_Project

## Project Structure

- `main.py`: The main Streamlit application file. This is the entry point for the frontend of the Intelligent Information Aggregation Engine.
- `QAYouTubeSearchClient.py`: A client module to interact with the backend QA and YouTube search services.
- `embedding_search_backend/`: Directory containing the backend logic for embedding-based search for QA and YouTube videos.
- `data_process/`: Directory containing scripts or modules for data preprocessing and preparation using spark.
- `README.md`: This file, providing an overview of the project.

## `main.py` Overview

`main.py` serves as the user interface for the "Intelligent Information Aggregation Engine". It is built using Streamlit.

Key functionalities include:
- Providing a text input field for users to ask questions.
- Utilizing `QAYouTubeSearchClient.py` to send the user's query to a backend service.
- Receiving structured QA results and YouTube video suggestions from the backend.
- Calling the OpenAI API to generate a concise summary based on the retrieved QA and YouTube information.
- Displaying the AI-generated summary, detailed QA pairs, and related YouTube videos to the user in a clear and organized manner.
- Handling potential errors such as API key issues or service unavailability.

The application aims to provide users with a quick and comprehensive understanding of their queries by aggregating information from different sources and summarizing key insights.

## Startup Sequence

To run the application, please follow these steps in order:

1.  **Configure and Start Backend Service:**
    *   Open the `embedding_search_backend/Faiss_server.ipynb` notebook.
    *   Fill in your NGROK_AUTHTOKEN in the designated cell: `os.environ['NGROK_AUTHTOKEN'] = "YOUR_NGROK_AUTHTOKEN_HERE"`
    *   Ensure the ngrok hostname is correctly set for your desired domain in the cell running `ngrok.connect()`: `public_url_obj = ngrok.connect(5000, hostname="your-chosen-domain.ngrok-free.app")`
    *   Run all cells in the notebook to start the backend FAISS server. This will also expose a public URL via ngrok.

2.  **Configure and Start Frontend Application:**
    *   Open the `main.py` file.
    *   Set your Ngrok authentication token in `main.py`: `NGROK_AUTHTOKEN = 'YOUR_NGROK_AUTHTOKEN_HERE'` 
    *   Set your OpenAI API key in `main.py`: `PRESET_OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"`
    *   Ensure the `PRESET_BASE_URL` in `main.py` points to the public URL provided by the ngrok tunnel of your backend service (from `Faiss_server.ipynb` in step 1). For example: `PRESET_BASE_URL = "https://your-chosen-domain.ngrok-free.app"`
    *   Run the Streamlit application: `streamlit run main.py`

**Dependencies:**
*   The `requirements.txt` file in the root directory lists the dependencies for the frontend application (`main.py` and `QAYouTubeSearchClient.py`). You can install them using: `pip install -r requirements.txt`
*   For the backend service (`embedding_search_backend/Faiss_server.ipynb`), please follow the `pip install` instructions within the notebook cells to install necessary packages like `pyngrok`, `flask`, `pyspark`, `spark-nlp`, and `faiss-cpu` in the notebook's environment.

Ensure all dependencies are installed as per the project requirements before starting the services.
