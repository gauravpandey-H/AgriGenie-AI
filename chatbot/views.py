from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
import os
from dotenv import load_dotenv
from .models import ChatHistory

# Load environment variables
load_dotenv()

@login_required
def chat_interface(request):
    """Renders the Chatbot UI"""
    return render(request, 'chatbot/chat.html')

@login_required
def chat_api(request):
    """API Endpoint to process chat messages via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({'error': 'Empty message'}, status=400)
            
            # Retrieve past chat history for context (last 5 messages)
            history = []
            if hasattr(request.user, 'farmer'):
                recent_chats = ChatHistory.objects.filter(farmer=request.user.farmer).order_by('-timestamp')[:5]
                history = list(reversed(recent_chats))
            
            # Intelligent AI Logic
            bot_response = generate_ai_response(user_message, history)
            
            # Save to Database (Skip if user is a superadmin without a farmer profile)
            if hasattr(request.user, 'farmer'):
                ChatHistory.objects.create(
                    farmer=request.user.farmer,
                    user_message=user_message,
                    bot_response=bot_response
                )
            
            return JsonResponse({'response': bot_response})
        except Exception as e:
            print(f"Chatbot Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def generate_mock_fallback(message, history):
    try:
        import requests
        
        messages = [
            {"role": "system", "content": "You are AgriGenie, a highly intelligent and friendly AI farming assistant. You specialize in crop recommendations, weather impacts, soil health, plant diseases, and market prices. Keep your responses concise, practical, and conversational, just like ChatGPT."}
        ]
        
        # Add history to context
        for chat in history:
            messages.append({"role": "user", "content": chat.user_message})
            messages.append({"role": "assistant", "content": chat.bot_response})
            
        messages.append({"role": "user", "content": message})
        
        # Use pollinations.ai for ultra-fast, keyless, free LLM text generation
        response = requests.post('https://text.pollinations.ai/', json={'messages': messages}, timeout=10)
        
        if response.status_code == 200:
            # Safely handle encoding so UI doesn't crash on special characters
            response.encoding = 'utf-8'
            return response.text
        raise Exception("API returned non-200 status")
    except Exception as e:
        print(f"Fallback Error: {e}")
        message_lower = message.lower()
        if any(word in message_lower for word in ['hi', 'hello', 'hey']):
            return "Hello! I am AgriGenie. (Offline Mode Active)"
        elif 'weather' in message_lower:
            return "The current weather is mostly sunny at 28°C."
        elif 'crop' in message_lower:
            return "Wheat and Maize are highly recommended right now."
        else:
            return "As an AI farming assistant, I specialize in crop recommendations, weather, and diseases. How can I help you?"

def generate_ai_response(message, history):
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "your_api_key_here":
        return generate_mock_fallback(message, history)
    
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        
        system_instruction = (
            "You are AgriGenie, a highly intelligent and friendly AI farming assistant. "
            "You specialize in crop recommendations, weather impacts, soil health, plant diseases, and market prices. "
            "Keep your responses concise, practical, and conversational, similar to ChatGPT but tailored for farmers. "
            "Use bullet points if necessary. Do not output markdown code blocks unless writing code. "
        )
        
        # Convert history for Gemini
        contents = []
        for chat in history:
            contents.append(types.Content(role="user", parts=[types.Part.from_text(text=chat.user_message)]))
            contents.append(types.Content(role="model", parts=[types.Part.from_text(text=chat.bot_response)]))
        
        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=message)]))
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )
        
        return response.text
    except Exception as e:
        return generate_mock_fallback(message, history)

