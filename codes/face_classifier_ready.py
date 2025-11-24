import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import image_dataset_from_directory
import matplotlib.pyplot as plt
import os
import json
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(base_dir, "dataset")

train_data = image_dataset_from_directory(
    dataset_path,
    image_size=(128, 128),
    batch_size=8,
    label_mode='categorical',
    validation_split=0.2,
    subset="training",
    seed=42
)

val_data = image_dataset_from_directory(
    dataset_path,
    image_size=(128, 128),
    batch_size=8,
    label_mode='categorical',
    validation_split=0.2,
    subset="validation",
    seed=42
)

model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(len(train_data.class_names), activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_data, validation_data=val_data, epochs=10)

model.save(os.path.join(base_dir, "face_model.keras"))
with open(os.path.join(base_dir, "class_names.json"), "w") as f:
    json.dump(train_data.class_names, f)

if "--no-show" in sys.argv:
    import matplotlib
    matplotlib.use('Agg')

plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Validation')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
