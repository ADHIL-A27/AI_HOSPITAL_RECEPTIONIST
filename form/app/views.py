# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# import os
# import google.generativeai as genai
# from gtts import gTTS
# from playsound import playsound
# import os
# import time
# import threading
# import uuid


# # Set your Google API key once
# GOOGLE_API_KEY = "AIzaSyC7Z9xyqpMofKgYsNXYNXw6AzJ65O1kdlk"
# os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# # Configure the generative model with the API key
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")


# def play_audio(temp_filename):
#     playsound(temp_filename)

# def speak(text):


#     tts = gTTS(text=text, lang='ml')
    
#     # Generate a unique filename using uuid
#     temp_filename = f"temp_audio_{uuid.uuid4()}.mp3"  
#     tts.save(temp_filename)  

#     # Use threading to play the audio
#     audio_thread = threading.Thread(target=play_audio, args=(temp_filename,))
#     audio_thread.start()  # Start playing the audio in a separate thread

#     # Wait for the audio to finish playing before removing the file
#     audio_thread.join()  # Wait for the thread to complete
#     os.remove(temp_filename)  # Remove the temp file after playing



# def get_text_file_content():
#     # Specify your text file path
#     file_path = 'qmark.txt'
    
#     try:
#         with open(file_path, 'r') as file:
#             return file.read().strip()  # Return the entire content of the file, stripped of leading/trailing whitespace
#     except Exception as e:
#         print(f"Error reading the file: {e}")
#         return None  # Return None if there's an error

# def clean_text(text):
#     # Remove unwanted characters or symbols from the text
#     return ''.join(char for char in text if char.isalnum() or char.isspace())

# def genresponse(question):

#      # Load the text file content
#         text_file_content = get_text_file_content()

 
#         # Combine the user message with the text file content
#         prompt = (
#             f"Act as a friendly and helpful hospital receptionist. Answer the following question clearly and accurately, "
#             f"based strictly on the provided hospital details. Use simple, polite Malayalam that patients can easily understand. "
#             f"Do not use special characters like *, _, or emojis. Ensure the answer is concise but informative, "
#             f"and provide only relevant information from the context.\n\n"
#             f"Question: {question}\n"
#             f"Context: {text_file_content}\n"
#             f"Response in Malayalam:"
#         )



#         # Generate a response using the generative model
#         try:
#             response = model.generate_content(prompt).text.strip()
#             print(f"Generated Response: {response}")
#             return response  # Clean the output to remove unwanted characters
#         except:
#             return "model as something issue"


# def hello_world(request):
#     return render(request, 'helo.html')  # Ensure the template exists

# # Set your Google API key once


# @csrf_exempt  # Temporarily disable CSRF protection for this view; use with caution
# def send_message(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_message = data.get('message', '').strip()
#         print(user_message)

#         # Print the user message to the console
#         bot = genresponse(user_message)
#         speak(bot)
         
#         # You can also send a response back to the frontend if needed
#         return JsonResponse({'status': 'success', 'message':bot})

#     return JsonResponse({'status': 'fail', 'message': 'Invalid request'})


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import google.generativeai as genai
from gtts import gTTS
from playsound import playsound
import threading
import uuid


# Set your Google API key once
GOOGLE_API_KEY = "AIzaSyC7Z9xyqpMofKgYsNXYNXw6AzJ65O1kdlk"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Configure the generative model with the API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


def play_audio(temp_filename):
    playsound(temp_filename)
    # Remove the audio file after playing
    os.remove(temp_filename)

def speak(text):
    tts = gTTS(text=text, lang='ml')
    
    # Generate a unique filename using uuid
    temp_filename = f"temp_audio_{uuid.uuid4()}.mp3"
    tts.save(temp_filename)

    # Use threading to play the audio asynchronously
    audio_thread = threading.Thread(target=play_audio, args=(temp_filename,))
    audio_thread.start()  # Start the audio playback thread

def get_text_file_content():
    file_path = 'qmark.txt'
    
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def clean_text(text):
    return ''.join(char for char in text if char.isalnum() or char.isspace())

def genresponse(question):
    text_file_content = get_text_file_content()

    prompt = (
            f"Act as a friendly and helpful hospital receptionist. Answer the following question clearly and accurately, "
            f"based strictly on the provided hospital details. Use simple, polite Malayalam that patients can easily understand. "
            f"Do not use special characters like *, _, or emojis. Ensure the answer is concise but informative, "
            f"and provide only relevant information from the context.\n\n"
            f"Question: {question}\n"
            f"Context: {text_file_content}\n"
            f"Response in Malayalam:"
        )


    try:
        response = model.generate_content(prompt).text.strip()
        print(f"Generated Response: {response}")
        return response
    except:
        return "model as something issue"

def hello_world(request):
    return render(request, 'helo.html')

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        # Generate bot response
        bot_response = genresponse(user_message)

        # Start a thread to play the audio while sending the text response immediately
        threading.Thread(target=speak, args=(bot_response,)).start()

        # Send JSON response immediately after generating the text response
        return JsonResponse({'status': 'success', 'message': bot_response})

    return JsonResponse({'status': 'fail', 'message': 'Invalid request'})
