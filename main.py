"""
pip install flask
pip install requests
pip install json
pip install os
pip install subprocess
pip install argparse
pip install whisper
pip install ollama
"""
import threading
from flask import Flask, request, redirect, url_for, jsonify
import os
import ollama
import os
import requests
import json
import subprocess
#from transcribe import transcribe_audio  # Import the function
import requests
import json
import whisper
import argparse

NOTION_KEY = "notion key here"
headers = {'Authorization': f"Bearer {NOTION_KEY}",
           'Content-Type': 'application/json',
           'Notion-Version': '2022-06-28'}

def transcribe_audio(FilePathForUpload):
    model = whisper.load_model("base")

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(FilePathForUpload)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)

    # post the recognized text to a Discord webhook
    post_to_discord("discord webhook", result.text)
    AIoutput = chat_with_ai("summarise the following text in bullet points"+result.text)
    post_to_discord("discord webhook", AIoutput)
    titlefromai = chat_with_ai("discord webhook"+result.text)
    post_to_discord("discord webhook", titlefromai)

    create_notion_page(titlefromai, result.text+"\n"+AIoutput)

def post_to_discord(webhook_url, content):
    data = {
        "content": content
    }
    response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    return response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():


    if request.method == 'POST':
        file = request.files['file']
        if file:
            post_to_discord("discord webhook", "file uploaded")
            filename = file.filename
            file_path = os.path.join('C:\\Users\\calvi\\PycharmProjects\\whisper transcribe server on server part2\\UploadedFiles', filename)
            file.save(file_path)
            uploaded_file_string = file_path  # New variable
            print(file_path)

            # Start a new thread for the transcription process
            threading.Thread(target=transcribe_audio, args=(str(uploaded_file_string),)).start()

            # Immediately return a response to the client
            return redirect(url_for('upload_file'))

    return '''
    <!doctype html>
    <title>Upload a File</title>
    <h1>Upload a File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def chat_with_ai(user_message):
    # Ensure the user message is not empty
    if not user_message:
        return 'No message provided'

    try:
        # Call the Ollama chat API with the user message
        response = ollama.chat(model='llama3:8b', messages=[
            {
                'role': 'user',
                'content': user_message,
            },
        ])

        # Extract the AI response
        ai_response = response['message']['content']

        # Return the AI response as a string
        return ai_response

    except Exception as e:
        # Handle potential errors
        return str(e)

def chat_with_phi(user_message):
    # Ensure the user message is not empty
    if not user_message:
        return 'No message provided'

    try:
        # Call the Ollama chat API with the user message
        response = ollama.chat(model='phi3', messages=[
            {
                'role': 'user',
                'content': user_message,
            },
        ])

        # Extract the AI response
        ai_response = response['message']['content']

        # Return the AI response as a string
        return ai_response

    except Exception as e:
        # Handle potential errors
        return str(e)

def create_notion_page(title, content):
    # Specify the fixed page_id of the parent page
    page_id = "page id for notion output"

    create_page_body = {
        "parent": { "page_id": page_id },
        "properties": {
            "title": {
                "title": [{
                    "type": "text",
                    "text": { "content": title }
                }]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": content
                        }
                    }]
                }
            }
        ]
    }

    create_response = requests.post(
        "https://api.notion.com/v1/pages",
        json=create_page_body, headers=headers)
    print(create_response.json())
#create_notion_page("title here", "body here")

def get_page_id(page_title):
    search_params = {"query": page_title, "filter": {"value": "page", "property": "object"}}
    search_response = requests.post(
        'https://api.notion.com/v1/search',
        json=search_params, headers=headers)

    search_results = search_response.json()["results"]
    if search_results:
        return search_results[0]["id"]
    else:
        return None

#parent_page_id = get_page_id("Output for whisper server")
#print(parent_page_id)
if __name__ == '__main__':
    app.run(debug=False, port=1987)
#create_notion_page("My New Page", "This is the content of my new page.")