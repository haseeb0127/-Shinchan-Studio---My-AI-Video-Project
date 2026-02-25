import streamlit as st
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from moviepy.audio.AudioClip import CompositeAudioClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import os
import random

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
    
    # Mapped to your 'fonts' folder on GitHub
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
                bg_music_file = f"music/{music_choice.lower().replace(' ', '_')}.mp3"
                if os.path.exists(bg_music_file):
                    bg_music = AudioFileClip(bg_music_file).with_duration(voice.duration).with_volume_scaled(0.15)
                    voice = CompositeAudioClip([voice, bg_music])

            st.write("🖼️ Selecting Random Background...")
            # --- FIXED: Direct folder name from your GitHub ---
            bg_folder = "backgrounds" 
            all_bgs = [f for f in os.listdir(bg_folder) if f.lower().endswith(('.png', '.jpg'))]
            bg_path = os.path.join(bg_folder, random.choice(all_bgs))
            bg = ImageClip(bg_path).with_duration(voice.duration).resized(width=1280)

            st.write("🚶 Animating Character...")
            prefix = "character" if char_choice == "Shinchan" else "character2"
            
            # Smart logic to handle the ' (2)' in filenames automatically
            potential_closed = [f"{prefix}_closed.png", f"{prefix}_closed (2).png"]
            potential_open = [f"{prefix}_open.png", f"{prefix}_open (2).png"]
            
            closed_path = next((f for f in potential_closed if os.path.exists(f)), potential_closed[0])
            open_path = next((f for f in potential_open if os.path.exists(f)), potential_open[0])

            c = ImageClip(closed_path).with_duration(0.15).resized(width=400)
            o = ImageClip(open_path).with_duration(0.15).resized(width=400)
                
            actor = concatenate_videoclips([c, o] * int(voice.duration/0.3 + 1)).with_duration(voice.duration).with_position((440, 320))

            st.write("📝 Adding Subtitles...")
            subs = create_subtitle_image(script_text, voice.duration, lang_choice)

            st.write("🎥 Final Render...")
            final = CompositeVideoClip([bg, actor, subs], size=(1280, 720)).with_audio(voice)
            final.write_videofile("studio_result.mp4", fps=24, preset="ultrafast", logger=None)
            
            status.update(label="✅ Video Ready!", state="complete", expanded=False)

        # 4. Display Video on Website
        st.video("studio_result.mp4")
        with open("studio_result.mp4", "rb") as file:
            st.download_button("📥 Download Video", data=file, file_name="ai_cartoon.mp4", mime="video/mp4")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
