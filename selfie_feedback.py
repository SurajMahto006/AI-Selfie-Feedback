import cv2
import mediapipe as mp
import numpy as np
import time

# Init MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
best_score = 0

def get_pose_score(landmarks, image_w, image_h):
    def px(idx):
        return int(landmarks[idx].x * image_w), int(landmarks[idx].y * image_h)
    
    left_eye = px(33)
    right_eye = px(263)
    nose = px(1)
    chin = px(152)
    top_lip = px(13)
    bottom_lip = px(14)
    left_lip = px(61)
    right_lip = px(291)
    left_eye_top = px(159)
    left_eye_bottom = px(145)
    right_eye_top = px(386)
    right_eye_bottom = px(374)

    eye_level_diff = abs(left_eye[1] - right_eye[1])
    centered = abs(nose[0] - image_w // 2) < 50
    upright = eye_level_diff < 15
    head_straight = abs(nose[1] - chin[1]) < image_h // 3
    lip_gap = bottom_lip[1] - top_lip[1]
    mouth_width = right_lip[0] - left_lip[0]
    smiling = lip_gap > 10 and mouth_width > 60

    # Head tilt (if eyes aren't horizontally aligned)
    tilt_left = left_eye[1] > right_eye[1] + 10
    tilt_right = right_eye[1] > left_eye[1] + 10
    head_tilted = tilt_left or tilt_right

    # Eye openness (closed if gap too small)
    left_eye_open = (left_eye_bottom[1] - left_eye_top[1]) > 5
    right_eye_open = (right_eye_bottom[1] - right_eye_top[1]) > 5
    eyes_open = left_eye_open and right_eye_open

    score = 0
    if centered: score += 30
    if upright: score += 20
    if head_straight: score += 20
    if smiling: score += 10
    if not head_tilted: score += 10
    if eyes_open: score += 10

    return score, centered, upright, head_straight, smiling, not head_tilted, eyes_open

def get_feedback(score, c, u, s, smile, tilt, eyes):
    if score >= 95:
        return "✅ Amazing! Perfect selfie 😍"
    if not eyes:
        return "😴 Open your eyes!"
    if not tilt:
        return "↔️ Keep your head straight"
    if not c:
        return "👤 Center your face"
    if not u:
        return "🧍 Straighten your head"
    if not s:
        return "📏 Adjust head height"
    if not smile:
        return "😊 Give us a smile!"
    return "📸 Almost there! Keep going"

while True:
    success, frame = cap.read()
    if not success:
        break

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                                      landmark_drawing_spec=None,
                                      connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1))

            score, c, u, s, smile, tilt, eyes = get_pose_score(face_landmarks.landmark, w, h)
            feedback = get_feedback(score, c, u, s, smile, tilt, eyes)

            # Save best selfie
            if score > best_score:
                best_score = score
                filename = f"best_selfie_{best_score}_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                print(f"📸 Saved new best selfie: {filename}")

            # Display score bar (color feedback)
            if score >= 90:
                bar_color = (0, 255, 0)
            elif score >= 60:
                bar_color = (0, 255, 255)
            else:
                bar_color = (0, 0, 255)

            cv2.rectangle(frame, (20, 20), (20 + int(score * 3), 50), bar_color, -1)
            cv2.putText(frame, f"Score: {score}/100", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, feedback, (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    cv2.imshow("🤖 AI Selfie Feedback", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):
        filename = f"manual_selfie_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 Manual selfie saved as {filename}")

cap.release()
cv2.destroyAllWindows()
