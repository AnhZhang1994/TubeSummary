#! /usr/bin/env python3
import re
import joblib
from deepmultilingualpunctuation import PunctuationModel
from transformers import pipeline
import requests
from pytube import YouTube
import openai
import os

if not os.path.exists("./case"):
    os.makedirs("./case")

model = PunctuationModel()


def main():
    get_metadata()
    chat("summary", result)
    with open("./case/" + "sum_" + yt.title + ".txt", "w") as f:
        f.write(response.json()['choices'][0]['message']['content'])


def get_metadata():
    url = input("Enter the URL of the YouTube video: ")
    #global yt
    yt = YouTube(url)
    # Print the video title
    print("Title:", yt.title)
    # Print the video description
    print("Description:", yt.description)
    # Print the video duration in seconds
    print("Duration (seconds):", yt.length)
    # Print the thumbnail URL
    print("Thumbnail URL:", yt.thumbnail_url)
    print(yt.captions)
    language = input("Enter the language code of the caption: ")
    caption = yt.captions.get_by_language_code(language)
    content = re.sub('<.*?>', '', caption.xml_captions)
    global result
    result = model.restore_punctuation(content)

    with open("./case/" + yt.title + ".txt", "w") as f:
        f.write(result)


def chat(prompt, text):
    API_KEY = 'yourOwnKey'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }
    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    }
    #global response
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    return response.json()['choices'][0]['message']['content']



if __name__ == "__main__":
    main()
   