import streamlit as st
from deepgram import Deepgram
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
        "buffer": uploaded_file,
        "mimetype": mimetype
    }
    response = get_result(source)

    st.subheader("Transcription Result:")
    st.write(response["results"]["channels"][0]["alternatives"][0]["transcript"])
    result_json = json.dumps(response, indent = 2)
    result_bytes = result_json.encode("utf-8")
    st.download_button(
        label = "Download Transcription Result",
        data = result_bytes,
        file_name = "transcription_result.json",
        key = "transcription_result_button",
    )