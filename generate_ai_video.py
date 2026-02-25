import streamlit as st
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from moviepy.audio.AudioClip import CompositeAudioClip
from gtts import gTTS
import os, random, glob

st.set_page_config(page_title="Asif's Bollywood AI Studio", page_icon="🎬")
st.title("🎬 Asif's Shinchan AI Studio")

with st.sidebar:
    st.header("Settings")
    char_choice = st.selectbox("Character", ["Shinchan", "Doraemon"])
    lang_choice = st.selectbox("Language", ["English", "Hindi", "Telugu", "Hinglish"])
    music_choice = st.selectbox("Music", ["No Music", "Bollywood Drama", "Hollywood Epic"])

script_text = st.text_area("Script:", "Hello dosto!")

def find_file(pattern):
    files = glob.glob(f"**/{pattern}", recursive=True)
    return files[0] if files else None

if st.button("🚀 Generate AI Video"):
    try:
        with st.status("🎬 Processing...", expanded=True) as status:
            lang_map = {"English": "en", "Hindi": "hi", "Telugu": "te", "Hinglish": "hi"}
            
            # 1. Voice & Music
            tts = gTTS(text=script_text, lang=lang_map[lang_choice])
            tts.save("temp.mp3")
            voice = AudioFileClip("temp.mp3")
            if music_choice != "No Music":
                m_file = find_file(f"{music_choice.lower().replace(' ', '_')}.mp3")
                if m_file:
                    bg_m = AudioFileClip(m_file).with_duration(voice.duration).with_volume_scaled(0.15)
                    voice = CompositeAudioClip([voice, bg_m])

            # 2. Background
            bg_files = glob.glob("**/backgrounds/*.*", recursive=True) + glob.glob("*.png") + glob.glob("*.jpg")
            bg_path = random.choice(bg_files)
            bg = ImageClip(bg_path).with_duration(voice.duration).resized(width=1280)

            # 3. Character Animation
            pre = "character" if char_choice == "Shinchan" else "character2"
            c_path, o_path = find_file(f"{pre}_closed*.png"), find_file(f"{pre}_open*.png")
            if not c_path or not o_path:
                st.error("Missing images on GitHub!")
                st.stop()

            c, o = ImageClip(c_path).with_duration(0.15).resized(width=400), ImageClip(o_path).with_duration(0.15).resized(width=400)
            actor = concatenate_videoclips([c, o] * int(voice.duration/0.3 + 1)).with_duration(voice.duration).with_position((440, 320))

            # 4. Render
            final = CompositeVideoClip([bg, actor], size=(1280, 72
