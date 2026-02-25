import streamlit as st
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, ColorClip
from moviepy.audio.AudioClip import CompositeAudioClip
from gtts import gTTS
import os, random, glob

st.set_page_config(page_title="Asif's AI Studio")
st.title("🎬 Asif's Shinchan AI Studio")

with st.sidebar:
    st.header("Settings")
    char = st.selectbox("Character", ["Shinchan", "Doraemon"])
    lang = st.selectbox("Language", ["English", "Hindi", "Telugu", "Hinglish"])
    mus = st.selectbox("Music", ["No Music", "Bollywood Drama", "Hollywood Epic"])

script = st.text_area("Script:", "Hello dosto!")

def find(pattern):
    f = glob.glob(f"**/{pattern}", recursive=True)
    return f[0] if f else None

if st.button("🚀 Generate AI Video"):
    try:
        with st.status("🎬 Processing...") as status:
            l_map = {"English":"en","Hindi":"hi","Telugu":"te","Hinglish":"hi"}
            tts = gTTS(text=script, lang=l_map[lang])
            tts.save("t.mp3")
            v = AudioFileClip("t.mp3")
            
            if mus != "No Music":
                mf = find(f"{mus.lower().replace(' ','_')}.mp3")
                if mf:
                    bm = AudioFileClip(mf).with_duration(v.duration).with_volume_scaled(0.15)
                    v = CompositeAudioClip([v, bm])

            # --- BACKGROUND LOGIC ---
            bgs = glob.glob("**/backgrounds/*.*", recursive=True)
            if bgs:
                bg = ImageClip(random.choice(bgs)).with_duration(v.duration).resized(width=1280)
            else:
                bg = ColorClip(size=(1280, 720), color=(135, 206, 235)).with_duration(v.duration)

            pre = "character" if char == "Shinchan" else "character2"
            cp, op = find(f"{pre}_closed*.png"), find(f"{pre}_open*.png")
            
            if not cp or not op:
                st.error("Images missing on GitHub!")
                st.stop()

            # --- TRANSPARENCY & POSITION FIX ---
            def prep_char(path):
                # We use .memoize() or .resized to ensure it fits the frame
                img = ImageClip(path).with_duration(0.15).resized(height=450)
                return img

            c, o = prep_char(cp), prep_char(op)
            
            # Animate the talking mouth
            act = concatenate_videoclips([c, o] * int(v.duration/0.3 + 1)).with_duration(v.duration)
            
            # Position character at the bottom center
            act = act.with_position(("center", "bottom"))

            fin = CompositeVideoClip([bg, act], size=(1280, 720)).with_audio(v)
            fin.write_videofile("out.mp4", fps=24, preset="ultrafast", logger=None)
            status.update(label="✅ Ready!", state="complete")

        st.video("out.mp4")
        with open("out.mp4", "rb") as f:
            st.download_button("📥 Download", data=f, file_name="video.mp4")
    except Exception as e:
        st.error(f"Error: {e}")
