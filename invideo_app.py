import streamlit as st
import os
import random
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont

# --- PAGE SETUP ---
st.set_page_config(page_title="Haseeb's AI Studio", layout="wide")
st.title("🎬 My AI Video Engine")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("Video Settings")
    char_name = st.selectbox("Select Character", ["shinchan", "doraemon"])
    lang = st.selectbox("Language", ["en", "hi", "te"])
    bg_music = st.checkbox("Add Background Music?")

# --- MAIN INPUT ---
user_prompt = st.text_area("Enter your video script here:", "Hello! Today we are learning something new.")

if st.button("🚀 Create Video"):
    with st.spinner("Generating your AI masterpiece..."):
        try:
            # 1. Voice Over
            tts = gTTS(text=user_prompt, lang=lang)
            tts.save("temp_voice.mp3")
            voice = AudioFileClip("temp_voice.mp3")

            # 2. Random Background Selection
            bg_files = [f for f in os.listdir("images/backgrounds") if f.endswith(('.png', '.jpg'))]
            bg_path = os.path.join("images/backgrounds", random.choice(bg_files))
            bg = ImageClip(bg_path).set_duration(voice.duration).resize(width=1280)

            # 3. Character Animation (Laptop Logic)
            c = ImageClip(f"images/{char_name}_closed.png").set_duration(0.15).resize(width=400)
            o = ImageClip(f"images/{char_name}_open.png").set_duration(0.15).resize(width=400)
            actor = concatenate_videoclips([c, o] * int(voice.duration/0.3 + 1)).set_duration(voice.duration).set_position((450, 320))

            # 4. Final Master Render
            final = CompositeVideoClip([bg, actor], size=(1280, 720)).set_audio(voice)
            output_file = "output/studio_result.mp4"
            final.write_videofile(output_file, fps=24, codec="libx264", preset="ultrafast")

            # 5. Show Video in App
            st.success("✅ Video Generated Successfully!")
            st.video(output_file)
            
        except Exception as e:
            st.error(f"Error: {e}")
            