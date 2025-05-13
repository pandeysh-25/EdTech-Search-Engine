'''
EDU_Search/main.py
Streamlit application for QA and YouTube search with OpenAI summarization.
'''
import streamlit as st
from openai import OpenAI, APIConnectionError, AuthenticationError
from QAYouTubeSearchClient import QAYouTubeSearchClient
import os
from pyngrok import ngrok, conf as ngrok_conf

def get_openai_summary(api_key: str, qa_results: list, yt_results: list, query: str):
    '''
    Uses OpenAI to summarize the QA and YouTube results.
    '''
    if not qa_results and not yt_results:
        return "No relevant information found to summarize."

    client = OpenAI(api_key=api_key)
    
    prompt_content = f"User question: {query}\n\n"
    prompt_content += "Based on the following Question-Answering (QA) and YouTube video information, please provide a concise summary for the user, appropriately combining content from both sources to answer the user's question.\n\n"

    if qa_results:
        prompt_content += "--- QA Results ---\n"
        for i, qa in enumerate(qa_results[:3]):
            answer_text = qa.get('Answer', 'N/A')
            prompt_content += f"QA {i+1}: Question: {qa.get('Question', 'N/A')}\nAnswer: {answer_text[:500] + '...' if len(answer_text) > 500 else answer_text}\n\n"
    else:
        prompt_content += "--- QA Results ---\nNo relevant QA content found.\n\n"

    if yt_results:
        prompt_content += "--- YouTube Video Results ---\n"
        for i, yt in enumerate(yt_results[:3]):
            prompt_content += f"Video {i+1}: Title: {yt.get('title', 'N/A')}\n"
            prompt_content += "\n"
    else:
        prompt_content += "--- YouTube Video Results ---\nNo relevant YouTube videos found.\n\n"
    
    prompt_content += "Please provide a comprehensive answer and summary:"

    try:
        response = client.chat.completions.create(
            model="o4-mini-2025-04-16",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant, skilled at summarizing information from provided materials and answering user questions."},
                {"role": "user", "content": prompt_content}
            ]
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        st.error(f"OpenAI API call failed: {e}")
        return "Summary generation failed."

st.set_page_config(layout="wide", page_title="Intelligent Information Aggregation Engine")

# --- Ngrok Setup ---
STREAMLIT_PORT = 8501
NGROK_AUTHTOKEN = ''

public_url = ""
if NGROK_AUTHTOKEN:
    try:
        ngrok_conf.get_default().auth_token = NGROK_AUTHTOKEN
        # Disconnect any existing tunnels
        for tunnel in ngrok.get_tunnels():
            if tunnel.proto == "http" or tunnel.proto == "https":
                ngrok.disconnect(tunnel.public_url)
        # Connect to Streamlit port
        public_url = ngrok.connect(STREAMLIT_PORT, bind_tls=True, domain="cs6513edu.ngrok.app").public_url
    except Exception as e:
        st.error(f"Ngrok connection failed: {e}. Ensure ngrok is installed and NGROK_AUTHTOKEN is set correctly.")
        st.warning("Proceeding with local access only.")
elif os.environ.get("CODESPACES") == "true" or os.environ.get("GITPOD_WORKSPACE_URL") == "true":
    pass
else:
    st.info("💡 To expose this app publicly, set your NGROK_AUTHTOKEN environment variable and restart.")

# --- Backend Configuration ---
PRESET_BASE_URL = "https://novel-osprey-uncommon.ngrok-free.app"
PRESET_OPENAI_API_KEY = ""

# --- Application Title and Main Search Area ---
st.title("🔍 Educational Information Search Engine")
st.markdown("Enter your question to get answers and related information sources.")

# --- User Input ---
query_text = st.text_input("", placeholder="For example: What is photosynthesis?", label_visibility="collapsed")
k_results_default = 3

if query_text:
    if PRESET_BASE_URL == "YOUR_QA_YOUTUBE_SERVICE_NGROK_URL_HERE" or not PRESET_BASE_URL:
        st.error("Error: QA & YouTube service address is not configured in the code. Please contact the administrator.")
    elif not PRESET_OPENAI_API_KEY:
        st.error("Error: OpenAI API key is not set in the environment variable OPENAI_API_KEY. Please set this environment variable and restart the application.")
    elif not PRESET_OPENAI_API_KEY.startswith("sk-"):
        st.error("Error: OpenAI API key loaded from environment variable has an incorrect format. Please check the value of OPENAI_API_KEY.")
    else:
        try:
            client_qa_yt = QAYouTubeSearchClient(base_url=PRESET_BASE_URL)
            with st.spinner(f'Aggregating information for "{query_text}"...'):
                combined_results = client_qa_yt.search(query_text=query_text, k=k_results_default)

            if combined_results:
                qa_results = combined_results.get("qa_results", [])
                yt_results = combined_results.get("yt_results", [])
                
                st.success("Information aggregation complete!")

                # OpenAI Summary
                with st.spinner("Extracting key insights for you..."):
                    summary = get_openai_summary(PRESET_OPENAI_API_KEY, qa_results, yt_results, query_text)
                
                st.markdown("## 💡 Summary:")
                st.markdown(summary)
                st.markdown("<hr style='margin-top: 1.5rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
                
                if qa_results or yt_results:
                    st.markdown("### Detailed Information Sources")

                col1, col2 = st.columns(2)

                with col1:
                    if qa_results:
                        st.markdown("#### 📚 Related Q&A")
                        for i, res in enumerate(qa_results):
                            with st.container():
                                st.markdown("**Question:**")
                                st.markdown(f"**{res.get('Question', 'N/A')}**")
                                st.markdown("**Answer:**")
                                answer_text = res.get('Answer', 'N/A')
                                st.markdown(f"<div style='max-height: 500px; overflow-y: auto; padding: 5px; border: 1px solid #ddd;'>{answer_text}</div>", unsafe_allow_html=True)
                                if res.get('Level'):
                                    st.caption(f"Level: {res.get('Level', 'N/A')}")
                                if res.get('similarity'): 
                                    st.caption(f"Similarity: {res.get('similarity')}")
                                st.markdown("<hr style='margin-top: 1.5rem; margin-bottom: 1.5rem; border-top: 4px solid #ddd;'>", unsafe_allow_html=True)
                    else:
                        with col1:
                            if yt_results:
                                pass
                            else:
                                st.info("No relevant Q&A results found.")
                
                with col2:
                    if yt_results:
                        st.markdown("#### 🎬 Related Videos")
                        for i, res in enumerate(yt_results):
                            with st.container():
                                video_id = res.get('video_id', 'N/A')
                                st.markdown(f"**[{res.get('title', 'N/A')}](https://www.youtube.com/watch?v={video_id})**")
                                if res.get('similarity'): 
                                    st.caption(f"Similarity: {res.get('similarity')}")
                                if video_id != 'N/A':
                                    st.video(f"https://www.youtube.com/watch?v={video_id}")
                                st.markdown("<hr style='margin-top: 0.5rem; margin-bottom: 0.5rem;'>", unsafe_allow_html=True)
                    else:
                        with col2:
                            if qa_results:
                                pass
                            else:
                                st.info("No relevant YouTube videos found.")
            else:
                st.error(f"Failed to retrieve results from the service. Please check if the service address is correct and the backend service is running.")
        
        except ImportError:
            st.error("Error: `QAYouTubeSearchClient` not found. Please ensure `QAYouTubeSearchClient.py` is in the same directory as `main.py`, or correctly installed.")
        except APIConnectionError as e: 
            st.error(f"OpenAI API connection error: {e}. Please check your network connection and API key.")
        except AuthenticationError as e: 
            st.error(f"OpenAI API authentication failed: {e}. Please ensure your OpenAI API key is correct and valid.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
