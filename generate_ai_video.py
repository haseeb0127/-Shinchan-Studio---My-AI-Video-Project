import streamlit as st
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, ColorClip
from moviepy.audio.AudioClip import CompositeAudioClip
from gtts import gTTS
import os, random, glob, time

st.set_page_config(page_title="Asif's AI Studio", layout="wide")
st.title("🎬 Asif's Advanced Scene Engine")
st.markdown("Generates dynamic, multi-scene videos by breaking your script into chunks.")

with st.sidebar:
    st.header("Global Settings")
    lang = st.selectbox("Language", ["English", "Hindi", "Telugu", "Hinglish"])
    mus = st.selectbox("Background Music", ["No Music", "Bollywood Drama", "Hollywood Epic"])

default_script = "Hello dosto, welcome to the psychology class. Aaj hum memory ke baare mein kheenge. The brain is like a computer. Let us look at how data is stored."
script = st.text_area("Script (Use periods '.' to create new scenes!):", default_script, height=150)

def find(pattern):
    f = glob.glob(f"**/{pattern}", recursive=True)
    return f[0] if f else None

if st.button("🚀 Generate Multi-Scene Video"):
    try:
        with st.status("🎬 Processing Scenes...", expanded=True) as status:
            l_map = {"English":"en","Hindi":"hi","Telugu":"te","Hinglish":"hi"}
            
            sentences = [s.strip() for s in script.split('.') if len(s.strip()) > 3]
            st.write(f"🔪 Sliced script into {len(sentences)} different scenes.")
            
            scene_clips = []
            
            for index, text in enumerate(sentences):
                st.write(f"⚙️ Rendering Scene {index + 1}...")
                
                # --- FIXED: Automatic Retry & Backoff Logic ---
                success = False
                for attempt in range(3): # It will try up to 3 times per sentence
                    try:
                        tts = gTTS(text=text, lang=l_map[lang])
                        temp_audio = f"temp_{index}.mp3"
                        tts.save(temp_audio)
                        success = True
                        break # If it works, break out of the retry loop!
                    except Exception as e:
                        if "429" in str(e):
                            wait_time = 5 * (attempt + 1)
                            st.warning(f"⏳ Google API busy. Retrying scene {index + 1} in {wait_time} seconds...")
                            time.sleep(wait_time)
                        else:
                            raise e
                            
                if not success:
                    st.error("Google TTS is completely blocking us right now due to server traffic. Please try again in 10 minutes.")
                    st.stop()
                
                v = AudioFileClip(temp_audio)
                
                bgs = glob.glob("**/backgrounds/*.*", recursive=True)
                if bgs:
                    bg = ImageClip(random.choice(bgs)).with_duration(v.duration).resized(width=1280)
                else:
                    bg = ColorClip(size=(1280, 720), color=(random.randint(50,250), random.randint(50,250), 200)).with_duration(v.duration)

                pre = "character" if index % 2 == 0 else "character2"
                cp, op = find(f"{pre}_closed*.png"), find(f"{pre}_open*.png")
                
                if cp and op:
                    c = ImageClip(cp).with_duration(0.15).resized(height=450)
                    o = ImageClip(op).with_duration(0.15).resized(height=450)
                    act = concatenate_videoclips([c, o] * int(v.duration/0.3 + 1)).with_duration(v.duration).with_position(("center", "bottom"))
                    scene = CompositeVideoClip([bg, act], size=(1280, 720)).with
