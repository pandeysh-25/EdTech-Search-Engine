# CS6513_Group_Project
CS6513_Group_Project

## Project Structure

- `main.py`: The main Streamlit application file. This is the entry point for the frontend of the Intelligent Information Aggregation Engine.
- `QAYouTubeSearchClient.py`: A client module to interact with the backend QA and YouTube search services.
- `embedding_search_backend/`: Directory containing the backend logic for embedding-based search for QA and YouTube videos.
- `data_process/`: Directory likely containing scripts or modules for data preprocessing and preparation.
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
