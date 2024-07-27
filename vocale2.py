mport streamlit as st
import streamlit as st
from deepgram import Deepgram
import aiohttp
import asyncio
import os

# Configuration de l'API Deepgram
DEEPGRAM_API_KEY = 'bd1d1c3c1caba214f6078a1129c1323d50eae666'
deepgram = Deepgram(DEEPGRAM_API_KEY)

# Fonction pour utiliser l'API Deepgram pour la reconnaissance vocale
async def transcribe_audio(file_path):
    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as audio_file:
            source = {
                'buffer': audio_file,
                'mimetype': 'audio/wav'  # Assurez-vous que le type MIME est correct pour votre fichier
            }
            response = await deepgram.transcription.prerecorded(source, {'punctuate': True})
            return response['results']['channels'][0]['alternatives'][0]['transcript']

# Interface utilisateur Streamlit
st.title("Reconnaissance Vocale avec Deepgram")

uploaded_file = st.file_uploader("Téléchargez un fichier audio", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.audio(file_path, format='audio/wav')

    if st.button("Transcrire"):
        with st.spinner("Transcription en cours..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            transcription = loop.run_until_complete(transcribe_audio(file_path))
            st.write("Transcription:")
            st.write(transcription)

        os.remove(file_path)
