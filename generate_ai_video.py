import customtkinter as ctk
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_videoclips
from gtts import gTTS
import os
import threading
import random

class HaseebUltimateStudio(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Haseeb's AI Content Studio")
        self.geometry("750x750")

        ctk.CTkLabel(self, text="AI SCRIPT-TO-VIDEO ENGINE", font=("Arial", 24, "bold"), text_color="red").pack(pady=20)
        
        self.char_menu = ctk.CTkOptionMenu(self, values=["Classic Actor", "TV Style Actor"])
        self.char_menu.pack(pady=10)

        self.lang_menu = ctk.CTkOptionMenu(self, values=["English", "Hindi", "Telugu"])
        self.lang_menu.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=600, height=150)
        self.textbox.pack(pady=10)
        self.textbox.insert("1.0", "Welcome to my automated YouTube channel!")

        self.progress = ctk.CTkProgressBar(self, width=500)
        self.progress.pack(pady=20)
        self.progress.set(0)

        self.btn = ctk.CTkButton(self, text="GENERATE SINGLE VIDEO", command=lambda: self.start_thread("single"), height=40, fg_color="green")
        self.btn.pack(pady=5)

        self.bulk_btn = ctk.CTkButton(self, text="RUN BULK MODE (scripts.txt)", command=lambda: self.start_thread("bulk"), height=40, fg_color="blue")
        self.bulk_btn.pack(pady=5)

        self.status = ctk.CTkLabel(self, text="Ready", text_color="white")
        self.status.pack(pady=10)

    def start_thread(self, mode):
        if mode == "single":
            threading.Thread(target=self.generate_single_from_ui).start()
        else:
            threading.Thread(target=self.run_bulk_mode).start()

    def generate_single_from_ui(self):
        script = self.textbox.get("1.0", "end-1c")
        self.process_video_logic(script, "manual_video")

    def run_bulk_mode(self):
        if not os.path.exists("scripts.txt"):
            self.status.configure(text="Error: scripts.txt not found!", text_color="red")
            return
        with open("scripts.txt", "r", encoding="utf-8") as f:
            scripts = [line.strip() for line in f if line.strip()]
        for i, s in enumerate(scripts):
            self.status.configure(text=f"Bulk: Processing {i+1}/{len(scripts)}")
            self.process_video_logic(s, f"bulk_video_{i+1}")
        self.status.configure(text="✅ Bulk Complete!", text_color="green")

    def process_video_logic(self, script_text, filename):
        try:
            lang_map = {"English": "en", "Hindi": "hi", "Telugu": "te"}
            tts = gTTS(text=script_text, lang=lang_map[self.lang_menu.get()])
            tts.save("temp.mp3")
            voice = AudioFileClip("temp.mp3")

            bg_folder = "images/backgrounds"
            all_bgs = [f for f in os.listdir(bg_folder) if os.path.isfile(os.path.join(bg_folder, f))]
            bg_path = os.path.join(bg_folder, random.choice(all_bgs)) if all_bgs else "images/background.png"
            bg = ImageClip(bg_path).with_duration(voice.duration).resized(width=1280)

            prefix = "character" if self.char_menu.get() == "Classic Actor" else "character2"
            c = ImageClip(f"images/{prefix}_closed.png").with_duration(0.15).resized(width=400)
            o = ImageClip(f"images/{prefix}_open.png").with_duration(0.15).resized(width=400)
            actor = concatenate_videoclips([c, o] * int(voice.duration/0.3 + 1)).with_duration(voice.duration).with_position((450, 300))

            final = CompositeVideoClip([bg, actor], size=(1280, 720)).with_audio(voice)
            os.makedirs("output", exist_ok=True)
            final.write_videofile(f"output/{filename}.mp4", fps=24, threads=4, preset="ultrafast", logger=None)
        except Exception as e:
            self.status.configure(text=f"Error: {str(e)}", text_color="red")

if __name__ == "__main__":
    app = HaseebUltimateStudio()
    app.mainloop()