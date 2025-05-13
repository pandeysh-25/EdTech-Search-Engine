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

## Data Processing Pipelines

The `data_process/` directory contains critical pipelines for preprocessing and embedding generation, which form the foundation of the search capabilities. These notebooks create the vector embeddings that power the semantic search functionality in the backend.

### QA Dataset Processing

The `data_process/QA_dataset_process/` directory contains scripts for processing question-answer datasets:

- **`QA_text_embed.ipynb`**: This notebook processes QA data and generates embeddings for semantic search.
  - **Input**: Parquet files containing question-answer pairs (`data_qa_combined.parquet`)
  - **Process**: 
    1. Loads QA data from Parquet files
    2. Combines Question and Answer text with appropriate formatting
    3. Generates BERT sentence embeddings for the combined text using SparkNLP
    4. Stores both the embeddings and metadata in Parquet format
    5. Builds a FAISS index (Fast Approximate Nearest Neighbor Search) for efficient similarity search
  - **Output**:
    - `qa_combined_embeddings.parquet`: Contains the QA data with embedding vectors
    - `qa_combined_embeddings.index`: FAISS index file for rapid vector similarity search

### YouTube Dataset Processing

The `data_process/Youtube_dataset_process/` directory contains scripts for processing YouTube video data:

- **`Video_transcripts&titles_embed.ipynb`**: Processes video metadata and generates combined embeddings.
  - **Input**: JSON files containing YouTube video transcripts and titles
  - **Process**:
    1. Loads and parses JSON data containing video transcripts and titles
    2. Generates separate embeddings for video titles and transcripts
    3. Creates weighted average embeddings combining title (70%) and transcript (30%) vectors
    4. Builds a FAISS index for efficient search through video content
  - **Output**:
    - `combined_video_embeddings.parquet`: Video metadata with combined embedding vectors
    - `combined_video_embeddings.index`: FAISS index for video content search

- **`Video_frame_embed_part1.ipynb` & `Video_frame_embed_part2.ipynb`**: Generate embeddings for video frames for visual search.
  - **Input**: YouTube video IDs and frames extracted from videos
  - **Process**:
    1. Uses CLIP (Contrastive Language-Image Pre-Training) model to generate embeddings for video frames
    2. Processes batches of video frames to create visual embeddings
    3. Builds FAISS indices for visual similarity search
  - **Output**:
    - `video_embeddings.index`: FAISS index containing video frame embeddings
    - `metadata.pkl`: Metadata mapping embeddings to their respective videos

These data processing pipelines create the vector embeddings that enable both text-based and visual semantic search functionality. The embedding models convert text and images into high-dimensional vectors that capture semantic meaning, allowing the application to find content similar to user queries even when exact keyword matches aren't present.

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
