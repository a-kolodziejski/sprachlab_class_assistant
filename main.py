import gradio as gr
from openai_utils import get_gpt_reply
from speech_utils import recognize_speech_from_audio, synthesize_speech

# Inicjalizacja historii rozmowy
chat_history = []

# Funkcja do rozpoczęcia rozmowy na określony temat
def start_conversation(topic):
    """
    Funkcja do rozpoczęcia rozmowy na określony temat.
    Args:
        topic (str): Temat rozmowy.
    """
    # Dobierz się do globalnej zmiennej chat_history
    global chat_history
    # Ustaw system prompt z tematem rozmowy
    system_prompt = f"Du bist ein freundlicher deutscher Gesprächspartner. Führe ein lockeres Gespräch auf Deutsch über das Thema: {topic}."
    # Ustaw historię rozmowy z system prompt
    chat_history = [{"role": "system", "content": system_prompt}]
    print(chat_history)
    return f"Das Thema wurde gesetzt: {topic}"

def handle_input(audio_path):
    """
    Funkcja do obsługi wejścia audio, rozpoznawania mowy i generowania odpowiedzi GPT.
    Args:
        audio_path (str): Ścieżka do pliku audio z nagraniem użytkownika.
    """
    # Dobierz się do globalnej zmiennej chat_history
    global chat_history
    # Rozpoznaj mowę z pliku audio
    user_message = recognize_speech_from_audio(audio_path)
    # Dodaj odpowiedz użytkownika do historii rozmowy
    chat_history.append({"role": "user", "content": user_message})
    # Orzymaj odpowiedź GPT na podstawie historii rozmowy
    gpt_reply = get_gpt_reply(chat_history)
    # Zaktualizuj historię rozmowy o odpowiedź GPT
    chat_history.append({"role": "assistant", "content": gpt_reply})
    # Syntezuj odpowiedź głosową z tekstu GPT
    tts_path = synthesize_speech(gpt_reply)
    # Zwróć transkrypcję użytkownika, odpowiedź GPT i ścieżkę do pliku audio
    return user_message, gpt_reply, tts_path

with gr.Blocks() as demo:
    gr.Markdown("# 💬 Deutsch AI Chat – mit Stimme")

    topic_input = gr.Textbox(label="Gib das Thema ein (z.B. Umwelt, Reisen, Geschichte)")
    set_topic_btn = gr.Button("Starte Gespräch")

    audio_input = gr.Audio(sources="microphone", type="filepath", label="Sprich hier (Deutsch)")
    user_text = gr.Textbox(label="🗣️ Was hast du gesagt?", interactive=False)
    bot_text = gr.Textbox(label="🤖 Antwort von GPT", interactive=False)
    audio_output = gr.Audio(label="🎧 Antwort anhören")

    set_topic_btn.click(start_conversation, inputs=topic_input, outputs=None)
    audio_input.change(handle_input, inputs=audio_input, outputs=[user_text, bot_text, audio_output])

demo.launch()
