import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Charger le modèle enregistré
model = tf.keras.models.load_model('mon_modele_v3.h5')

# Fonction pour charger et prétraiter une image
def preprocess_image(img_path, target_size):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

# Fonction pour effectuer la prédiction
def predict_image(img_path):
    img = preprocess_image(img_path, target_size=(500, 500))
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions, axis=1)
    categories = ['texte verticale manquant', 'police differente', ' signature differente','puce manquante','taille photo incorrecte','authentique']  # Adaptez cette liste selon vos catégories
    print(predictions)
    return categories[predicted_class[0]]

# Fonction pour choisir un fichier
def choose_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        result = predict_image(file_path)
        display_result(file_path, result)

# Fonction pour afficher le résultat et l'image choisie
def display_result(img_path, result):
    img = Image.open(img_path)
    img = img.resize((300, 300), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.image = img
    result_label.config(text=result)

# Créer l'interface Tkinter
root = tk.Tk()
root.title("Vérification d'authenticité de l'image")

frame = tk.Frame(root)
frame.pack(pady=20)

choose_button = tk.Button(frame, text="Choisir un fichier", command=choose_file)
choose_button.pack(pady=10)

panel = tk.Label(frame)
panel.pack(pady=10)

result_label = tk.Label(frame, text="", font=("Helvetica", 16))
result_label.pack(pady=10)

root.mainloop()
