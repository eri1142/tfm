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

<p>La app utiliza el modelo "Blip Image Captioning" de Hugging Face para generar descripciones de imágenes y realizar algunas acciones adicionales con los resultados obtenidos. A continuación, te explico paso a paso el código:</p>

<ol>
  <li><strong>Importar las bibliotecas necesarias:</strong>
    <ul>
      <li><code>requests</code>: se utiliza para realizar solicitudes HTTP, en este caso para descargar la imagen.</li>
      <li><code>PIL</code> (Python Imaging Library): se utiliza para abrir y manipular la imagen descargada.</li>
      <li><code>transformers</code>: se utiliza para trabajar con modelos de procesamiento de lenguaje natural (NLP).</li>
    </ul>
  </li>

  <li><strong>Descargar la imagen:</strong>
    <ul>
      <li>Se utiliza <code>requests.get</code> para descargar la imagen desde la URL especificada.</li>
      <li><code>Image.open</code> se utiliza para abrir la imagen descargada.</li>
      <li><code>.convert('RGB')</code> se utiliza para convertir la imagen a modo RGB.</li>
    </ul>
  </li>

  <li><strong>Inicializar los modelos y procesadores:</strong>
    <ul>
      <li><code>BlipProcessor</code> y <code>BlipForConditionalGeneration</code> son modelos preentrenados proporcionados por Hugging Face.</li>
      <li>Se carga el procesador y el modelo preentrenados usando <code>from_pretrained</code>.</li>
      <li><code>pipeline</code> se utiliza para inicializar un modelo de traducción preentrenado.</li>
    </ul>
  </li>

  <li><strong>Generar la descripción de la imagen:</strong>
    <ul>
      <li>Se procesa la imagen descargada utilizando el procesador (<code>processor</code>) para prepararla como entrada para el modelo.</li>
      <li>Luego, se genera la descripción utilizando el modelo (<code>model.generate</code>).</li>
      <li>La descripción generada se decodifica utilizando el procesador para obtener el texto final (<code>processor.decode</code>).</li>
    </ul>
  </li>

  <li><strong>Traducir la descripción al español:</strong>
    <ul>
      <li>Se utiliza el modelo de traducción (<code>traductor</code>) para traducir la descripción generada al español.</li>
      <li>La traducción se obtiene de la primera entrada en el resultado (<code>traductor(out_image)[0]['translation_text']</code>).</li>
    </ul>
  </li>

  <li><strong>Buscar las palabras:</strong>
    <ul>
      <li>Se define una lista de palabras de búsqueda (<code>palabras_busqueda</code>) que se desean encontrar en la descripción.</li>
      <li>Se inicializa una lista vacía (`palabras_encontradas`) para almacenar las palabras encontradas.</li>
      <li>Se recorre cada palabra de búsqueda y se verifica si está presente en la descripción traducida.</li>
      <li>Si se encuentra una palabra, se agrega a la lista de palabras encontradas y se actualiza el texto con una advertencia específica para esa palabra.</li>
    </ul>
  </li>

  <li><strong>Obtener el audio a través de la API de Google Text-to-Speech:</strong>
    <ul>
      <li>Se realiza una solicitud GET a la API de Google Text-to-Speech para convertir el texto en audio en español.</li>
      <li>La URL de la solicitud incluye el texto (<code>`q={texto}`</code>) y otros parámetros como el idioma (<code>`tl=es`</code>).</li>
    </ul>
  </li>

  <li><strong>Guardar el audio en un archivo:</strong>
    <ul>
      <li>Se guarda la respuesta de la API de Google Text-to-Speech en un archivo de audio (<code>`output.mp3`</code>).</li>
    </ul>
  </li>

<li><strong>Reproducir el audio:</strong>
    <ul>
      <li>Finalmente, se utiliza la biblioteca <code>`IPython.display.Audio`</code> para reproducir el archivo de audio generado.</li>
    </ul>
  </li>

<!-- Explicación del codigo -->

<h3>Explicación del código</h3><br>

<p>El código del archivo <strong>app.py</strong> es un ejemplo de una aplicación web utilizando el framework Flask en Python. La aplicación permite a los usuarios cargar una imagen y generar un archivo de audio correspondiente a una descripción de la imagen.</p>

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

<h3>Uso de la app:</h3><br>

<p>Una vez clonado el repositorio para ejecutar la app en el terminal se debe acceder a la carpeta del proyecto y ejecutar en el terminal el codigo: <strong>python3 app.py</strong>, al ejecutar app.py, deberías poder acceder al formulario HTML en la ruta principal <strong>(http://localhost:5000)</strong> y enviar una imagen para generar el audio correspondiente.</p>
  