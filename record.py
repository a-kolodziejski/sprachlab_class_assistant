import pyaudio
import wave
import threading
import tkinter as tk

# Globalne zmienne do kontrolowania nagrywania
is_recording = False
frames = []

def nagrywaj_audio():
    global is_recording, frames

    # Parametry nagrywania
    format = pyaudio.paInt16  # Format dźwięku
    kanały = 1  # Mono
    czestotliwosc = 44100  # Częstotliwość próbkowania
    rozmiar_bufora = 1024  # Rozmiar bufora

    # Inicjalizacja PyAudio
    audio = pyaudio.PyAudio()

    # Otwarcie strumienia do nagrywania
    stream = audio.open(format=format,
                        channels=kanały,
                        rate=czestotliwosc,
                        input=True,
                        frames_per_buffer=rozmiar_bufora)

    print("Nagrywanie...")

    frames = []  # Resetowanie listy frames

    # Nagrywanie aż do momentu, gdy is_recording stanie się False
    while is_recording:
        data = stream.read(rozmiar_bufora)
        frames.append(data)

    print("Nagrywanie zakończone.")

    # Zatrzymanie i zamknięcie strumienia
    stream.stop_stream()
    stream.close()
    audio.terminate()

def zapisz_audio(nazwa_pliku):
    global frames

    # Zapis nagrania do pliku WAV
    with wave.open(nazwa_pliku, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

    print(f"Nagranie zapisane jako {nazwa_pliku}")

def start_nagrywania():
    global is_recording
    if not is_recording:
        is_recording = True
        threading.Thread(target=nagrywaj_audio).start()

def stop_nagrywania():
    global is_recording
    if is_recording:
        is_recording = False

# Tworzenie interfejsu graficznego
root = tk.Tk()
root.title("Nagrywanie dźwięku")

# Przycisk do rozpoczęcia nagrywania
start_button = tk.Button(root, text="Rozpocznij nagrywanie", command=start_nagrywania)
start_button.pack(pady=10)

# Przycisk do zatrzymania nagrywania
stop_button = tk.Button(root, text="Zatrzymaj nagrywanie", command=stop_nagrywania)
stop_button.pack(pady=10)

# Przycisk do zapisania nagrania
save_button = tk.Button(root, text="Zapisz nagranie", command=lambda: zapisz_audio("nagranie.wav"))
save_button.pack(pady=10)

# Uruchomienie pętli głównej interfejsu graficznego
root.mainloop()