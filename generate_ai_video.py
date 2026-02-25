import streamlit as st
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, ColorClip
from moviepy.audio.AudioClip import CompositeAudioClip
from gtts import gTTS
import os, random, glob, time

st.set_page_config(page_title="AI Studio", layout="wide")
st.title("🎬 Asif's Advanced Scene Engine")

with st.sidebar:
    st.header("Settings")
    lang = st.selectbox("Language", ["English", "Hindi", "Telugu", "Hinglish"])
    mus = st.selectbox("Music", ["No Music", "Bollywood Drama", "Hollywood Epic"])

def_script = "Hello dosto. Welcome to class. Aaj hum memory seekhenge. Brain is like a computer."
script = st.text_area("Script (Use periods '.' for new scenes):", def_script, height=100)

def find(pattern):
    f = glob.glob(f"**/{pattern}", recursive=True)
    return f[0] if f else None

if st.button("🚀 Generate"):
    try:
        with st.status("🎬 Processing...") as status:
            l_map = {"English":"en","Hindi":"hi","Telugu":"te","Hinglish":"hi"}
            sentences = [s.strip() for s in script.split('.') if len(s.strip()) > 3]
            clips = []
            
            for i, txt in enumerate(sentences):
                st.write(f"⚙️ Scene {i + 1}...")
                ok = False
                for att in range(3):
                    try:
                        tts = gTTS(text=txt, lang=l_map[lang])
                        tmp = f"t_{i}.mp3"
                        tts.save(tmp)
                        ok = True
                        break
                    except Exception as e:
                        if "429" in str(e):
                            time.sleep(5 * (att + 1))
                        else:
                            raise e
                            
                if not ok:
                    st.error("Google TTS Blocked. Try later.")
                    st.stop()
