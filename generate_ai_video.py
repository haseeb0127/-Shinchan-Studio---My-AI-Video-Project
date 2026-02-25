import streamlit as st
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from moviepy.audio.AudioClip import CompositeAudioClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import os
import random
import glob

# Page Config
st.set_page_config(page_title="Asif's Bollywood AI Studio", page_icon="🎬")

st.title("🎬 Asif's Shinchan AI Studio")
st.markdown("### Create Kids Videos for YouTube & Instagram")

# 1. Sidebar for Settings
with st.sidebar:
    st.header("Studio Settings")
    char_choice = st.selectbox("Select Character", ["Shinchan", "Doraemon"])
    lang_choice = st.selectbox("Select Language", ["English", "Hindi", "Telugu", "Hinglish"])
    music_choice = st.selectbox("Music Style", ["No Music", "Bollywood Drama", "Hollywood Epic"])

# 2. Script Input
script_text = st.text_area("Enter your script here:", "Hello dosto! Aaj hum psychology ke baare mein baat karenge.")

# Subtitle Helper
def create_subtitle_image(text, duration, lang):
    img = Image.new('RGBA', (1280, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([100, 50, 1180, 150], fill=(0, 0, 0, 160))
    
    if lang == "Hindi": font_file = "fonts/Hind-Regular.ttf"
    elif lang == "Telugu": font_file = "fonts/Ramabhadra-Regular.ttf"
    else: font_file = "fonts/Hind-Regular.ttf"

    try:
        font = ImageFont.truetype(font_file, 45)
    except:
        font = ImageFont.load_default()

    draw.text((640, 100), text, fill="white", anchor="mm", font=font)
    img.save("temp_sub.png")
    return ImageClip("temp_sub.png").with_duration(duration).with_position(("center", "bottom"))

# NEW: Super Searcher Function
def find_any_file(pattern):
    # This looks in ALL folders for any file matching the pattern
    files = glob.glob(f"**/{pattern}", recursive=True)
    if files:
        return files[0]
    return None

# 3. Generate Button
if st.button("🚀 Generate AI Video"):
    try:
        with st.status("🎬 Processing Video...", expanded=True) as status:
            lang_map = {"English": "en", "Hindi": "hi", "Telugu": "te", "Hinglish": "hi"}
            
            st.write("🎙️ Generating AI Voice...")
            tts = gTTS(text=script_text, lang=lang_map[lang_choice])
            tts.save("temp.mp3")
            voice = AudioFileClip("temp.mp3")

            st.write("🎵 Mixing Background Music...")
            if music_choice != "No Music":
                bg_music_file = find_any_file(f"{music_choice.lower().replace(' ', '_')}.mp3")
                if bg_music_file:
                    bg_music = AudioFileClip(bg_music_file).with_duration(voice.duration).with_volume_scaled(0.15)
                    voice = CompositeAudioClip([voice, bg_music])

            st.write("🖼️ Selecting Random Background...")
            # Look for backgrounds in any folder
            bg_files = glob.glob("**/backgrounds/*.
