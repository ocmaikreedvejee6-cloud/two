import cv2
import os
import numpy as np

# Path to dataset
dataset_path = "dataset"

# Initialize face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

faces = []
labels = []
label_ids = {}
current_id = 0

# Loop through dataset
for root, dirs, files in os.walk(dataset_path):
    for dir_name in dirs:
        person_name = dir_name
        person_path = os.path.join(root, dir_name)

        if person_name not in label_ids:
            label_ids[person_name] = current_id
            current_id += 1

        for file in os.listdir(person_path):
            if file.endswith("jpg") or file.endswith("png"):
                path = os.path.join(person_path, file)

                image = cv2.imread(path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                faces_rect = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(50, 50)
                )

                for (x, y, w, h) in faces_rect:
                    roi = gray[y:y+h, x:x+w]
                    faces.append(roi)
                    labels.append(label_ids[person_name])

# Convert labels
labels = np.array(labels)

# Train LBPH model
recognizer = cv2.face.LBPHFaceRecognizer_create(
    radius=1,
    neighbors=8,
    grid_x=8,
    grid_y=8
)

recognizer.train(faces, labels)

# Save model
recognizer.save("trainer.yml")

# Save labels
np.save("labels.npy", label_ids)

print("✅ Training Complete!")
print("Saved: trainer.yml and labels.npy")
