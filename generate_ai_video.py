import streamlit as st  # <--- THIS MUST BE LINE 1
import google.generativeai as genai
import json
import os
import random
import glob
import time
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, ColorClip, VideoFileClip
import moviepy.video.fx.all as vfx
from gtts import gTTS

# NOW you can use st.secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
import google.generativeai as genai
import json

# 1. Initialize the Brain
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

if st.button("🚀 Generate Animated Video"):
    try:
        with st.status("🧠 AI Director is analyzing your script...", expanded=True) as status:
            # 2. The Prompt (Instructions for the AI)
            prompt = f"""
            Break this script into logical scenes for an educational video.
            Script: {script}
            
            Return ONLY a JSON list like this:
            [
              {{"text": "dialogue here", "char": "character1", "bg_search": "classroom"}},
              {{"text": "next dialogue", "char": "character2", "bg_search": "office"}}
            ]
            """
            
            # 3. Get AI Response
            response = model.generate_content(prompt)
            # Clean the response text to ensure it's valid JSON
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            scenes = json.loads(clean_json)
            
            st.write(f"🎬 Director planned {len(scenes)} scenes.")
            
            clips = []
            for i, scene in enumerate(scenes):
                st.write(f"⚙️ Rendering Scene {i+1}: {scene['char']} in {scene['bg_search']}")
                
                # --- AUDIO GENERATION ---
                tts = gTTS(text=scene['text'], lang=l_map[lang])
                tmp_audio = f"scene_{i}.mp3"
                tts.save(tmp_audio)
                audio_clip = AudioFileClip(tmp_audio)
                
                # --- BACKGROUND PICKER ---
                # Search for a background that matches the AI's suggestion
                bg_files = glob.glob("**/backgrounds/*.*", recursive=True)
                bg_match = [f for f in bg_files if scene['bg_search'].lower() in f.lower()]
                selected_bg = random.choice(bg_match if bg_match else bg_files)
                
                bg_clip = ImageClip(selected_bg).set_duration(audio_clip.duration).resize(width=1280)

                # --- CHARACTER PICKER ---
                gif_path = find(f"{scene['char']}*.gif")
                if gif_path:
                    char_clip = (VideoFileClip(gif_path, has_mask=True)
                                 .resize(height=450)
                                 .fx(vfx.loop, duration=audio_clip.duration)
                                 .set_position(("center","bottom")))
                    final_scene = CompositeVideoClip([bg_clip, char_clip], size=(1280, 720)).set_audio(audio_clip)
                else:
                    final_scene = bg_clip.set_audio(audio_clip)
                
                clips.append(final_scene)

            # 4. Final Assembly
            video = concatenate_videoclips(clips)
            video.write_videofile("out.mp4", fps=24, preset="ultrafast", logger=None)
            status.update(label="✅ Video Produced!", state="complete")

        st.video("out.mp4")
        
    except Exception as e:
        st.error(f"Founder, we have a glitch: {e}")

