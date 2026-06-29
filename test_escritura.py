'''La idea de este proyecto es crear un programa que evalúe cuan rápido puedes escribir una
oración de manera precisa.'''

import tkinter as tk
import random
import timeit

class TypingSpeedTest:

    '''Clase que representa la prueba de velocidad de escritura. Contiene métodos para iniciar la prueba, verificar la entrada del usuario y calcular la velocidad y precisión de escritura.'''

    def __init__(self, master):

        '''Inicializa la ventana principal de la prueba de velocidad de escritura y configura los elementos de la interfaz.'''

        # Configuración de la ventana principal
        self.master = master
        self.master.title("Typing Speed Test")
        self.master.geometry("600x400")

        # Lista de frases para la prueba de escritura
        self.phrases = [
            "El rapido zorro marron salta sobre el perro perezoso.",
            "La lluvia en Sevilla es una maravilla para los ojos.",
            "Python es un lenguaje de programacion versatil y poderoso.",
            "La practica hace al maestro, y la perseverancia es la clave del exito.",
            "El conocimiento es poder, y la educacion es la llave para desbloquearlo."
        ]

        # Variables para almacenar la frase actual y el tiempo de inicio de la prueba
        self.current_phrase = ""
        self.start_time = 0

        # Configuración de los elementos de la interfaz gráfica
        self.label = tk.Label(master, text="Presiona 'Iniciar' para comenzar la prueba de escritura.", font=("Helvetica", 14))
        self.label.pack(pady=10)

        # Botón para iniciar la prueba de escritura
        self.start_button = tk.Button(master, text="Iniciar", command=self.start_test)
        self.start_button.pack(pady=10)

        # Campo de entrada para que el usuario escriba la frase mostrada
        self.entry = tk.Entry(master, width=50, font=("Helvetica", 14))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.check_input)

        # Etiqueta para mostrar los resultados de la prueba de escritura
        self.result_label = tk.Label(master, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=20)

    def start_test(self):

        '''Inicia la prueba de escritura seleccionando una frase aleatoria y comenzando el temporizador.'''

        # Selecciona una frase aleatoria de la lista de frases
        self.current_phrase = random.choice(self.phrases)

        # Actualiza la etiqueta con la frase seleccionada y limpia el campo de entrada
        self.label.config(text=self.current_phrase)

        # Inicia el temporizador para medir la velocidad de escritura
        self.entry.delete(0, tk.END)

        # Almacena el tiempo de inicio de la prueba utilizando timeit
        self.start_time = timeit.default_timer()

    def check_input(self, event):

        '''Verifica la entrada del usuario y calcula la velocidad de escritura y precisión.'''

        # Almacena el tiempo de finalización de la prueba y calcula el tiempo transcurrido
        end_time = timeit.default_timer()

        # Calcula el tiempo transcurrido desde que se inició la prueba
        elapsed_time = end_time - self.start_time

        # Obtiene la entrada del usuario desde el campo de entrada
        user_input = self.entry.get()

        # Compara la entrada del usuario con la frase actual y calcula la velocidad de escritura y precisión
        if user_input == self.current_phrase:
            wpm = (len(user_input.split()) / elapsed_time) * 60
            accuracy = (len(user_input) / len(self.current_phrase)) * 100
            result_text = f"¡Correcto! {wpm:.2f} palabras por minuto, Precisión: {accuracy:.2f}%"
        else:
            result_text = "Incorrecto. Intenta de nuevo."

        # Actualiza la etiqueta de resultados con la información calculada
        self.result_label.config(text=result_text)

# Inicia la aplicación de prueba de velocidad de escritura
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
