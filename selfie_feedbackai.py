import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time
import os
from datetime import datetime

# Voice engine setup
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# MediaPipe setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Create folder for selfies
if not os.path.exists("selfies"):
    os.makedirs("selfies")

# Stats
selfie_count = 0
best_score = 0
current_emotion = "Neutral"
last_emotion = ""
last_emotion_time = time.time()

# Dummy emotion detection
emotions = ["Happy", "Sad", "Neutral", "Angry"]
emojis = {
    "Happy": "😊",
    "Sad": "😢",
    "Neutral": "😐",
    "Angry": "😠"
}

def detect_emotion():
    return current_emotion  # Stable until expression analysis is real

# Webcam Setup
frame_width, frame_height = 640, 480
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

last_saved_time = time.time()
last_dashboard_update = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    score = 0
    feedback = []

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Smile approximation
        if len(landmarks) > 10:
            left_mouth = landmarks[9]
            right_mouth = landmarks[10]
            mouth_width = abs(right_mouth.x - left_mouth.x)
            if mouth_width > 0.10:
                current_emotion = "Happy"
                score += 40
                feedback.append("Nice smile")
            else:
                current_emotion = "Neutral"

        # Eyes open approximation
        if len(landmarks) > 11:
            left_eye = landmarks[2].y
            left_shoulder = landmarks[11].y
            if abs(left_shoulder - left_eye) > 0.1:
                score += 30
                feedback.append("Eyes open")

        # Head tilt check
        if len(landmarks) > 12:
            shoulder_diff = abs(landmarks[11].y - landmarks[12].y)
            if shoulder_diff < 0.05:
                score += 30
                feedback.append("Good head tilt")

    emoji = emojis.get(current_emotion, "😐")

    if score > best_score:
        best_score = score
        speak("Great pose!")

    # Auto selfie every 10 sec only for happy mood
    if time.time() - last_saved_time > 10 and current_emotion == "Happy":
        selfie_count += 1
        filename = f"selfies/selfie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(filename, frame)
        last_saved_time = time.time()
        speak("Selfie taken")

    # Draw larger green rectangle around face area if detected
    h, w, _ = frame.shape
    if results.pose_landmarks:
        if len(landmarks) > 10:
            x_coords = [landmarks[9].x, landmarks[10].x, landmarks[2].x]
            y_coords = [landmarks[9].y, landmarks[10].y, landmarks[2].y]
            min_x = int(min(x_coords) * w) - 60
            max_x = int(max(x_coords) * w) + 60
            min_y = int(min(y_coords) * h) - 100
            max_y = int(max(y_coords) * h) + 60
            cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 3)

    # Score bar
    bar_color = (0, 255, 0) if score >= 70 else (0, 255, 255) if score >= 40 else (0, 0, 255)
    cv2.rectangle(frame, (30, 30), (30 + int(score * 2), 60), bar_color, -1)
    cv2.putText(frame, f"Score: {score}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    # Dashboard inside OpenCV window
    cv2.putText(frame, f"{emoji} {current_emotion}", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)
    cv2.putText(frame, f"Selfies: {selfie_count} | Best: {best_score}", (30, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 255, 200), 2)

    # Show
    cv2.imshow("AI Selfie Feedback", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        selfie_count += 1
        filename = f"selfies/selfie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(filename, frame)
        speak("Manual selfie taken")

cap.release()
cv2.destroyAllWindows()
