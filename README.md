# Whisper-Transcribe-and-Summarise
A webserver that transcribes and summarises audio using ollama llama3 and outputs to notion and discord
---
# Audio Transcription Web Server

This project is a web server that transcribes audio using OpenAI's Whisper model, generates a summary and a title with Ollama's LLaMA3 model, and outputs the results to both Discord and Notion.

## Features

- **Audio Transcription**: Transcribes uploaded audio files using OpenAI's Whisper.
- **Text Summarization**: Generates summaries and titles for the transcribed text using Ollama's LLaMA3 model.
- **Discord Integration**: Sends transcribed and summarized text to a specified Discord webhook.
- **Notion Integration**: Creates a new page in Notion with the transcribed text and summary.

## Installation

1. Clone the repository.
2. Install the required dependencies:

    ```bash
    pip install flask
    pip install requests
    pip install json
    pip install os
    pip install subprocess
    pip install argparse
    pip install whisper
    pip install ollama
    ```

## Configuration

1. **Discord Webhook**: Set the Discord webhook URL in the `post_to_discord` function.
2. **Notion API**: Obtain a Notion API key and set the `NOTION_KEY` variable.
3. **Notion Parent Page ID**: Find the Notion parent page ID and update the `page_id` variable in `create_notion_page`.

## Usage

1. Start the web server:

    ```bash
    python server.py
    ```

2. Access the server's upload page at `http://localhost:1987/`.
3. Upload an audio file to start the transcription process.

## Contribution

Contributions are welcome! If you find a bug or have suggestions for features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

