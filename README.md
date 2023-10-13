# chatbot-development
## Installation
Python3 must be already installed

```
git clone https://github.com/alina-boichenko/task-chatbot-development.git
cd task-chatbot-development
python3 -m venv venv

# on Windows
venv\Scripts\activate

# on macOS
source venv/bin/activate 

pip install -r requirement.txt

```

Install spaCy

```
pip install -U spacy
python -m spacy download en_core_web_sm
```

Install Whisper

```
pip install -U openai-whisper

# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

```
You need to register at https://openai.com and get OPENAI_API_KEY from there.

You also need to register at https://www.weatherapi.com and get WEATHER_API.

The next step is to create a chatbot in telegram. Use @BotFather in telegram and get BOT_TOKEN from there.

## Setting environment variables

Create an empty file .env in the following path: task-chatbot-development/.env. Copy the entire content of the .env.sample file and paste it into the .env file. Modify the placeholders in the .env file with the actual environment variables. For example (but don`t use "< >" in your project):
```
WEATHER_API=<your key>
```

## Run in terminal

```python3 main.py```

## Features
1. You can start conversation with a chatbot, use command `/start`. A chatbot can answer the following questions (examples):
- What is the weather like in Madrid tomorrow?
- Is it warm in Berlin after tomorrow?
- Is wind expected in London today?

2. Send an audio file. The chatbot transcribes the content and transmits its content in text format.
