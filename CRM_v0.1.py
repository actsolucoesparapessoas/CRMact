import streamlit as st
from datetime import datetime
from datetime import date
import pytz
import time

from io import BytesIO
import requests
import json

import numpy as np
import pandas as pd
import sqlite3
from streamlit_timeline import timeline
import plotly.express as px #Para o Funnel Chart

from GoogleNews import GoogleNews
from random import randrange

from deep_translator import GoogleTranslator
tradutor = GoogleTranslator(source= "en", target= "pt")

Status = True

# Page setting
st.set_page_config(layout="wide", page_title="CRM ACT")

placeholder = st.empty() #Este comando é necessário para limpar a tela

datetime_br= datetime.now(pytz.timezone('America/Sao_Paulo'))
#t = datetime_br.strftime('%d:%m:%Y %H:%M:%S %Z %z')
data_atual = datetime_br.strftime('%d/%m/%Y')

def atualiza_cotacoes():
    #Link para Scraping de Cotação de moedas
    requisicao1 = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
    cotacaoUS = requisicao1.json() 
    requisicao2 = requests.get('https://economia.awesomeapi.com.br/all/EUR-BRL')
    cotacaoEUR = requisicao2.json()
    a1, a2, a3, a4 = st.columns(4)
    a1.image('act_LOGO150.jpg', width=150, output_format='auto') 
    D2 = "U$ (" + str(cotacaoUS['USD']['create_date']) + ")"
    a2.metric (f"{D2}", f" {cotacaoUS['USD']['bid']} ", f" {cotacaoUS['USD']['pctChange']} "+"%")
    D3 = "EU$ (" + str(cotacaoEUR['EUR']['create_date']) + ")"
    a3.metric (f"{D3}", f" {cotacaoEUR['EUR']['bid']} ", f" {cotacaoEUR['EUR']['pctChange']} "+"%")
    DATA = '<p style="font-family:tahoma; color:gray; text-align: center; font-size: 48px;"> (%s) </p>' % data_atual
    a4.markdown(DATA, unsafe_allow_html=True)

def atualiza_news():
    googlenews = GoogleNews()
    googlenews.set_lang('pt')
    #googlenews.set_lang('en')
    googlenews.set_period('3d')
    #googlenews.set_time_range('02/01/2020','02/28/2020')
    googlenews.set_encode('utf-8')
    googlenews.get_news('A')

    resp = googlenews.results(sort=True)

    df = pd.DataFrame(resp)
    MeiosMaisCitados = df['media'].value_counts()
    filtro = lambda x: x["media"] == MeiosMaisCitados.index[0]
    filtrados = list(filter(filtro , resp))
    dfFILTER = pd.DataFrame(filtrados)
    CincoMais = dfFILTER.head(5)
    indice = randrange(5)
    Noticia_Selecionada = CincoMais['title'][indice]
    Noticia_Selecionada = Noticia_Selecionada.replace(str(MeiosMaisCitados.index[0]),"",1)
    Noticia_Selecionada = Noticia_Selecionada.replace("Mais","",1)
    Noticia_Selecionada = tradutor.translate(Noticia_Selecionada)
    Link_Selecionado = CincoMais['link'][indice]
    #url = "https://www.streamlit.io"
    #st.write("check out this [link](%s)" % url)

    TEXTO1 = '<p style="font-family:tahoma; color:white; text-align: center; font-size: 26px;"> (%s) </p>' % Noticia_Selecionada
    st.markdown(TEXTO1, unsafe_allow_html=True)
    TEXTO2 = '<p style="font-family:tahoma; color:blue; text-align: center; font-size: 5px;"> (%s) </p>' % Link_Selecionado
    st.markdown(TEXTO2, unsafe_allow_html=True)      
  
def exibir():
    conn = sqlite3.connect('CRMact.db')
    cursor = conn.execute(""" SELECT * FROM CRM_ACT """)
    rows = cursor.fetchall()
    for row in cursor:
        st.write("ID: ", row[0])
        st.write("Acontecimento: ", row[1])
        st.write("Data: ", row[2])
        st.write("Nº Processo: ", row[3])
        st.write("Responsável: ", row[4])
        st.write("Data Lembrete: ", row[5])
        st.write("Observação: ", row[6])   
        st.write("Situação: ", row[7])   
    if len(rows) != 0:
        db = pd.DataFrame(rows)    
        db.columns = ['ID' , 'ACONTECIMENTO' , 'DATA', 'Nprocesso', 'RESPONSAVEL' , 'Data_LEMBRETE', 'OBSERVACAO', 'SITUACAO']
        st.write(db)
    conn.close()
    
VetorDB0 = []
VetorDB1 = []
VetorDB2 = []
VetorDB3 = []
VetorDB4 = []

#1º)Para criar um banco de dados SQL , usamos o seguinte comando:
conn = sqlite3.connect('CRMact.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS CRM_ACT(ID         TEXT    NOT NULL,
                                                    CONTENT     TEXT    NOT NULL,
                                                    DATA        TEXT    NOT NULL,
                                                    Nprocesso   TEXT    NOT NULL,
                                                    RESP        TEXT    NOT NULL,
                                                    DLEMBRETE   TEXT    NOT NULL,
                                                    OBS         TEXT    NOT NULL,
                                                    SITUACAO    TEXT    NOT NULL);''')
conn.close()

def Exibir_Abas():
    #2º)INSERT data and READ this data
    #   Following Python program shows how to create records in the COMPANY table created in the above example.
    conn = sqlite3.connect('CRMact.db')
    cursor = conn.execute(""" SELECT * FROM CRM_ACT """)
    rows = cursor.fetchall()
    n = len(rows)
    tab1, tab2, tab3 = st.tabs(["Cadastrar", "DADOS", "Gráficos"])
    with tab1:
        b1, b2, b3 = st.columns(3)
        txtID = b1.text_input("ID: ", str(n+1))
        txtCONTENT = b1.text_input("Acontecimento:")
        txtDATA = b1.text_input("Data:", "2024-12-01")
        txtNprocesso = b1.text_input("Nº do Processo: ")
        txtRESP = b1.text_input("Responsável:")
        txtDataLembrete = b1.text_input("Data para Lembrete:", "2024-12-01")
        txtOBS = b1.text_input("Observação:")
        txtSITUACAO = b1.text_input("SITUAÇÃO:")
        if b2.button('✔️ Salvar Dados'):
            conn.execute("""INSERT INTO CRM_ACT (ID, CONTENT, DATA, Nprocesso, RESP, DLEMBRETE, OBS, SITUACAO)
                            VALUES (?,?,?,?,?,?,?,?)
                            """, (txtID, txtCONTENT, txtDATA, txtNprocesso, txtRESP, txtDataLembrete, txtOBS, txtSITUACAO))
            conn.commit()
            st.write("Records created successfully")
            conn.close()
        with b3:
            st.write("Base de dados atual:")
            exibir() 
    with tab2: 
        exibir()

    with tab3:   
        Nproc = str(st.text_input("Nº Processo a pesquisar?", 1))
        conn = sqlite3.connect('CRMact.db')
        cursor = conn.execute(" SELECT * FROM CRM_ACT WHERE Nprocesso=?;", [Nproc])
        rows = cursor.fetchall()

        if len(rows) != 0:
            db = pd.DataFrame(rows)  
            nreg = len(db)        
            db.columns = ['ID' , 'ACONTECIMENTO' , 'DATA', 'Nprocesso', 'RESPONSAVEL' , 'Data_LEMBRETE', 'OBSERVACAO', 'SITUACAO']
            #st.write(db)                                      
            db = dict(db)
            #st.write("QTD de registros = ", nreg)
            for l in range(nreg):
                for c in range(3):
                    if c==0:
                        if l==0:
                            VetorDB0.append(db['ID'][0])
                        if l==1:
                            VetorDB1.append(db['ID'][1])
                        if l==2:
                            VetorDB2.append(db['ID'][2])
                        if l==3:
                            VetorDB3.append(db['ID'][3])
                        if l==4:
                            VetorDB4.append(db['ID'][4]) 
                    elif c==1:
                        if l==0:
                            VetorDB0.append(db['ACONTECIMENTO'][0] + "/" + db['RESPONSAVEL'][0])
                        if l==1:
                            VetorDB1.append(db['ACONTECIMENTO'][1] + "/" + db['RESPONSAVEL'][1])
                        if l==2:
                            VetorDB2.append(db['ACONTECIMENTO'][2] + "/" + db['RESPONSAVEL'][2])
                        if l==3:
                            VetorDB3.append(db['ACONTECIMENTO'][3] + "/" + db['RESPONSAVEL'][3])
                        if l==4:
                            VetorDB4.append(db['ACONTECIMENTO'][4] + "/" + db['RESPONSAVEL'][4]) 
                    else:
                        if l==0:
                            VetorDB0.append(db['DATA'][0])
                        if l==1:
                            VetorDB1.append(db['DATA'][1])
                        if l==2:
                            VetorDB2.append(db['DATA'][2])
                        if l==3:
                            VetorDB3.append(db['DATA'][3])
                        if l==4:
                            VetorDB4.append(db['DATA'][4])
            if nreg==1:
                items = [{"id": 1, "content": str(VetorDB0[1]), "start": str(VetorDB0[2])}]       
            elif nreg==2:
                items = [{"id": 1, "content": str(VetorDB0[1]), "start": str(VetorDB0[2])},
                        {"id": 2, "content": str(VetorDB1[1]), "start": str(VetorDB1[2])}]      
            elif nreg==3:
                items = [{"id": 1, "content": str(VetorDB0[1]), "start": str(VetorDB0[2])},
                        {"id": 2, "content": str(VetorDB1[1]), "start": str(VetorDB1[2])},
                        {"id": 3, "content": str(VetorDB2[1]), "start": str(VetorDB2[2])}]  
            elif nreg==4:
                items = [{"id": 1, "content": str(VetorDB0[1]), "start": str(VetorDB0[2])},
                        {"id": 2, "content": str(VetorDB1[1]), "start": str(VetorDB1[2])},
                        {"id": 3, "content": str(VetorDB2[1]), "start": str(VetorDB2[2])},
                        {"id": 4, "content": str(VetorDB3[1]), "start": str(VetorDB3[2])}]        
            elif nreg==5:
                items = [{"id": 1, "content": str(VetorDB0[1]), "start": str(VetorDB0[2])},
                        {"id": 2, "content": str(VetorDB1[1]), "start": str(VetorDB1[2])},
                        {"id": 3, "content": str(VetorDB2[1]), "start": str(VetorDB2[2])},
                        {"id": 4, "content": str(VetorDB3[1]), "start": str(VetorDB3[2])},
                        {"id": 5, "content": str(VetorDB4[1]), "start": str(VetorDB4[2])}]
            else:
                items = [{"id": 1, "content": "Acontecimento 01", "start": "2022-10-08"},
                        {"id": 2, "content": "Acontecimento 02", "start": "2022-10-12"},
                        {"id": 3, "content": "Acontecimento 03", "start": "2022-10-15"},
                        {"id": 4, "content": "Acontecimento 04", "start": "2022-10-18"},
                        {"id": 5, "content": "Acontecimento 05", "start": "2022-10-21"}]          
            
            st.subheader("Linha do tempo:")
            st.write(timeline(items, height=800) )
            #tline = timeline(items, height=800)          
            #st.write(tline)            
            st.divider()
            
            #GRAFICO FUNIL 
            st.subheader("Funil de Vendas:")            
            rD2 = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vQ_Aogr8qHdY-p27WXM7P-LoxVDSnXZsY5cVDxOBz28FdpFnkZQHMdPZonBVBvJhYxWlT_KhKJNFo--/pub?gid=1323132851&single=true&output=csv')
            dataD2 = rD2.content
            dfD2 = pd.read_csv(BytesIO(dataD2), index_col=0)
            NregD2 = len(dfD2)
            data = dict(
                number=[NregD2, 23, 20, 11, 2],
                stage=["Website visit", "Downloads", "Potential customers", "Requested price", "invoice sent"])
            fig = px.funnel(data, x='number', y='stage')

            st.plotly_chart(fig, use_container_width=True)
            
            conn.close()


#=====================================================================================================================
# A rotina a seguir possibilita uma atualização de dados das cotações, notícias e gráficos limpando e re-exibindo!
Status = st.button("🔁")

with open('style.css') as f:
    Status = True
    if Status:
        placeholder.empty()
        placeholder.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        atualiza_cotacoes()
        with st.expander("Resumo de Notícias:"):
            atualiza_news()
        st.divider()
        Exibir_Abas()
    Status = False


