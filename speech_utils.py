import speech_recognition as sr
from gtts import gTTS
import uuid


def recognize_speech_from_audio(audio_file):
    """
    Funkcja do rozpoznawania mowy z pliku audio i zwracania transkrypcji.
    
    Args:
        audio_file (str): Ścieżka do pliku audio, który ma być przetworzony.
    Returns:
        str: Transkrypcja rozpoznanej mowy w języku niemieckim lub komunikat o błędzie.
    """
    # Tworzy instancję rozpoznawacza mowy
    recognizer = sr.Recognizer()
    # Otwiera plik audio i przetwarza go
    with sr.AudioFile(audio_file) as source:
        # Odczytuje zawartosc pliku audio
        audio = recognizer.record(source)
    try:
        # Zwraca transkrypcję rozpoznanej mowy w języku niemieckim
        return recognizer.recognize_google(audio, language="de-DE")
    except sr.UnknownValueError:
        return "[Unverständlich]"
    except sr.RequestError as e:
        return f"[Fehler bei der Verbindung: {e}]"

def synthesize_speech(text, lang='de'):
    """
    Funkcja do syntezowania mowy z tekstu i zapisywania go jako plik MP3.
    
    Args:
        text (str): Tekst do syntezowania.
        lang (str): Język syntezowanej mowy (domyślnie 'de' dla niemieckiego).
    Returns:
        str: Nazwa pliku MP3, w którym zapisano syntezowaną mowę.
    """
    # Tworzy unikalną nazwę pliku na podstawie UUID
    filename = f"reply_{uuid.uuid4().hex}.mp3"
    # używa gTTS do syntezowania mowy
    tts = gTTS(text=text, lang=lang)
    # Zapisuje plik audio
    # Ustawia głośność na maksymalną
    tts.volume = 1.0  
    # Zapisuje plik audio
    tts.save(filename)
    # Zwraca nazwę pliku, aby można było go później odtworzyć lub usunąć
    return filename
