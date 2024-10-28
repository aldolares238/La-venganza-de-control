import random

def get_dynamic_character_info(culprit, correct_weapon, correct_location, character):
    clues = []

    if character == culprit:
        # Pistas claras pero con posible ambigüedad
        clues.append(f"{character} fue visto cerca del {correct_location}.")
        clues.append(f"Algunos testigos vieron a {character} sosteniendo algo parecido al {correct_weapon}, pero no están seguros.")
        clues.append(f"Se escuchó una conversación entre {character} y la víctima cerca del {correct_location}.")
        clues.append(f"{character} estaba muy nervioso cuando fue visto por última vez.")
    else:
        incorrect_locations = [loc for loc in ['Baño', 'Biblioteca', 'Cafetería', 'Salón', 'Gimnasio'] if loc != correct_location]
        wrong_location = random.choice(incorrect_locations)

        # Falsos testimonios y ambigüedad
        if random.choice([True, False]):
            clues.append(f"{character} fue visto en el {wrong_location}, pero su testimonio es confuso.")
            clues.append(f"Alguien mencionó haber visto a {character} cerca de algo que podría ser el {correct_weapon}, pero no están seguros.")
        else:
            clues.append(f"Algunos testigos afirman que {character} estaba en el {wrong_location}, pero otras versiones lo contradicen.")
            clues.append(f"{character} fue visto con algo en las manos, pero no era el {correct_weapon}.")
        
        # Acusaciones indirectas
        if random.choice([True, False]):
            clues.append(f"{character} dice haber visto a {culprit} con el {correct_weapon} cerca del {correct_location}, aunque no está seguro.")
        else:
            clues.append(f"{character} estaba distraído y no vio nada sospechoso en el {wrong_location}.")

    context = "El crimen es un misterio, y algunas versiones son contradictorias."
    return clues, context


# Nueva función para obtener información sobre las armas
def get_weapon_info(culprit, correct_weapon, weapon):
    if weapon == correct_weapon:
        return [
            f"El {weapon} tiene huellas sospechosas.",
            f"Parece que el {weapon} fue usado recientemente.",
            f"El {weapon} estaba fuera de lugar cuando se encontró."
        ]
    else:
        return [
            f"No hay señales de que el {weapon} haya sido usado.",
            f"El {weapon} parece estar intacto.",
            f"Nadie vio el {weapon} cerca de la escena."
        ]


# Nueva función para obtener información sobre las ubicaciones
def get_location_info(culprit, weapon, correct_location, location):
    if location == correct_location:
        return [
            f"El {location} tenía algunas huellas extrañas.",
            f"Se escucharon ruidos en el {location} poco antes del incidente.",
            f"Alguien vio algo sospechoso en el {location} justo antes del crimen."
        ]
    else:
        return [
            f"No parece haber nada fuera de lo normal en el {location}.",
            f"El {location} estaba vacío en el momento del crimen.",
            f"Nadie notó nada sospechoso en el {location}."
        ]
