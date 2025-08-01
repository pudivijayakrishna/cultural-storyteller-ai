from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from sarvamai import SarvamAI, ChatCompletionRequestMessage_UserParams
from dotenv import load_dotenv
from pydub import AudioSegment
import io
import base64
import re
import traceback

# Load environment variables
# load_dotenv()  # Commented out due to .env file encoding issues

app = Flask(__name__)

# Configure CORS for Vercel deployment
CORS(app, origins=["*"])

# Get API key from environment variable
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY', 'sk_wxjx9cp5_R2uM1pYIhBNyaNakZd51Pf6l')

# Debug: Print API key status (without exposing the actual key)
print(f"API Key Status: {'Set' if SARVAM_API_KEY != 'YOUR_API_KEY_HERE' else 'NOT SET'}")
print(f"API Key Length: {len(SARVAM_API_KEY) if SARVAM_API_KEY != 'YOUR_API_KEY_HERE' else 'N/A'}")
print(f"API Key starts with: {SARVAM_API_KEY[:10]}..." if SARVAM_API_KEY != 'YOUR_API_KEY_HERE' else 'N/A')
if SARVAM_API_KEY == 'YOUR_API_KEY_HERE':
    print("WARNING: SARVAM_API_KEY environment variable is not set!")

# Initialize SarvamAI client
try:
    sarvam_client = SarvamAI(api_subscription_key=SARVAM_API_KEY)
    print("SarvamAI client initialized successfully")
except Exception as e:
    print(f"Error initializing SarvamAI client: {e}")
    sarvam_client = None

@app.route('/')
def home():
    return 'The Cultural Storyteller and Poet--AI Backend'

@app.route('/api/generate_content', methods=['POST', 'OPTIONS'])
def generate_content():
    if request.method == 'OPTIONS':
        return '', 204
    
    # Check if API key is set
    if SARVAM_API_KEY == 'YOUR_API_KEY_HERE':
        return jsonify({"error": "SARVAM_API_KEY environment variable is not set. Please set your API key."}), 500
    
    # Check if SarvamAI client is properly initialized
    if sarvam_client is None:
        return jsonify({"error": "SarvamAI client not initialized. Please check your API key."}), 500
    
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        language = data.get('language')
        content_type = data.get('content_type')
        
        if not prompt or not language or not content_type:
            return jsonify({"error": "Missing required fields: prompt, language, or content_type"}), 400
        
        # Validate language
        supported_languages = {'hi-IN', 'ta-IN', 'bn-IN', 'te-IN'}
        if language not in supported_languages:
            return jsonify({"error": f"Unsupported language: {language}"}), 400
        
        # Define system prompts
        poem_system_prompt = (
            f"The user's prompt may be in English or another language, but you MUST write your entire response exclusively in {language}. "
            f"You are a talented and lyrical poet who writes elegant, meaningful, and heartfelt poems in {language}. "
            "Write a complete and meaningful poem about the given topic. The poem should be longer and free-flowing, and can be formatted into paragraphs later."
        )
        
        story_system_prompt = (
            f"The user's prompt may be in English or another language, but you MUST write your entire response exclusively in {language}. "
            f"You are a skilled storyteller who writes short, engaging, and inspiring stories for children in {language}. "
            "Every story you write must be between 15 and 20 lines long and have a clear, easy-to-understand moral. "
            "The story must have a main character, a clear conflict, a resolution, and must make complete logical sense from start to finish. "
            "The story must be logically consistent and avoid including elements or events that are not related to the main plot. "
            "The narrative should have a clear, satisfying conclusion and not end abruptly. Do not include random, irrelevant characters."
        )
        
        simple_story_prompt = (
            f"The user's prompt may be in English or another language, but you MUST write your entire response exclusively in {language}. "
            f"You are a skilled storyteller who writes short, engaging, and inspiring stories for children in {language}. "
            "The story must be between 15 and 20 lines long and end with a clear, easy-to-understand moral. "
            "You have the creative freedom to create a unique and entertaining plot based on the user's prompt."
        )
        
        # Set up system messages and user messages based on content type
        if content_type == 'poem':
            system_message = poem_system_prompt
            temperature = 0.8
            user_message = f'Write a complete and meaningful poem about: {prompt}'
        elif content_type == 'story':
            if len(prompt) > 100 or any(keyword in prompt.lower() for keyword in ["plot", "story about", "character", "conflict", "resolution"]):
                system_message = story_system_prompt
                user_message = prompt
            else:
                system_message = simple_story_prompt
                user_message = f'Write a story about: {prompt}'
            temperature = 0.6
        else:
            return jsonify({"error": "Invalid content_type. Must be 'poem' or 'story'"}), 400
        
        # Generate text with continuation loop
        if content_type == 'story':
            full_story = ""
            max_story_length = 3000
            # Initial request: ask the AI to end the story with [END]
            chat_message = [
                ChatCompletionRequestMessage_UserParams(role="system", content=system_message),
                ChatCompletionRequestMessage_UserParams(role="user", content=user_message + " End the story with [END] when it is complete.")
            ]
            chat_response = sarvam_client.chat.completions(messages=chat_message, temperature=temperature)
            full_story += chat_response.choices[0].message.content
            # Loop until [END] is found or max length reached
            while "[END]" not in full_story and len(full_story) < max_story_length:
                continuation_prompt = f"Continue the story from the last sentence: {full_story} End the story with [END] when it is complete."
                chat_message = [
                    ChatCompletionRequestMessage_UserParams(role="system", content=system_message),
                    ChatCompletionRequestMessage_UserParams(role="user", content=continuation_prompt)
                ]
                chat_response = sarvam_client.chat.completions(messages=chat_message, temperature=temperature)
                full_story += chat_response.choices[0].message.content
            generated_text = full_story.replace("[END]", "").strip()
        else:
            generated_text = ""
            max_iterations = 10
            iteration = 0
            while iteration < max_iterations:
                print(f"Making API call to SarvamAI (iteration {iteration + 1})")
                print(f"Using API key: {SARVAM_API_KEY[:10]}...")
                print(f"Content type: {content_type}, Language: {language}")
                chat_response = sarvam_client.chat.completions(messages=chat_message, temperature=temperature)
                new_text = chat_response.choices[0].message.content
                generated_text += new_text
                print(f"Received response: {len(new_text)} characters")
                if generated_text.strip().endswith(('.', '!', '?')):
                    break
                chat_message = [
                    ChatCompletionRequestMessage_UserParams(role="system", content=system_message),
                    ChatCompletionRequestMessage_UserParams(role="user", content=f"Continue the following poem: {generated_text}")
                ]
                iteration += 1
            # Format poem if needed
            generated_text = format_poem(generated_text)
        
        # Generate audio
        if content_type in ['story', 'poem']:
            sentences = split_text_into_sentences(generated_text)
            audio_chunks = []
            for sentence in sentences:
                if sentence.strip():
                    tts_response = sarvam_client.text_to_speech.convert(
                        text=sentence,
                        target_language_code=language,
                        model='bulbul:v2',
                        output_audio_codec='wav'
                    )
                    if tts_response.audios:
                        audio_chunks.append(tts_response.audios[0])
            audio_base64 = combine_audio_chunks(audio_chunks)
        else:
            tts_response = sarvam_client.text_to_speech.convert(
                text=generated_text,
                target_language_code=language,
                model='bulbul:v2',
                output_audio_codec='wav'
            )
            audio_base64 = tts_response.audios[0] if tts_response.audios else None
        
        return jsonify({
            "generated_text": generated_text,
            "audio_base64": audio_base64
        })
        
    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

def format_poem(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if len(lines) < 8:
        import re
        sentences = re.split(r'(?<=[.!?]) +', text)
        lines = [s.strip() for s in sentences if s.strip()][:8]
    else:
        lines = lines[:8]
    
    para1 = '\n'.join(lines[:4])
    para2 = '\n'.join(lines[4:8])
    return f"{para1}\n\n{para2}" if para2 else para1

def split_text_into_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def combine_audio_chunks(audio_chunks):
    if not audio_chunks:
        return None
    
    final_audio = AudioSegment.empty()
    for chunk_base64 in audio_chunks:
        if chunk_base64:
            audio_data = base64.b64decode(chunk_base64)
            chunk_audio = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
            final_audio += chunk_audio
    
    output_buffer = io.BytesIO()
    final_audio.export(output_buffer, format="wav")
    output_buffer.seek(0)
    return base64.b64encode(output_buffer.getvalue()).decode('utf-8')

@app.errorhandler(Exception)
def handle_exception(e):
    print("Exception occurred:", e)
    traceback.print_exc()
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
