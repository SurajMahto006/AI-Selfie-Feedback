# 🤖 AI Selfie Feedback

An intelligent real-time selfie evaluator using Python, OpenCV, MediaPipe, and pyttsx3. It provides feedback on your pose, smile, head tilt, and emotion — and automatically captures your best selfies!

---

## 📸 Features

- ✅ Real-time webcam pose analysis using MediaPipe
- 😊 Emotion detection simulation (Happy, Neutral, Sad, Angry)
- 📏 Head tilt & eye openness checks
- 🟩 Green box around face area for visual feedback
- 🗣️ Voice guidance using pyttsx3
- 🎯 Live selfie scoring (0–100)
- 💾 Auto-save selfie if score is high and mood is Happy
- 🧠 Stats dashboard inside OpenCV window
- 💻 Simple and clean codebase, easy to extend

---

## 🗂️ Project Structure

AI-Selfie-Feedback/
├── selfie_feedbackai.py # Main Python file
├── selfies/ # Auto and manual selfies saved here
└── requirements.txt # Python dependencies
▶️ How to Run

python selfie_feedbackai.py
Then:

Press s to take a selfie manually

Press q to quit
quit

📥 Output
Your selfies will be saved in the /selfies/ folder

Score and emotion will be shown on the video feed

Voice will guide you when you look good 📢

📦 Requirements (requirements.txt)
opencv-python
mediapipe
numpy
pyttsx3
Pillow

🚀 Future Enhancements
Real facial emotion detection (using deep learning models)

Live beauty filters (blur skin, smooth tone)

Upload selfies to cloud or Google Drive

GUI version using Tkinter or PyQt5

window

💻 GitHub Upload Instructions (With Git)
✅ One-time Git Setup:
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

🔃 Steps to upload your folder to GitHub:
cd path/to/your/AI-Selfie-Feedback
git init
git add .
git commit -m "Initial commit for AI Selfie Feedback project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/AI-Selfie-Feedback.git
git push -u origin main

📚 License
This project is open-source and free to use under the MIT License.

🙋‍♂️ Created By
Suraj Mahto
AI Enthusiast | B.E Student | Developer
GitHub: SurajMahto006
