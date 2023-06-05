#Importar flask y otras bibliotecas necesarias para el proyecto
from flask import Flask, request, jsonify, send_file, render_template
#import requests #Generación de archivo de audio .mp3 
from gtts import gTTS #Audio en línea
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import pipeline

#Iniciar la aplicación flask
app = Flask(__name__)

# Iniciar la aplicación Flask
app = Flask(__name__)

# Ruta principal para renderizar el formulario HTML
@app.route('/')
def home():
    return render_template('index.html')

#Definir ruta para recibir la imagen cargada por los usuarios y generar el audio correspondiente:
@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    # Obtener la imagen cargada por el usuario
    image_file = request.files['image']
    raw_image = Image.open(image_file).convert('RGB')

    # Inicializar los modelos y procesadores
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    #model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda") #Maquina con GPU NVIDIA
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large") #Maquina sin GPU NVIDEA
    #model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-small") #Modelo mas liviano
    traductor = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")

    # Generar la descripción de la imagen
    
    #inputs = processor(raw_image, return_tensors="pt").to("cuda") #NVIDIA
    inputs = processor(raw_image, return_tensors="pt") #NO NVIDIA

    out = model.generate(**inputs)
    out_image = processor.decode(out[0], skip_special_tokens=True)

    # Traducir la descripción al español
    traduccion = traductor(out_image)[0]['translation_text']

    # Buscar las palabras
    palabras_busqueda = ["cuchillo", "cristal", "tabla de cortar"]
    palabras_encontradas = []
    texto = f"No se detectan peligros en la imagen. La descripción de la imagen es: {traduccion}"

    for palabra in palabras_busqueda:
        if palabra in traduccion:
            palabras_encontradas.append(palabra)
            if len(palabras_encontradas) > 1:
                texto = f"Precaución, existen en la imagen los siguientes objetos: '{palabras_encontradas}'. La descripción de la imagen es: {traduccion}"
            elif len(palabras_encontradas) == 1:
                texto = f"Precaución, existe en la imagen el siguiente objeto: '{palabras_encontradas}'. La descripción de la imagen es: {traduccion}"

    # Obtener el audio (API de Google Text-to-Speech)
    #response = requests.get(f"https://translate.google.com/translate_tts?ie=UTF-8&tl=es&client=tw-ob&q={texto}")

    # Guardar el audio en archivo
    #audio_file = 'output.mp3'
    #with open(audio_file, 'wb') as f:
    #    f.write(response.content)
    
    #Generar el audio en línea utilizando gTTS
    tts = gTTS(text=texto, lang='es')
    audio_file = 'output.mp3'
    tts.save(audio_file)

    return send_file(audio_file, mimetype='audio/mpeg')

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run()

