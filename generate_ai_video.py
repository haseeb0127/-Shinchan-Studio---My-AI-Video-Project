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
                
                v = AudioFileClip(tmp)
                bgs = glob.glob("**/backgrounds/*.*", recursive=True)
                bg = ImageClip(random.choice(bgs)).with_duration(v.duration).resized(width=1280) if bgs else ColorClip((1280, 720), (100,150,200)).with_duration(v.duration)

                pre = "character" if i % 2 == 0 else "character2"
                cp, op = find(f"{pre}_closed*.png"), find(f"{pre}_open*.png")
                
                if cp and op:
                    c, o = ImageClip(cp).with_duration(0.15).resized(height=450), ImageClip(op).with_duration(0.15).resized(height=450)
                    act = concatenate_videoclips([c, o]*int(v.duration/0.3 + 1)).with_duration(v.duration).with_position(("center","bottom"))
                    scn = CompositeVideoClip([bg, act], size=(1280, 720)).with_audio(v)
                else:
                    scn = CompositeVideoClip([bg], size=(1280, 720)).with_audio(v)
                clips.append(scn)

            fin = concatenate_videoclips(clips)
            if mus != "No Music":
                mf = find(f"{mus.lower().replace(' ','_')}.mp3")
                if mf:
                    bm = AudioFileClip(mf).with_duration(fin.duration).with_volume_scaled(0.10)
                    fin.audio = CompositeAudioClip([fin.audio, bm])

            fin.write_videofile("out.mp4", fps=24, preset="ultrafast", logger=None)
            status.update(label="✅ Ready!", state="complete")

        st.video("out.mp4")
        with open("out.mp4", "rb") as f:
            st.download_button("📥 Download", data=f, file_name="vid.mp4")
    except Exception as e:
        st.error(f"Error: {e}")
