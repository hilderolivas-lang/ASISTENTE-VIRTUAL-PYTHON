# =====================================================
# ASISTENTE INTELIGENTE - VERSION 1
# Autor: Hilder olivas
#
# Funciones:
# - Reconocimiento de voz
# - Voz natural con Edge-TTS
# - Registro de nombre
# - Conversación básica
# - Historial en pantalla
# =====================================================

from flask import Flask, render_template, request

# Reconocimiento de voz
import speech_recognition as sr

# Hilos
import threading

# Voz natural
import asyncio
import edge_tts
import pygame
import os

#NUEVAS LIBRERIAS PARA MAEJO DE ARCHIVOS INVERTIGAR LO QUE HACER CADA UNA 
import shutil
from pathlib import Path

# =====================================================
# CREACION DE LA APLICACION FLASK: NOS SERVIRA PARA PUBLICARLA 
# =====================================================

app = Flask(__name__)

# =====================================================
# VARIABLES GLOBALES
# =====================================================

nombre_usuario = ""

conversacion = []

# =====================================================
# FUNCION DE VOZ NATURAL: ESTA VOZ SE HA CAMBIADO POR LO QUE SE ESCUCHABA MUY ROBOTICA EN EL ARCHIVO PT.PY ESTA 
# OTRA VOZ QUE PUEDEN UTILIZAR SI LES GUSTA. OJO VERIFICAR SI ESTA FUNCIONANDO EL NARRADO EN WINDOWS
# =====================================================

async def generar_voz(texto):

    archivo = "voz.mp3"

    comunicacion = edge_tts.Communicate(
        texto,
        voice="es-MX-DaliaNeural"
    )

    await comunicacion.save(archivo)

    pygame.mixer.init()

    pygame.mixer.music.load(archivo)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.quit()

    if os.path.exists(archivo):
        os.remove(archivo)

# =====================================================
#FUNCIO DE  HABLAR
# =====================================================

def hablar(texto):

    asyncio.run(
        generar_voz(texto)
    )

# =====================================================
# HABLAR EN SEGUNDO PLANO
# =====================================================

def hablar_async(texto):

    hilo = threading.Thread(
        target=hablar,
        args=(texto,)
    )

    hilo.start()

# =====================================================
# ESCUCHAR MICROFONO DE MI LAPTON SI LO COLOCAMOS EN WEB O EN LINEA NO FUNCIONARA NO USA AUN MICROFONO DE NAVEGADOR
# =====================================================

def escuchar():

    reconocedor = sr.Recognizer()

    with sr.Microphone() as source:

        print("Escuchando...")

        reconocedor.adjust_for_ambient_noise(
            source,
            duration=1
        )

        audio = reconocedor.listen(
            source,
            timeout=5,
            phrase_time_limit=8
        )

    texto = reconocedor.recognize_google(
        audio,
        language="es-ES"
    )

    print("Usuario dijo:", texto)

    return texto.lower()


# =====================================================
# ORGANIZAR ARCHIVOS
# =====================================================

def organizar_archivos(carpeta):

    try:

        # ------------------------------------------
        # OBTENER RUTA
        # ------------------------------------------

        usuario = os.getlogin()

        if carpeta == "Descargas":

            ruta = os.path.join(
        "C:\\Users",
        usuario,
        "Downloads"
    )

        elif carpeta == "Escritorio":

         ruta = os.path.join(
        "C:\\Users",
        usuario,
        "Desktop"
    )

        elif carpeta == "Archivos":

         ruta = r"D:\Escritorio\ARCHIVOS"

        else:

            return "No encontré la carpeta."
            
        # ------------------------------------------
        # CREAR CARPETAS DESTINO
        # ------------------------------------------

        pdf_dir = os.path.join(ruta, "PDF")
        imagenes_dir = os.path.join(ruta, "Imagenes")
        videos_dir = os.path.join(ruta, "Videos")
        otros_dir = os.path.join(ruta, "Otros")

        os.makedirs(pdf_dir, exist_ok=True)
        os.makedirs(imagenes_dir, exist_ok=True)
        os.makedirs(videos_dir, exist_ok=True)
        os.makedirs(otros_dir, exist_ok=True)

        contador = 0

        # ------------------------------------------
        # RECORRER ARCHIVOS
        # ------------------------------------------

        for archivo in os.listdir(ruta):

            archivo_completo = os.path.join(
                ruta,
                archivo
            )

            # Ignorar carpetas

            if os.path.isdir(archivo_completo):

                continue

            extension = Path(
                archivo
            ).suffix.lower()

            # --------------------------------------
            # PDF
            # --------------------------------------

            if extension == ".pdf":

                destino = os.path.join(
                    pdf_dir,
                    archivo
                )

            # --------------------------------------
            # IMAGENES
            # --------------------------------------

            elif extension in [

                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".bmp",
                ".webp"

            ]:

                destino = os.path.join(
                    imagenes_dir,
                    archivo
                )

            # --------------------------------------
            # VIDEOS
            # --------------------------------------

            elif extension in [

                ".mp4",
                ".avi",
                ".mov",
                ".mkv"

            ]:

                destino = os.path.join(
                    videos_dir,
                    archivo
                )

            # --------------------------------------
            # ACTIVIDAD DEL ESTUDIANTE
            # Agregar Word, Excel, ZIP,
            # PowerPoint y Python
            # --------------------------------------

            else:

                destino = os.path.join(
                    otros_dir,
                    archivo
                )

            shutil.move(
                archivo_completo,
                destino
            )

            contador += 1

        return (
            f"Se organizaron correctamente "
            f"{contador} archivos."
        )
    except Exception as e:

     return (
            f"Ocurrió un error: {str(e)}"
        )



# =====================================================
# PROCESAR COMANDO : EL QUE YO LE DICTE O HABLE
# =====================================================

def procesar_comando(comando):

    global nombre_usuario

    # -------------------------------------------------
    # SI AUN NO EXISTE NOMBRE
    # -------------------------------------------------

    if nombre_usuario == "":

        nombre_usuario = comando.title()

        return (
        f"Mucho gusto {nombre_usuario}. "
        f"Estoy listo para ayudarte.\n"
        f"Puedes decir:\n"
        f"Organizar archivos,\n"
        f"Dictar texto,\n"
        f"Tomar fotografía,\n"
        f"O salir."
    )

    # -------------------------------------------------
    # OPCION DICTADO
    # -------------------------------------------------

    if "dictar" in comando:

        return (
            "Has seleccionado el modo dictado."
        )

    # -------------------------------------------------
    # OPCION ORGANIZAR
    # -------------------------------------------------

    elif "organizar" in comando:

        respuesta=organizar_archivos (
            "Archivos"
        )
        return respuesta
    # -------------------------------------------------
    # OPCION FOTO
    # -------------------------------------------------

    elif "foto" in comando or "fotografia" in comando:

        return (
            "Has seleccionado tomar fotografía."
        )

    # -------------------------------------------------
    # OPCION SALIR
    # -------------------------------------------------

    elif "salir" in comando:

        return (
            "Hasta luego."
        )

    # -------------------------------------------------
    # COMANDO DESCONOCIDO
    # -------------------------------------------------

    else:

        return (
            "No entendí el comando."
        )

# =====================================================
# PAGINA PRINCIPAL, ESTO ES PARA UTILIZAR MI HTML CON EL ASISTENTE
# =====================================================

@app.route("/", methods=["GET", "POST"])

def inicio():

    global conversacion

    mensaje_error = ""

    if request.method == "POST":

        try:

            texto_usuario = escuchar()

            respuesta_asistente = procesar_comando(
                texto_usuario
            )

            conversacion.append({

                "usuario": texto_usuario,

                "respuesta": respuesta_asistente

            })

            hablar_async(
                respuesta_asistente
            )

        except Exception as e:

            mensaje_error = str(e)

            print(e)

    return render_template(

        "index.html",

        nombre=nombre_usuario,

        conversacion=conversacion,

        error=mensaje_error

    )

# =====================================================
# INICIO DEL PROGRAMA
# =====================================================

if __name__ == "__main__":

    print("ASISTENTE INICIADO")

    hablar_async(
        "Hola. Soy tu asistente virtual. "
        "Por favor dime tu nombre."
    )

    app.run(
        debug=False
    )
    