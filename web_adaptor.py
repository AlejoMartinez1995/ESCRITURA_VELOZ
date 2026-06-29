'''
Adaptador Genérico de Escritorio a Web (web_adaptor.py)
Poné este archivo al lado de tu proyecto de escritura original.
'''
from flask import Flask, render_template_string, jsonify
import importlib
import random

app = Flask(__name__)

# 1. CONFIGURACIÓN DEL NOMBRE DE TU ARCHIVO
# Poné acá adentro el nombre exacto de tu archivo original SIN el .py
# Por ejemplo, si tu archivo se llama 'script_escritura.py', poné 'script_escritura'
NOMBRE_ARCHIVO_ORIGINAL = 'test_escritura' 

try:
    # El adaptador importa dinámicamente tu lógica de fondo
    proyecto_original = importlib.import_module(NOMBRE_ARCHIVO_ORIGINAL)
    # Extraemos la lista de frases de tu clase TypingSpeedTest usando metaprogramación
    # Si no la encuentra, usa una lista de respaldo por seguridad
    if hasattr(proyecto_original, 'TypingSpeedTest'):
        instancia_dummy = proyecto_original.TypingSpeedTest.__new__(proyecto_original.TypingSpeedTest)
        PHRASES = getattr(instancia_dummy, 'phrases', [])
    else:
        PHRASES = []
except Exception:
    PHRASES = []

# Respaldo por si falla la importación dinámica de la lista
if not PHRASES:
    PHRASES = [
        "El rapido zorro marron salta sobre el perro perezoso.",
        "La lluvia en Sevilla es una maravilla para los ojos.",
        "Python es un lenguaje de programacion versatil y poderoso.",
        "La practica hace al maestro, y la perseverancia es la clave del exito.",
        "El conocimiento es poder, y la educacion es la llave para desbloquearlo."
    ]

# 2. INTERFAZ WEB AUTOMÁTICA
HTML_BASE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Typing Speed Test - Web Adaptor</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            margin-top: 50px; 
            background-color: #f4f7f6; 
            color: #333;
        }
        .contenedor {
            background: white; 
            padding: 30px; 
            display: inline-block; 
            border-radius: 8px; 
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            max-width: 600px;
            width: 90%;
        }
        h2 { color: #028090; margin-bottom: 20px; }
        .frase-caja {
            font-size: 1.2rem;
            background: #eef1f6;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-weight: 500;
            min-height: 30px;
        }
        input[type="text"] { 
            width: 100%; 
            padding: 12px; 
            margin-bottom: 20px; 
            border: 2px solid #ccc; 
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 1.1rem;
        }
        input[type="text"]:focus { border-color: #00a896; outline: none; }
        button { 
            padding: 12px 25px; 
            background-color: #00a896; 
            color: white; 
            border: none; 
            border-radius: 4px; 
            font-size: 16px;
            cursor: pointer; 
            font-weight: bold;
            margin-bottom: 20px;
        }
        button:hover { background-color: #028090; }
        .resultado { font-size: 1.2rem; font-weight: bold; margin-top: 15px; min-height: 25px; }
        .correcto { color: #2a9d8f; }
        .incorrecto { color: #e63946; }
    </style>
</head>
<body>
    <div class="contenedor">
        <h2>Typing Speed Test</h2>
        <div id="frase" class="frase-caja">Presiona 'Iniciar' para comenzar la prueba de escritura.</div>
        <button id="btn-inicio" onclick="iniciarTest()">Iniciar</button>
        <input type="text" id="entrada-usuario" onkeypress="verificarEnter(event)" disabled placeholder="Hacé clic en Iniciar...">
        <div id="resultado" class="resultado"></div>
    </div>

    <script>
        let tiempoInicio = 0;
        let fraseActual = "";

        async function iniciarTest() {
            const respuesta = await fetch('/obtener-frase');
            const data = await respuesta.json();
            
            fraseActual = data.frase;
            document.getElementById('frase').innerText = fraseActual;
            
            const entrada = document.getElementById('entrada-usuario');
            entrada.value = "";
            entrada.disabled = false;
            entrada.focus();
            
            document.getElementById('resultado').innerText = "";
            tiempoInicio = performance.now();
        }

        function verificarEnter(event) {
            if (event.key === 'Enter') {
                const tiempoFin = performance.now();
                const tiempoTranscurrido = (tiempoFin - tiempoInicio) / 1000;
                
                const entrada = document.getElementById('entrada-usuario').value;
                const resultadoDiv = document.getElementById('resultado');
                
                if (entrada === fraseActual) {
                    const cantidadPalabras = entrada.split(/\s+/).filter(Boolean).length;
                    const wpm = (cantidadPalabras / tiempoTranscurrido) * 60;
                    const accuracy = (entrada.length / fraseActual.length) * 100;
                    
                    resultadoDiv.className = "resultado correcto";
                    resultadoDiv.innerText = `¡Correcto! ${wpm.toFixed(2)} palabras por minuto, Precisión: ${accuracy.toFixed(2)}%`;
                    document.getElementById('entrada-usuario').disabled = true;
                } else {
                    resultadoDiv.className = "resultado incorrecto";
                    resultadoDiv.innerText = "Incorrecto. Intenta de nuevo.";
                }
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_BASE)

@app.route('/obtener-frase')
def obtener_frase():
    return jsonify({"frase": random.choice(PHRASES)})

if __name__ == '__main__':
    app.run(debug=True)