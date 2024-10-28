import random

class Game:
    def __init__(self):
        # Personajes
        self.suspects = ['Aldios', 'Iktan', 'Don Chava', 'Ajolotito', 'Bimbo']
        # Armas
        self.weapons = ['Corbata de Pau', 'Martillo de Roberto', 'Cuchillo de Alexis', 'Botella de Mau', 'Libro de control']
        # Ubicaciones
        self.locations = ['Baño', 'Biblioteca', 'Cafetería', 'Salón', 'Gimnasio']

        # Selección aleatoria de la combinación correcta
        self.culprit = random.choice(self.suspects)
        self.weapon = random.choice(self.weapons)
        self.location = random.choice(self.locations)
        self.selected_clues = 0  # Contador de pistas seleccionadas

    def make_guess(self, guess_culprit, guess_weapon, guess_location):
        return guess_culprit == self.culprit and guess_weapon == self.weapon and guess_location == self.location

    def get_remaining_clues(self):
        return 5 - self.selected_clues  # Regresa el número de pistas restantes

    def increment_clue_count(self):
        self.selected_clues += 1  # Aumentar el contador de pistas
