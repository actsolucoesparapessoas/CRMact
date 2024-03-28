import streamlit as st
from streamlit_chat import message
from PIL import Image # Lib para carregar imagem no Streamlit
from gtts import gTTS #Lib para Conversão Text2Voice. Em seguida pode usar Gemini para converter voice para texto
import google.generativeai as genai

import os

def api_calling(QUESTION):
    genai.configure(api_key="AIzaSyChCrbdYRD0AVTVf3RzFkxw2XzKooATnMQ")

    # Set up the model
    generation_config = {
      "temperature": 0.9,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 2048,
    }

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(QUESTION)
    resp = response.text
    return resp

def get_text():
	input_text = st.text_input("Digite sua pergunta aqui 👇", key="input")
	return input_text
    
col1, col2 = st.columns((1,1))
with col1:
    st.title("A Fran Responde!") 
    st.write("Suportado pela API Google Gemini")
    # Playing the Audio of Fran's Presentation
    audio_file = open('Fran0.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg',start_time=0)
    user_input = get_text()
with col2:
    image = Image.open('Fran.PNG')
    st.image(image, caption='Foto da Fran')

if 'user_input' not in st.session_state:
	st.session_state['user_input'] = []

if 'ai_response' not in st.session_state:
	st.session_state['ai_response'] = []




if user_input:
	output = api_calling(user_input)
	output = output.lstrip("\n")

	# Store the output
	st.session_state.ai_response.append(user_input)
	st.session_state.user_input.append(output)

message_history = st.empty()

if st.session_state['user_input']:
    my_expander = st.expander(label='Clique e abra o hitórico de Perguntas & Respostas! 	👉')
    with my_expander:
        for i in range(len(st.session_state['user_input']) - 1, -1, -1):
            # This function displays Gemini response
            message(st.session_state['ai_response'][i], 
                    avatar_style="user",is_user=True,                                    
                    key=str(i) + 'data_by_user')  
            perg = st.session_state['ai_response'][i] 
            
            #Pergunta para Gemini
            language = 'pt'     # Language in which you want to convert
            # Passing the text and language to the engine,here we have marked slow=False. Which tells the module that the converted audio should have a high speed
            myobj1 = gTTS(text=perg, lang=language, slow=False)
            myobj1.save("perg.mp3")   #Saving the converted audio in a mp3 file
            # Playing the converted file
            audio_file = open('perg.mp3', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/ogg',start_time=0)
    
            # This function displays user input
            message(st.session_state["user_input"][i],
                    key=str(i),avatar_style="icons")            
            resp = st.session_state["user_input"][i]
            
            #RESPOSTA Gemini
            # Passing the text and language to the engine,here we have marked slow=False. Which tells the module that the converted audio should have a high speed
            myobj2 = gTTS(text=resp, lang=language, slow=False)
            myobj2.save("resp.mp3")   #Saving the converted audio in a mp3 file
            # Playing the converted file
            audio_file2 = open('resp.mp3', 'rb')
            audio_bytes2 = audio_file2.read()
            st.audio(audio_bytes2, format='audio/ogg',start_time=0)

st.markdown("""#### Programador responsável: Massaki de Oliveira Igarashi """)

#st.image(LogoCCT, width=600, caption='Mackenzie Campinas - 20 anos')
st.markdown("""#### _________________________________________________________________________""")
st.markdown("""##### Integrante  do Grupo de Pesquisa em Direito, Inovação e Tecnologia - GPDIT """)
