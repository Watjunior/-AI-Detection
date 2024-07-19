import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Préparation des données
datagen = ImageDataGenerator(rescale=0.2, validation_split=0.2)

train_generator = datagen.flow_from_directory(
    'data3/',
    target_size=(500, 500),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    'data3/',
    target_size=(500, 500),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)


num_categories = 6  # Assurez-vous de mettre le bon nombre de catégories

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(500, 500, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(num_categories, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])


# Entraînement du modèle
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size,
    epochs=5
)

model.save('mon_modele_v3.h5')

# Évaluation du modèle
loss, accuracy = model.evaluate(validation_generator)
print(f'Accuracy: {accuracy * 100:.2f}%')


