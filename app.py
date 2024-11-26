from flask import Flask, render_template, request, jsonify
from groq import Groq


client = Groq(api_key="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",)

def initialize_messages():
    return [{"role": "system",
             "content": "You are a financial expert that specializes in real estate investment and negotiation"}]

messages_prmt = initialize_messages()

app = Flask(__name__)


def customLLMBot(user_input, history):
    global messages_prmt

    messages_prmt.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        messages=messages_prmt,
        model="llama3-8b-8192",
    )
    print(response)

    # Extract the assistant's reply
    LLM_reply = response.choices[0].message.content
    messages_prmt.append({"role": "assistant", "content": LLM_reply})

    return LLM_reply


@app.route('/')
def home():
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    history = messages_prmt
    response = customLLMBot(user_input, history)
    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
