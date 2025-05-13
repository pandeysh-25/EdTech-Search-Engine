import requests
import json

class QAYouTubeSearchClient:
    """A client to interact with the combined QA and YouTube search service."""
    def __init__(self, base_url: str):
        """
        Initializes the QAYouTubeSearchClient.

        Args:
            base_url (str): The base URL of the combined QA and YouTube search service 
                          (e.g., your ngrok URL).
        """
        self.base_url = base_url.rstrip('/')
        self.search_endpoint = f"{self.base_url}/search"

    def search(self, query_text: str, k: int = 5):
        """
        Performs a search query against the combined QA and YouTube service.
        This is expected to return a dictionary with 'qa_results' and 'yt_results'.

        Args:
            query_text (str): The text to search for.
            k (int): The number of top results to return. Defaults to 5.

        Returns:
            dict | None: A dictionary containing 'qa_results' and 'yt_results'
                         (each being a list of search result dictionaries) if successful,
                         None otherwise.
        """
        params = {"query": query_text, "k": k}

        try:
            response = requests.get(self.search_endpoint, params=params, timeout=60)
            response.raise_for_status()
            
            results_dict = response.json()
            
            if isinstance(results_dict, dict) and \
               'qa_results' in results_dict and isinstance(results_dict['qa_results'], list) and \
               'yt_results' in results_dict and isinstance(results_dict['yt_results'], list):
                return results_dict
            else:
                print("Error: Response JSON does not have the expected structure ('qa_results' and 'yt_results' as lists).")
                print(f"Received: {json.dumps(results_dict, indent=2)}")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# --- Example Usage for Combined QA & YouTube Service ---
if __name__ == "__main__":
    current_ngrok_url = "https://novel-osprey-uncommon.ngrok-free.app"
    
    print(f"Attempting to connect to Combined QA & YouTube Search Service at: {current_ngrok_url}")
    client = QAYouTubeSearchClient(base_url=current_ngrok_url)

    print("\n--- Example Combined QA & YouTube Search ---")
    query1 = "how to bake cake?"
    k1 = 3
    combined_results = client.search(query_text=query1, k=k1)

    if combined_results:
        print("\n--- QA Results ---")
        qa_results = combined_results.get("qa_results", [])
        if qa_results:
            print(json.dumps(qa_results, indent=2))
            if len(qa_results) > 0:
                 top_qa_res = qa_results[0]
                 print(f"\n   Top QA result for '{query1}':")
                 print(f"     Rank: {top_qa_res.get('rank')}, QA ID: {top_qa_res.get('qa_id')}")
                 print(f"     Question: {str(top_qa_res.get('Question', ''))[:80]}...")
        else:
            print("No QA results found or an error in QA results part.")

        print("\n--- YouTube Results ---")
        yt_results = combined_results.get("yt_results", [])
        if yt_results:
            print(json.dumps(yt_results, indent=2))
            if len(yt_results) > 0:
                top_yt_res = yt_results[0]
                print(f"\n   Top YouTube result for '{query1}':")
                print(f"     Rank: {top_yt_res.get('rank')}, Video ID: {top_yt_res.get('video_id')}")
                print(f"     Title: {str(top_yt_res.get('title', ''))[:80]}...")
        else:
            print("No YouTube results found or an error in YouTube results part.")
            
    else:
        print(f"No results or an error occurred for query: '{query1}'")
        print("Please ensure your Colab script for the combined QA & YouTube service is running,")
        print("and the ngrok URL is correct and accessible if errors persist.")

    print("\n--- Test script for combined QA & YouTube service finished ---")
