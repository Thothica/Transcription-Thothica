import streamlit as st
from deepgram import Deepgram
from deepgram_captions import DeepgramConverter, srt
import json

st.title("Thothica Rekhta Transcription")

@st.cache_data
def get_result(source):
    return deepgram.transcription.sync_prerecorded(source = source, options = {"language" : "hi"})

uploaded_file = st.file_uploader(label = "Upload audio file", label_visibility = "collapsed")
mimetype = (uploaded_file.type if uploaded_file else None)
deepgram = Deepgram(st.secrets["DEEPGRAM_API_KEY"])

if uploaded_file is not None:
    source = {
        "model" : "nova-2-ea",
        "buffer": uploaded_file,
        "mimetype": mimetype
    }
    response = get_result(source)

    st.subheader("Transcription Result:")
    st.write(response["results"]["channels"][0]["alternatives"][0]["transcript"])
    transcription = DeepgramConverter(response)
    captions = srt(transcription)
    st.download_button(
        label = "Download Transcription Result",
        data = captions,
        file_name = "transcription_result.txt",
        key = "transcription_result_button",
    )