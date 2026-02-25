import streamlit as st
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from moviepy.audio.AudioClip import CompositeAudioClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import os, random, glob

st.set_page_config(page_title="Asif's Bollywood AI Studio", page_icon="🎬")
st.title("🎬 Asif's Shinchan AI Studio")

with st.sidebar:
    st.header("Studio Settings")
    char_choice = st.selectbox("Select Character", ["Shinchan", "Doraemon"])
    lang_choice = st.selectbox("Select Language", ["English", "Hindi", "Telugu", "Hinglish"])
    music_choice = st.selectbox("Music Style", ["No Music", "Bollywood Drama", "Hollywood Epic"])

script_text = st.text_area("Enter your script here:", "Hello dosto!")

def find_any_file(pattern):
    files = glob.glob(f"**/{pattern}", recursive=True)
    return files[0] if files else None

if st.button("🚀 Generate AI Video"):
    try:
        with st.status("🎬 Processing...", expanded=True) as status:
            lang_map = {"English": "en", "Hindi": "hi", "Telugu": "te", "Hinglish": "hi"}
            
            st.write("🎙️ Voice...")
            tts = gTTS(text=script_text, lang=lang_map[lang_choice])
            tts.save("temp.mp3")
            voice = AudioFileClip("temp.mp3")

            st.write("🎵 Music...")
            if music_choice != "No Music":
                m_file = find_any_file(f"{music_choice.lower().replace(' ', '_')}.mp3")
                if m_file:
                    bg_m = AudioFileClip(m_file).with_duration(voice.duration).with_volume_scaled(0.15)
                    voice = CompositeAudioClip([voice, bg_m])

            st.write("🖼️ Background...")
            bg_files = glob.glob("**/backgrounds/*.*", recursive=True) + glob.glob("*.png") + glob.glob("*.jpg")
            bg_path = random.choice(bg_files)
            bg = ImageClip(bg_path).with_duration(voice.duration).resized(width=1280)

            st.write("🚶 Character...")
            search_prefix = "character" if char_choice == "Shinchan" else "character2"
            c_path = find_any_file(f"{search_prefix}_closed*.png")
            o_path = find_any_file(f"{search_prefix}_open*.png")

            if not c_path or not o_path:
                st.error(f"Missing images for {char_choice} on GitHub!")
                st.stop()

            c = ImageClip(c_path).with_duration(0.15).resized(width=400)
            o = ImageClip(o_path).with_duration(0.15).resized(width=400)
            actor =
