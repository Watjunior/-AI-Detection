from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import UploadImageForm
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import pytesseract
from PIL import Image
from tqdm import tqdm
from .models import CNI

def modele(request):
    return render(request, 'modele.html')

def home(request):
    return render(request, 'accueil.html')

def about(request):
    return render(request, 'about.html')

def choix(request):
    return render(request, 'choix.html')

def contact(request):
    return render(request, 'contact.html')

# Charger le modèle TensorFlow/Keras
model = tf.keras.models.load_model('/home/noel/Documents/projet/CNN/mon_modele_v3.h5')

# Fonction pour charger et prétraiter une image
def preprocess_image(img_path, target_size):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normaliser les valeurs des pixels
    return img_array

# Fonction pour effectuer la prédiction
def predict_image(img_path):
    img = preprocess_image(img_path, target_size=(500, 500))
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions, axis=1)[0]
    categories = ['texte verticale manquant', 'police differente', 'signature differente', 'puce manquante', 'taille photo incorrecte', 'authentique']  # Adaptez cette liste selon vos catégories
    return categories[predicted_class]

# Fonction pour zoomer sur des régions spécifiques de l'image
def zoom_image(input_image_path, zoom_factor, regions):
    img = Image.open(input_image_path)
    zoomed_images = []
    for region in tqdm(regions, desc="Zooming Regions"):
        x1, y1, x2, y2 = region
        width = x2 - x1
        height = y2 - y1
        cropped_img = img.crop((x1, y1, x2, y2))
        zoom_width = int(width * zoom_factor)
        zoom_height = int(height * zoom_factor)
        zoomed_img = cropped_img.resize((zoom_width, zoom_height), Image.LANCZOS)
        zoomed_images.append(zoomed_img)
    return zoomed_images

# Fonction pour extraire le texte d'une image zoomée
def extract_text_from_image(image):
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            fs = FileSystemStorage()
            file_path = fs.save(image_file.name, image_file)
            file_url = fs.url(file_path)

            # Faire une prédiction
            predicted_category = predict_image(os.path.join(settings.MEDIA_ROOT, file_path))

            # Zoomer sur les régions spécifiques et extraire le texte
            regions = [
                (333, 274, 388, 290),  # Exemple de zone
            ]
            zoom_factor = 2.0
            zoomed_images = zoom_image(os.path.join(settings.MEDIA_ROOT, file_path), zoom_factor, regions)

            # Extraire le texte des images zoomées
            all_text = []
            ids =""
            id1=""
            for i, zoomed_image in enumerate(tqdm(zoomed_images, desc="Extracting Text"), start=1):
                text = extract_text_from_image(zoomed_image)
                all_text.append(f"Texte extrait de la zone {i} :\n{text}\n" + "-" * 30)
                ids=text.split()
                id1 = int(ids[0])
            # Vérifier si la catégorie est "authentique" et vérifier l'unicité dans la base de données
            if predicted_category == "authentique":
                numero_cni = id1  # Adaptation selon la structure du texte extrait
                if  CNI.objects.filter(NumeroCni=numero_cni).exists():
                    # Sauvegarder dans la base de données
                    product = CNI.objects.get(NumeroCni=numero_cni)
                    print(product)
                    result = "authentique"
                    return render(request, 'resultat_auth.html', {
                    'product': product,
                    'result':result,
                    'file_url': file_url})
                else:
                    result= "carte d'identite introuvable "
                    return render(request, 'resultat_auth.html', {
                    'result':result,
                    'file_url': file_url
            })
                    
            else:
                result=""
                result = predicted_category
            return render(request, 'result.html', {
                'predicted_category': predicted_category,
                'file_url': file_url,
                'ids': ids,
                'result':result
            })
    else:
        form = UploadImageForm()
    return render(request, 'upload.html', {'form': form})
