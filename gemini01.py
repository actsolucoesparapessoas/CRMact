"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import streamlit as st
import google.generativeai as genai

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
    st.write(response.text)