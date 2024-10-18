import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def upload_to_gemini(path, mime_type=None):
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file
    except Exception as e:
        print("Erro ao fazer upload do arquivo:", e)
        return None

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

print("Olá! Eu sou um chatbot. Como posso ajudá-lo hoje? (Digite 'sair' para encerrar)")

chat_history = []

while True:
    user_input = input("Você: ")
    if user_input.lower() == "sair":
        print("AIA: Até logo!")
        break

    chat_history.append({"role": "user", "parts": [user_input + "\n"]})

    chat_session = model.start_chat(history=chat_history)

    try:
        response = chat_session.send_message(user_input)
        print("AIA:", response.text)
        chat_history.append({"role": "model", "parts": [response.text]})
    except Exception as e:
        print("Erro ao enviar mensagem:", e)
