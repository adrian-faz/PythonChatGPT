#Se importa la librería Whisper
import whisper
import openai
import os
from dotenv import load_dotenv
import pprint
import pyaudio
import wave
from pydub import AudioSegment

def grabar_audio(num):
    # set parameters for recording
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output.wav"
    MP3_OUTPUT_FILENAME = f"output{num}.mp3"

    # initialize PyAudio
    audio = pyaudio.PyAudio()

    # start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save the recorded audio to a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # convert the WAV file to MP3
    sound = AudioSegment.from_wav(WAVE_OUTPUT_FILENAME)
    sound.export(MP3_OUTPUT_FILENAME, format="mp3")




def update_chat(message, role, content):
    message.append({"role": role, "content": content})
    return message

def get_chatgpt_response(messages):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    return response['choices'][0]['message']['content']

# Se carga el modelo a utilizar
model = whisper.load_model("base")

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
'''
messages=[{"role": "system", "content": "You are an english evaluator. You will create an question to evaluate the english skill of the user. After receiving the answer of the user, you will evaluate his grammar, coherence and vocabulary, along with providing feedback and how to improve. The answer was spoken and transcribed with Whisper. The user did not write it, he spoke it."},
          {"role": "assistant", "content": "I understand. I will evaluate the answer of the user."},
          {"role": "assistant", "content": "Hey, are you ready to begin the test? Once you say yes, I will provide the question that you will need to answer."},
          {"role": "user", "content": "yes"},
          {"role": "assistant", "content": "What are you currently studying and why?"}]

'''

messages= [{"role": "system", "content": "You are an english evaluator. We will have a conversation about a topic. Start asking an initial question to talk with me. Keep the conversation going for 3 more questions in total, but ask only one question after i answer, and so on. After that, evaluate my grammar, coherence and vocabulary, each in a scale from 1 to 100. After finishing the conversations, only respond with the 3 scores on the areas previously mentioned, i don't want feedback, only the scores stored in a json. "},
          {"role": "assistant", "content": "I understand, after 5 questions I will only show the results in coherence, vocabulary and grammar in a JSON and that is the only thing I will return to the user."},
          {"role": "assistant", "content": "Hey! What are you currently studying and why'"}]

go = True
control = 0
preguntas = 0
first = True

pprint.pprint(messages[-1]["content"])

while go:
    preguntas += 1
    if not first:
        pprint.pprint(messages[-1]["content"])

    user_input = input()
    # grabar_audio(0)
    # user_input = model.transcribe("output0.mp3")["text"]
    messages = update_chat(messages, "user", user_input)
    model_response = get_chatgpt_response(messages)
    messages = update_chat(messages, "assistant", model_response)
    first = False
    if preguntas == 5:
        break

print("Holaaa")
messages = update_chat(messages, "assistant",
                               "The conversation has finished. Based on the answers I gave you, generate a JSON with 6 fields: Grammar, Coherence, Vocabulary, Feedback, Recommendations and English_Level. The first three fields must be evaluated in a scale from 1 to 100, the feedback must be a paragraph of my overall performance and the English_Level field must be either A1, A2, B1, B2, C1 or C2. The Recommendations field must be an array of 3 specific recommendations that the user could have done to improve his phrasing referring to what he said, in this recommendations mention specific words or sentences that could have been changed..")
model_response = get_chatgpt_response(messages)

print(model_response)
