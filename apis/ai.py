import requests
import os

API_KEY = os.getenv("GEMINI_API_KEY")

BASE_URL = "https://api.gemini.com/v1"  # Replace with actual Gemini AI endpoint

def send_task_to_gemini(task_title: str, task_description: str):
    """
    Sends task info to Gemini AI and returns processed response.
    """
    url = f"{BASE_URL}/process-task"  # replace with the actual endpoint
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": task_title
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Gemini API Error: {response.text}")
    return response.json()
