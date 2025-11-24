import os
import cv2
import numpy as np
import tensorflow as tf
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
test_dir = os.path.join(base_dir, "test_images")

model = tf.keras.models.load_model(os.path.join(base_dir, "face_model.keras"))

with open(os.path.join(base_dir, "class_names.json"), "r") as f:
    class_names = json.load(f)

print("🔎 Результати передбачення:")

for file_name in os.listdir(test_dir):
    if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        file_path = os.path.join(test_dir, file_name)

        img = cv2.imread(file_path)
        if img is None:
            print(f"[Пропущено] {file_name} — не вдалося завантажити")
            continue

        try:
            img_resized = cv2.resize(img, (128, 128)) / 255.0
            img_batch = np.expand_dims(img_resized, axis=0)

            prediction = model.predict(img_batch)
            predicted_class = np.argmax(prediction)
            confidence = np.max(prediction)

            print(f"{file_name}: {class_names[predicted_class]} (ймовірність: {confidence:.2f})")

        except Exception as e:
            print(f"[Помилка] {file_name}: {e}")
