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
            
            # Split script by periods
            sentences = [s.strip() for s in script.split('.') if len(s.strip()) > 3]
            st.write(f"🔪 Sliced script into {len(sentences)} different scenes.")
            
            scene_clips = []
            
            for index, text in enumerate(sentences):
                st.write(f"⚙️ Rendering Scene {index + 1}...")
                
                # --- FIXED: Added a 2-second pause to prevent Google 429 Error ---
                tts = gTTS(text=text, lang=l_map[lang])
                temp_audio = f"temp_{index}.mp3"
                tts.save(temp_audio)
                time.sleep(2) # <--- The computer takes a deep breath here
                
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
                    scene = CompositeVideoClip([bg, act], size=(1280, 720)).with_audio(v)
                else:
                    scene = CompositeVideoClip([bg], size=(1280, 720)).with_audio(v)

                scene_clips.append(scene)

            st.write("🧵 Stitching all scenes into one final video...")
            final_video = concatenate_videoclips(scene_clips)
            
            if mus != "No Music":
                mf = find(f"{mus.lower().replace(' ','_')}.mp3")
                if mf:
                    bm = AudioFileClip(mf).with_duration(final_video.duration).with_volume_scaled(0.10)
                    final_video.audio = CompositeAudioClip([final_video.audio, bm])

            st.write("🎥 Final Encoding (This takes time for long videos)...")
            final_video.write_videofile("out.mp4", fps=24, preset="ultrafast", logger=None)
            
            status.update(label="✅ Full Video Ready!", state="complete")

        st.video("out.mp4")
        with open("out.mp4", "rb") as f:
            st.download_button("📥 Download Full Video", data=f, file_name="multi_scene_video.mp4")
            
    except Exception as e:
        st.error(f"Error: {e}")
