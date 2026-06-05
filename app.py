# =====================================================
# ASISTENTE INTELIGENTE - VERSION 1
# Autor: Hilder
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

# =====================================================
# CREACION DE LA APLICACION FLASK
# =====================================================

app = Flask(__name__)

# =====================================================
# VARIABLES GLOBALES
# =====================================================

nombre_usuario = ""

conversacion = []

# =====================================================
# FUNCION DE VOZ NATURAL
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
# HABLAR
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
# ESCUCHAR MICROFONO
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
# PROCESAR COMANDO
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
            f"¿Qué deseas hacer?"
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

        return (
            "Has seleccionado organizar archivos."
        )

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
# PAGINA PRINCIPAL
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