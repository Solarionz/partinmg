import openai
import requests
import hashlib
import sys

# Paste your OpenAI API key between the quotes below
openai.api_key = "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"

# Replace this with the URL of the raw GitHub page you want to check
GITHUB_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/yourfile.py"

# Replace this with the path to the local .py file you want to update
LOCAL_FILE_PATH = "main.py"

# Download the contents of the GitHub page
response = requests.get(GITHUB_URL)

# Calculate the hash of the downloaded contents
new_hash = hashlib.sha256(response.content).hexdigest()

# Read the current hash from the local .py file
with open(LOCAL_FILE_PATH, "rb") as f:
    current_contents = f.read()
current_hash = hashlib.sha256(current_contents).hexdigest()

# If the hash has changed, update the local file
if new_hash != current_hash:
    print("An update is available for the app. Updating...")
    with open(LOCAL_FILE_PATH, "w") as f:
        f.write(response.text)
    print("Update successful. Open the updated app.")
else:
    print("Your file is already up to date.")

# Define the prompt to be fed to the AI
prompt = ("""Write a short story about a haunted house.

Once upon a time, there was a house on a hill. It was rumored to be haunted, and no one had lived there for years. One day, a brave family decided to move in despite the rumors. As soon as they entered the house, strange things began to happen. Doors would slam shut by themselves, and they could hear whispers in the night. The family soon realized that they were not alone in the house. """)

# Generate the AI's response to the prompt
try:
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=200,
        n=1,
        stop=None,
        timeout=15
    )
except openai.error.AuthenticationError as error:
    print("Error: Failed to authenticate with OpenAI API. Check your API key and try again.")
    sys.exit(1)
except openai.error.APIError as error:
    print(f"Error: {error}")
    sys.exit(1)

print(response.choices[0].text)
