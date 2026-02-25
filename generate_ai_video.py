import customtkinter as ctk
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from moviepy.audio.AudioClip import CompositeAudioClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import os
import threading
import random

class HaseebUltimateStudio(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Asif's Bollywood & Hollywood AI Studio")
        self.geometry("750x850")

        ctk.CTkLabel(self, text="AI SCRIPT-TO-VIDEO ENGINE", font=("Arial", 24, "bold"), text_color="red").pack(pady=20)
        
        # 1. Character Selection
        ctk.CTkLabel(self, text="Select Character:").pack()
        self.char_menu = ctk.CTkOptionMenu(self, values=["Shinchan", "Doraemon"])
        self.char_menu.pack(pady=10)

        # 2. Language Selection (Includes Hinglish)
        ctk.CTkLabel(self, text="Select Language:").pack()
        self.lang_menu = ctk.CTkOptionMenu(self, values=["English", "Hindi", "Telugu", "Hinglish"])
        self.lang_menu.pack(pady=10)

        # 3. Music Style Selection
        ctk.CTkLabel(self, text="Background Music Style:").pack()
        self.music_menu = ctk.CTkOptionMenu(self, values=["No Music", "Bollywood Drama", "Hollywood Epic"])
        self.music_menu.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=600, height=150)
        self.textbox.pack(pady=10)
        self.textbox.insert("1.0", "Enter your script here (Hinglish works too!)...")

        self.btn = ctk.CTkButton(self, text="GENERATE VIDEO", command=self.start_thread, height=40, fg_color="green")
        self.btn.pack(pady=20)

        self.status = ctk.CTkLabel(self, text="Ready", text_color="white")
        self.status.pack(pady=10)

    def create_subtitle_image(self, text, duration, lang):
        # Creates a transparent subtitle layer
        img = Image.new('RGBA', (1280, 200), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Background bar for subtitles
        draw.rectangle([100, 50, 1180, 150], fill=(0, 0, 0, 160))
        
        # Font logic
        if lang == "Hindi":
            font_file = "fonts/Hind-Regular.ttf"
        elif lang == "Telugu":
            font_file = "fonts/Ramabhadra-Regular.ttf"
        else: # English or Hinglish
            font_file = "fonts/Hind-Regular.ttf"

        try:
            font = ImageFont.truetype(font_file, 45)
        except:
            font = ImageFont.load_default()

        draw.text((640, 100), text, fill="white", anchor="mm", font=font)
        img.save("temp_sub.png")
        return ImageClip("temp_sub.png").with_duration(duration).with_position(("center", "bottom"))

    def start_thread(self):
        threading.Thread(target=self.process_video_logic).start()

    def process_video_logic(self):
        try:
            script_text = self.textbox.get("1.0", "end-1c")
            lang_choice = self.lang_menu.get()
            
            # Map choice to gTTS engine (Hinglish uses Hindi engine 'hi' for accent)
            lang_map = {"English": "en", "Hindi": "hi", "Telugu": "te", "Hinglish": "hi"}
            
            # 1. Generate Voice
            self.status.configure(text="Generating Voice...", text_color="yellow")
            tts = gTTS(text=script_text, lang=lang_map[lang_choice])
            tts.save("temp.mp3")
            voice = AudioFileClip("temp.mp3")

            # 2. Mix Background Music (v2 FIX: with_volume_scaled)
            music_choice = self.music_menu.get()
            if music_choice != "No Music":
                bg_music_file = f"music/{music_choice.lower().replace(' ', '_')}.mp3"
                if os.path.exists(bg_music_file):
                    bg_music = AudioFileClip(bg_music_file).with_duration(voice.duration).with_volume_scaled(0.15)
                    voice = CompositeAudioClip([voice, bg_music])

            # 3. Background Image
            bg_folder = "images/backgrounds"
            all_bgs = [f for f in os.listdir(bg_folder) if f.endswith(('.png', '.jpg'))]
            bg_path = os.path.join(bg_folder, random.choice(all_bgs))
            bg = ImageClip(bg_path).with_duration(voice.duration).resized(width=1280)

            # 4. Character Animation
            prefix = "character" if self.char_menu.get() == "Shinchan" else "character2"
            c = ImageClip(f"images/{prefix}_closed.png").with_duration(0.15).resized(width=400)
            o = ImageClip(f"images/{prefix}_open.png").with_duration(0.15).resized(width=400)
            actor = concatenate_videoclips([c, o] * int(voice.duration/0.3 + 1)).with_duration(voice.duration).with_position((440, 320))

            # 5. Subtitles
            subs = self.create_subtitle_image(script_text, voice.duration, lang_choice)

            # 6. Final Render
            self.status.configure(text="Rendering Video...", text_color="orange")
            final = CompositeVideoClip([bg, actor, subs], size=(1280, 720)).with_audio(voice)
            os.makedirs("output", exist_ok=True)
            final.write_videofile("output/studio_result.mp4", fps=24, preset="ultrafast", logger=None)
            self.status.configure(text="✅ Video Saved in 'output' folder!", text_color="green")
            
        except Exception as e:
            self.status.configure(text=f"Error: {str(e)}", text_color="red")

if __name__ == "__main__":
    app = HaseebUltimateStudio()
    app.mainloop()