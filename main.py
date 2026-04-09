import cv2
import numpy as np
import serial
import time
import requests

# ================= CONFIG =================
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

TELEGRAM_TOKEN = "8490765768:AAFU-Vpi0HAiS5_2V2mcboWYeiG8W4neiVE"
CHAT_ID = "437470295"

CONFIDENCE_THRESHOLD = 70  # LOWER = more strict match

FACE_TIMEOUT = 3
TELEGRAM_COOLDOWN = 30

last_face_time = 0
last_telegram_time = 0
system_on = False
unknown_triggered = False
# =========================================

# ================= LOAD MODEL =================
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer1.yml")

label_map = np.load("labels1.npy", allow_pickle=True).item()

# ================= FACE DETECTOR =================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ================= ARDUINO =================
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

# ================= TELEGRAM =================
def send_telegram_image(image_path, message):
    global last_telegram_time

    now = time.time()
    if now - last_telegram_time < TELEGRAM_COOLDOWN:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    try:
        with open(image_path, "rb") as photo:
            requests.post(
                url,
                files={"photo": photo},
                data={"chat_id": CHAT_ID, "caption": message},
                timeout=10
            )

        last_telegram_time = now
        print("Telegram sent")

    except Exception as e:
        print("Telegram error:", e)

# ================= MAIN LOOP =================
print("System Running (LBPH TEST MODE)...")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    now = time.time()

    # ================= FACE DETECTED =================
    if len(faces) > 0:
        last_face_time = now

        if not system_on:
            arduino.write(b'ON\n')
            system_on = True
            print("Face detected ? RELAYS ON")

        unknown_triggered = False

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]

            try:
                label, confidence = recognizer.predict(face)
            except Exception as e:
                print("Prediction error:", e)
                continue

            # ===== KNOWN FACE =====
            if confidence < CONFIDENCE_THRESHOLD:
                name = label_map.get(label, "Unknown")
                print(f"Known: {name} | Confidence: {confidence:.2f}")

            # ===== UNKNOWN FACE =====
            else:
                print(f"Unknown detected | Confidence: {confidence:.2f}")

                if not unknown_triggered:
                    img_path = "unknown.jpg"
                    cv2.imwrite(img_path, frame)

                    send_telegram_image(
                        img_path,
                        f"Unknown person detected!\nConfidence: {confidence:.2f}"
                    )

                    unknown_triggered = True

    # ================= NO FACE =================
    else:
        if system_on and (now - last_face_time > FACE_TIMEOUT):
            arduino.write(b'OFF\n')
            system_on = False
            print("No face ? RELAYS OFF")

    time.sleep(0.2)
