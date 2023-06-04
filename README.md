<h1>Proyecto TFM Reconocer Imagen y Reproducir Audio</h1>

<h3>Datos del Trabajo:</h3>

<ul>
<li>Nombre Alumnos: Alejandro Alio, Erick Castillo, Pietro Giacchero, Ivan Reyes</li>
<li>Profesor Guia: Abilio Romero</li>
<li>Director de Master: Rafael Muñoz Gil</li>
</ul><br>

<h3>Antecedentes:</h3><br>

<p>Este proyecto tiene por objeto el generar una aplicación que mediante el uso de modelos, solucione un problema de negocio como es el poder describir imagenes mediante audio para personas con problemas visuales y les indique si alguno de los objetos identificados en la imagen representa un peligro, junto con describir la imagen observada.</p> <br>

<h3>Archivos:</h3><br>

<ol>
  <li>README.md: Archivo de presentación del proyecto</li>
  <li>app.py: Archivo con el codigo pythonb y los  modelos empleados para la aplicación</li>
  <li>index.html: HTML para generar la interfaz de usuario y desplegar el modelo en un navegador</li>
  <li>output.mp3: Archivo de audio generado por el modelo, este se va actualizando con cada ejecución del modelo</li>
</ol>

<h3>Descripción de la app:</h3><br>

<h2>Explicación del código</h2>

<p>El siguiente código es un ejemplo de una aplicación web utilizando el framework Flask en Python. La aplicación permite a los usuarios cargar una imagen y generar un archivo de audio correspondiente a una descripción de la imagen.</p>

<h3>Importar las bibliotecas necesarias:</h3>

<p>El código importa las siguientes bibliotecas:</p>

<ul>
  <li><code>Flask</code>: El framework web utilizado para construir la aplicación.</li>
  <li><code>request</code>: Proporciona funcionalidades para manejar las solicitudes HTTP.</li>
  <li><code>jsonify</code>: Utilizado para serializar las respuestas en formato JSON.</li>
  <li><code>send_file</code>: Permite enviar archivos como respuesta HTTP.</li>
  <li><code>render_template</code>: Utilizado para renderizar plantillas HTML.</li>
  <li><code>requests</code>: Permite realizar solicitudes HTTP a otros servidores.</li>
  <li><code>Image</code> (de la biblioteca PIL): Proporciona funciones para manipular imágenes.</li>
  <li><code>BlipProcessor</code> y <code>BlipForConditionalGeneration</code> (de la biblioteca Transformers): Utilizados para procesar y generar descripciones de imágenes.</li>
  <li><code>pipeline</code> (de la biblioteca Transformers): Permite utilizar modelos preentrenados para tareas de procesamiento del lenguaje natural.</li>
</ul>

<h3>Iniciar la aplicación Flask:</h3>

<pre><code>app = Flask(__name__)
</code></pre>

<h3>Definir la ruta principal ("/") para renderizar un formulario HTML:</h3>

<pre><code>@app.route('/')
def home():
    return render_template('index.html')
</code></pre>

<h3>Definir la ruta "/generate-audio" para recibir la imagen cargada por los usuarios y generar el audio correspondiente:</h3>

<pre><code>@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    # Obtener la imagen cargada por el usuario
    image_file = request.files['image']
    raw_image = Image.open(image_file).convert('RGB')

    # ... (Procesamiento de la imagen y generación de la descripción)

    # Obtener el audio (API de Google Text-to-Speech)
    response = requests.get(f"https://translate.google.com/translate_tts?ie=UTF-8&amp;tl=es&amp;client=tw-ob&amp;q={texto}")

    # Guardar el audio en archivo
    audio_file = 'output.mp3'
    with open(audio_file, 'wb') as f:
        f.write(response.content)

    return send_file(audio_file, mimetype='audio/mpeg')
</code></pre>

<p>En esta función, se obtiene la imagen cargada por el usuario, se procesa utilizando un modelo preentrenado para generar una descripción de la imagen en inglés. Luego, se traduce la descripción al español utilizando otro modelo preentrenado. A continuación, se busca si la descripción contiene ciertas palabras clave y se genera un texto de precaución en caso de encontrarlas. Finalmente, se utiliza la API de Google Text-to-Speech
