"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import streamlit as st
import google.generativeai as genai
from gtts import gTTS

genai.configure(api_key="AIzaSyChCrbdYRD0AVTVf3RzFkxw2XzKooATnMQ")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel('gemini-pro')
txtQUESTION = st.text_input("Digite uma pergunta: ","Escreva um parágrafo sobre Inteligência Artificial e coloque as referências bibliográficas no qual se baseiou.")
if st.button(label = '✔️ Enviar Pergunta'):
    response = model.generate_content(txtQUESTION)
    resp = response.text
    st.write(resp)
    myobj2 = gTTS(text=resp, lang='pt', slow=False)
    myobj2.save("resp.mp3")   #Saving the converted audio in a mp3 file
    # Playing the converted file
    audio_file2 = open('resp.mp3', 'rb')
    audio_bytes2 = audio_file2.read()
    st.audio(audio_bytes2, format='audio/ogg',start_time=0)
