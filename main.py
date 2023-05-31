from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

def get_chatgpt_response(messages):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    return response['choices'][0]['message']['content']

@app.route('/chatgpt/chat', methods=['POST'])
def getChatResponse():
    messages = request.json['messages']
    print(messages)
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model_response = get_chatgpt_response(messages)
    return {"response": model_response}

@app.route('/', methods=['GET'])
def getResponse():
    return {"salud"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True) #Con el True en debug se reinicia cuando hay cambios
