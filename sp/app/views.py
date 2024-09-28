from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
import pyttsx3
import json
import threading  # Import threading

def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()


    # Set the rate of speech (optional)
    engine.setProperty('rate', 120)  # Default is usually around 200

    # Speak the text
    engine.say(text)

    # Wait until the speaking is finished
    engine.runAndWait()

def hello_world(request):
    return render(request, 'helo.html')  # Ensure the template exists

# Set your Google API key once
GOOGLE_API_KEY = "AIzaSyC7Z9xyqpMofKgYsNXYNXw6AzJ65O1kdlk"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Configure the generative model with the API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def get_text_file_content():
    # Specify your text file path
    file_path = 'qmark.txt'
    
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()  # Return the entire content of the file, stripped of leading/trailing whitespace
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None  # Return None if there's an error

def clean_text(text):
    # Remove unwanted characters or symbols from the text
    return ''.join(char for char in text if char.isalnum() or char.isspace())

@csrf_exempt  # Temporarily disable CSRF protection for this view; use with caution
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        # Print the user message to the console
        print(f"User Message: {user_message}")

        # Load the text file content
        text_file_content = get_text_file_content()

        # If text file content is available, use it as context for the model
        if text_file_content:
            # Combine the user message with the text file content
            prompt = f"very Short answer the question: {clean_text(user_message)}\nFrom the context: {clean_text(text_file_content)}"
        else:
            prompt = clean_text(user_message)  # Fallback to just the user message if the file can't be read

        # Generate a response using the generative model
        try:
            response = model.generate_content(prompt).text.strip()
            print(f"Generated Response: {response}")
            bot_message = clean_text(response)  # Clean the output to remove unwanted characters
            
            # Return the bot message as a response first
            response_json = JsonResponse({
                'status': 'success',
                'user_message': user_message,
                'bot_message': bot_message
            })

            # Create a thread for the text-to-speech to run in the background
            threading.Thread(target=text_to_speech, args=(bot_message,)).start()

            return response_json
            
        except Exception as e:
            print(f"Error generating response: {e}")
            bot_message = "Sorry, I couldn't generate a response at this time."

            return JsonResponse({
                'status': 'fail',
                'message': bot_message
            })

    return JsonResponse({'status': 'fail', 'message': 'Invalid request'})
