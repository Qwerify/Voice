import vosk
import pyaudio
import json
import os
import time
model_path = os.path.join(os.getcwd(), "model")
model = vosk.Model(model_path)
SPEECH_TIMEOUT = 12.0 
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,input=True, frames_per_buffer=8000)
stream.start_stream()
rec = vosk.KaldiRecognizer(model, 16000)
def listen():
    print("Speak ...")
    last_speech_time = time.time()
    question = ""
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "")
            if text:
                question += " " + text
                last_speech_time = time.time()
                # print(f"\r{question}")
        else:
            partial = json.loads(rec.PartialResult())
            partial_text = partial.get("partial", "")
            if partial_text:
                print(f"\r{question.strip()} {partial_text}", end="")
        if time.time() - last_speech_time > SPEECH_TIMEOUT and question.strip():
            print(f"\r{question.strip()}")
            # print("the strip")
            # deepseek_reply(utterance.strip())
            # question = ""
            # last_speech_time = time.time()
            return question.strip()
try:
    user_input = listen()
    with open("output.txt","w") as f:
        f.write(user_input)
except KeyboardInterrupt:
    print("\nStopping...")
    stream.stop_stream()
    stream.close()
    p.terminate()

