import tkinter as tk
from tkinter import messagebox, OptionMenu, StringVar
from PIL import Image, ImageTk
from game_logic import Game
from stories import get_dynamic_character_info, get_weapon_info, get_location_info
import os
import sys

# Función para obtener la ruta correcta del archivo de recursos
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # Si está empaquetado, usa el directorio temporal de PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class ClueGame:
    def __init__(self, root):
        self.root = root
        self.root.title("La venganza de Teoria de control")
        self.root.geometry("600x600")
        self.start_game()

    def load_background(self, canvas, image_path="fondo.png"):
        # Cargar y aplicar la imagen de fondo
        bg_image = Image.open(resource_path(image_path))
        bg_image = bg_image.resize((600, 600), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(bg_image)
        canvas.create_image(0, 0, anchor="nw", image=self.background_image)

    def start_game(self):
        self.game = Game()
        self.create_intro_screen()

    def create_intro_screen(self):
        canvas = tk.Canvas(self.root, width=600, height=600)
        canvas.pack(fill="both", expand=True)
        self.load_background(canvas)

        story = ("Un crimen ha ocurrido durante un evento escolar en CETI Colomos. "
                 "El profesor Víctor ha sido asesinado, y tú debes descubrir quién fue el culpable, "
                 "qué arma se utilizó y dónde ocurrió el crimen.")
        intro_label = tk.Label(canvas, text=story, wraplength=550, bg="white", font=("Arial", 10, "bold"))
        intro_label.pack(pady=10)

        # Botón de inicio
        start_button = tk.Button(canvas, text="Comenzar Investigación", command=self.ask_for_clue_type)
        start_button.pack(pady=10)

        # Botón de reglas
        rules_button = tk.Button(canvas, text="Reglas", command=self.show_rules)
        rules_button.pack(pady=10)

        # Mostrar la imagen de "Victor"
        self.display_victor_image(canvas)

    def show_rules(self):
        # Ventana emergente con las reglas del juego
        rules = (
            "Reglas del Juego:\n\n"
            "1. Tu objetivo es resolver el misterio del crimen en CETI Colomos.\n"
            "2. Selecciona el personaje, arma y ubicación para obtener informacion de cada uno.\n"
            "3. Tienes un número limitado de 5 pistas, úsalas sabiamente.\n"
            "4. Si te equivocas en tu conjetura final, perderás el juego.\n"
            "5. Buena suerte en tu investigación, la necesitaras..."
        )
        messagebox.showinfo("Reglas del Juego", rules)

    def display_victor_image(self, canvas):
        image_path = "Victor.png"
        if os.path.exists(resource_path(image_path)):
            victor_image = Image.open(resource_path(image_path))
            victor_image = victor_image.resize((300, 300), Image.LANCZOS)
            self.victor_image_tk = ImageTk.PhotoImage(victor_image)
            canvas.create_image(300, 450, anchor="center", image=self.victor_image_tk)
        else:
            print("Imagen de Victor no encontrada.")

    def ask_for_clue_type(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.root, width=600, height=600)
        canvas.pack(fill="both", expand=True)
        self.load_background(canvas)

        if self.game.get_remaining_clues() > 0:
            tk.Label(canvas, text="¿Qué tipo de pista quieres obtener?", bg="white", font=("Arial", 10, "bold")).pack(pady=5)
            tk.Button(canvas, text="Personaje", command=self.ask_characters).pack(pady=5)
            tk.Button(canvas, text="Arma", command=self.ask_weapon).pack(pady=5)
            tk.Button(canvas, text="Ubicación", command=self.ask_location).pack(pady=5)
        else:
            self.show_final_guess()

    def ask_characters(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.root, width=600, height=600)
        canvas.pack(fill="both", expand=True)
        self.load_background(canvas)

        tk.Label(canvas, text="Selecciona un personaje para interrogar:", bg="white", font=("Arial", 10, "bold")).pack(pady=5)
        for character in self.game.suspects:
            tk.Button(canvas, text=character, command=lambda c=character: self.show_character_info(c)).pack(pady=5)

        back_button = tk.Button(canvas, text="Regresar", command=self.ask_for_clue_type)
        back_button.pack(pady=10)

    def show_character_info(self, character):
        clues, context = get_dynamic_character_info(self.game.culprit, self.game.weapon, self.game.location, character)
        self.game.increment_clue_count()

        for widget in self.root.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.root, width=600, height=600)
        canvas.pack(fill="both", expand=True)
        self.load_background(canvas)

        self.display_character_image(canvas, character)

        tk.Label(canvas, text=f"Información de {character}:", bg="white", font=("Arial", 10, "bold")).pack(pady=5)
        for clue in clues:
            tk.Label(canvas, text=clue, wraplength=550, bg="white", font=("Arial", 10)).pack(pady=5)

        next_button = tk.Button(canvas, text="Siguiente", command=self.ask_for_clue_type)
        next_button.pack(pady=20)

    def display_character_image(self, canvas, character):
        image_path = f"{character}.png"
        if os.path.exists(resource_path(image_path)):
            character_image = Image.open(resource_path(image_path))
            character_image = character_image.resize((300, 300), Image.LANCZOS)
            self.character_image_tk = ImageTk.PhotoImage(character_image)
            canvas.create_image(300, 500, anchor="center", image=self.character_image_tk)
        else:
            print(f"Imagen para {character} no encontrada.")

    def ask_weapon(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.root, width=600, height=600)
        canvas.pack(fill="both", expand=True)
        self.load_background(canvas)

        tk.Label(canvas, text="Selecciona un arma para investigar:", bg="white", font=("Arial", 10, "bold")).pack(pady=5)
        for weapon in self.game.weapons:
            tk.Button(canvas, text=weapon, command=lambda w=weapon: self.show_weapon_info(w)).pack(pady=5)

        back_button = tk.Button(canvas, text="Regresar", command=self.ask_for_clue_type)
        back_button.pack(pady=10)

    def show_weapon_info(self, weapon):
        clues = get_weapon_info(self.game.culprit, self.game.weapon, weapon)
        self.game.increment_clue_count()

        for widget in self.root.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.root, width=600, height=600)
        canvas.pack(fill="both", expand=True)
        self.load_background(canvas)

        tk.Label(canvas, text=f"Información sobre el arma {weapon}:", bg="white", font=("Arial", 10, "bold")).pack(pady=5)
        for clue in clues:
            tk.Label(canvas, text=clue, wraplength=550, bg="white", font=("Arial", 10)).pack(pady=5)

        next_button = tk.Button(canvas, text="Siguiente", command=self.ask_for_clue_type)
        next_button.pack(pady=20)

    def ask_location(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.root, width=600, height=600)
        canvas.pack(fill="both", expand=True)
        self.load_background(canvas)

        tk.Label(canvas, text="Selecciona una ubicación para investigar:", bg="white", font=("Arial", 10, "bold")).pack(pady=5)
        for location in self.game.locations:
            tk.Button(canvas, text=location, command=lambda l=location: self.show_location_info(l)).pack(pady=5)

        back_button = tk.Button(canvas, text="Regresar", command=self.ask_for_clue_type)
        back_button.pack(pady=10)

    def show_location_info(self, location):
        clues = get_location_info(self.game.culprit, self.game.weapon, self.game.location, location)
        self.game.increment_clue_count()

        for widget in self.root.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.root, width=600, height=600)
        canvas.pack(fill="both", expand=True)
        self.load_background(canvas)

        tk.Label(canvas, text=f"Información sobre la ubicación {location}:", bg="white", font=("Arial", 10, "bold")).pack(pady=5)
        for clue in clues:
            tk.Label(canvas, text=clue, wraplength=550, bg="white", font=("Arial", 10)).pack(pady=5)

        next_button = tk.Button(canvas, text="Siguiente", command=self.ask_for_clue_type)
        next_button.pack(pady=20)

    def show_final_guess(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.root, width=600, height=600)
        canvas.pack(fill="both", expand=True)
        self.load_background(canvas)

        tk.Label(canvas, text="Haz tu conjetura final:", bg="white", font=("Arial", 10, "bold")).pack(pady=5)

        self.culprit_var = StringVar(self.root)
        self.culprit_var.set(self.game.suspects[0])
        tk.Label(canvas, text="¿Quién es el culpable?", bg="white", font=("Arial", 10)).pack(pady=5)
        OptionMenu(canvas, self.culprit_var, *self.game.suspects).pack()

        self.weapon_var = StringVar(self.root)
        self.weapon_var.set(self.game.weapons[0])
        tk.Label(canvas, text="¿Cuál es el arma?", bg="white", font=("Arial", 10)).pack(pady=5)
        OptionMenu(canvas, self.weapon_var, *self.game.weapons).pack()

        self.location_var = StringVar(self.root)
        self.location_var.set(self.game.locations[0])
        tk.Label(canvas, text="¿Dónde ocurrió?", bg="white", font=("Arial", 10)).pack(pady=5)
        OptionMenu(canvas, self.location_var, *self.game.locations).pack()

        submit_button = tk.Button(canvas, text="Enviar conjetura", command=self.check_guess)
        submit_button.pack(pady=20)

    def check_guess(self):
        guess_culprit = self.culprit_var.get()
        guess_weapon = self.weapon_var.get()
        guess_location = self.location_var.get()

        correct = self.game.make_guess(guess_culprit, guess_weapon, guess_location)

        if correct:
            messagebox.showinfo("Felicidades", f"¡Has resuelto el crimen!\n"
                                               f"El culpable era {guess_culprit}, con la {guess_weapon} en el {guess_location}.")
        else:
            messagebox.showerror("Fin del Juego", f"Has fallado.\n"
                                                 f"La respuesta correcta era: {self.game.culprit}, con la {self.game.weapon} en el {self.game.location}.")

        if messagebox.askyesno("Juego terminado", "¿Quieres jugar de nuevo?"):
            self.root.destroy()  
            root = tk.Tk()  
            clue_game = ClueGame(root)  
            root.mainloop()
        else:
            self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    clue_game = ClueGame(root)
    root.mainloop()
