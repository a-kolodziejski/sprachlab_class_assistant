import openai

# Odczytaj klucz API z pliku
with open("api_key.txt", "r") as file:
    api_key = file.read().strip()
    
# Ustaw klucz API
openai.api_key = api_key

def get_gpt_reply(history):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=history,
        temperature=0.8,
        max_tokens=500
    )
    return response['choices'][0]['message']['content']