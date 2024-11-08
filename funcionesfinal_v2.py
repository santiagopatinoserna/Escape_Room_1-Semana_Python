"""
Escape Room Game Engine V2
-------------------------
Motor de juego mejorado con características modernas y visualización avanzada.
"""

import time
import os
import sys
from typing import Dict, List, Optional, Set, Any
import random
from datetime import datetime
from colorama import init, Fore, Back, Style

# Inicializar colorama para colores en la terminal
init(autoreset=True)

class GameColors:
    """Colores para diferentes elementos del juego"""
    TITLE = Fore.CYAN + Style.BRIGHT
    ROOM = Fore.GREEN + Style.BRIGHT
    ITEM = Fore.YELLOW
    KEY = Fore.MAGENTA + Style.BRIGHT
    DOOR = Fore.BLUE + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    HINT = Fore.CYAN
    RESET = Style.RESET_ALL
    TREASURE = Fore.YELLOW + Style.BRIGHT
    PROGRESS = Fore.WHITE + Style.BRIGHT
    ACHIEVEMENT = Fore.MAGENTA
    INVENTORY = Fore.BLUE
    SCORE = Fore.GREEN + Style.BRIGHT

class GameArt:
    """Arte ASCII para diferentes elementos del juego"""
    LOGO = f"""{GameColors.TITLE}
    ╔═══════════════════════════════════════╗
    ║     ESCAPE ROOM - AVENTURA FINAL      ║
    ╚═══════════════════════════════════════╝{GameColors.RESET}
    """
    
    GAME_OVER = f"""{GameColors.ERROR}
    ╔═══════════════════════════════════════╗
    ║            FIN DEL JUEGO              ║
    ╚═══════════════════════════════════════╝{GameColors.RESET}
    """
    
    VICTORY = f"""{GameColors.SUCCESS}
    ╔═══════════════════════════════════════╗
    ║         ¡FELICITACIONES!              ║
    ║         HAS ESCAPADO CON ÉXITO        ║
    ╚═══════════════════════════════════════╝{GameColors.RESET}
    """
    
    TREASURE = f"""{GameColors.TREASURE}
    💎 ¡Has encontrado un tesoro! 💎{GameColors.RESET}
    """
    
    ACHIEVEMENT = f"""{GameColors.ACHIEVEMENT}
    🏆 ¡Logro Desbloqueado! 🏆{GameColors.RESET}
    """
    
    SAVE = f"""{GameColors.SUCCESS}
    💾 ¡Partida Guardada! 💾{GameColors.RESET}
    """
    
    LOAD = f"""{GameColors.SUCCESS}
    📂 ¡Partida Cargada! 📂{GameColors.RESET}
    """

class GameSounds:
    """Efectos de sonido del juego usando caracteres ASCII"""
    @staticmethod
    def play_key_found():
        print('\a')  # Bell sound
        time.sleep(0.1)
    
    @staticmethod
    def play_door_open():
        print('\a')
        time.sleep(0.1)
        print('\a')
    
    @staticmethod
    def play_treasure_found():
        for _ in range(3):
            print('\a')
            time.sleep(0.1)
    
    @staticmethod
    def play_achievement():
        for _ in range(2):
            print('\a')
            time.sleep(0.2)

def clear_screen():
    """Limpiar la pantalla de la terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_elapsed_time(start_time: float) -> str:
    """Obtener el tiempo transcurrido en formato legible"""
    elapsed = int(time.time() - start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    return f"{minutes:02d}:{seconds:02d}"

def calculate_score(game_state: Dict[str, Any]) -> int:
    """Calcular la puntuación actual del juego"""
    score = 0
    
    # Puntos por tiempo restante
    time_elapsed = time.time() - game_state["start_time"]
    time_remaining = max(0, game_state["time_limit"] - time_elapsed)
    score += int((time_remaining / 60) * 100)  # 100 puntos por minuto restante
    
    # Puntos por tesoros
    score += sum(treasure.get("value", 0) for treasure in game_state["treasure_collected"])
    
    # Puntos por logros
    score += sum(1000 for achievement in game_state["achievements"].values() if achievement["unlocked"])
    
    # Multiplicador por dificultad
    multiplier = {
        "easy": 0.5,
        "normal": 1.0,
        "hard": 2.0
    }.get(game_state["difficulty"], 1.0)
    
    return int(score * multiplier)

def check_achievements(game_state: Dict[str, Any]) -> None:
    """Verificar y actualizar logros"""
    achievements = game_state["achievements"]
    
    # Speed Runner
    if not achievements["speed_runner"]["unlocked"]:
        time_elapsed = time.time() - game_state["start_time"]
        if time_elapsed < 900:  # 15 minutos
            achievements["speed_runner"]["unlocked"] = True
            print(GameArt.ACHIEVEMENT)
            print(f"¡Logro desbloqueado: {achievements['speed_runner']['name']}!")
            GameSounds.play_achievement()
    
    # Treasure Hunter
    if not achievements["treasure_hunter"]["unlocked"]:
        if len(game_state["treasure_collected"]) >= 3:  # todos los tesoros
            achievements["treasure_hunter"]["unlocked"] = True
            print(GameArt.ACHIEVEMENT)
            print(f"¡Logro desbloqueado: {achievements['treasure_hunter']['name']}!")
            GameSounds.play_achievement()
    
    # Master Explorer
    if not achievements["master_explorer"]["unlocked"]:
        if len(game_state["examined_objects"]) >= 15:  # número arbitrario de objetos
            achievements["master_explorer"]["unlocked"] = True
            print(GameArt.ACHIEVEMENT)
            print(f"¡Logro desbloqueado: {achievements['master_explorer']['name']}!")
            GameSounds.play_achievement()

def print_map(game_state: Dict[str, Any], object_relations: Dict[str, List]) -> None:
    """Mostrar un mapa ASCII del juego con la posición actual"""
    rooms_layout = {
        "game_room":     (0, 0),
        "bedroom1":      (0, 1),
        "bedroom2":      (0, 2),
        "livingroom":    (1, 1),
        "outside":       (2, 1)
    }
    
    map_width = 40
    map_height = 7
    current_room = game_state["current_room"]["name"]
    
    print(f"\n{GameColors.TITLE}═══ MAPA DEL JUEGO ═══{GameColors.RESET}")
    print("╔" + "═" * (map_width-2) + "╗")
    
    for y in range(map_height):
        print("║", end="")
        for x in range(map_width-2):
            room_found = False
            for room, pos in rooms_layout.items():
                if pos == (x//8, y//2):
                    if room == current_room:
                        print(f"{GameColors.PLAYER}P{GameColors.RESET}", end="")
                    else:
                        print(f"{GameColors.ROOM}□{GameColors.RESET}", end="")
                    room_found = True
                    break
            if not room_found:
                if x % 8 == 7:
                    print("│", end="")
                elif y % 2 == 1:
                    print("─", end="")
                else:
                    print(" ", end="")
        print("║")
    
    print("╚" + "═" * (map_width-2) + "╝")

def print_status(game_state: Dict[str, Any]) -> None:
    """Mostrar el estado actual del juego"""
    print(f"\n{GameColors.PROGRESS}═══ ESTADO ACTUAL ═══{GameColors.RESET}")
    print(f"{GameColors.ROOM}Habitación Actual: {game_state['current_room']['name']}{GameColors.RESET}")
    
    # Tiempo y puntuación
    elapsed_time = get_elapsed_time(game_state["start_time"])
    score = calculate_score(game_state)
    print(f"{GameColors.PROGRESS}Tiempo: {elapsed_time}{GameColors.RESET}")
    print(f"{GameColors.SCORE}Puntuación: {score}{GameColors.RESET}")
    
    # Inventario
    if game_state["inventory"]:
        print(f"{GameColors.INVENTORY}Inventario: {', '.join(item['name'] for item in game_state['inventory'])}{GameColors.RESET}")
    else:
        print(f"{GameColors.INVENTORY}Inventario: Vacío{GameColors.RESET}")
    
    # Llaves
    if game_state["keys_collected"]:
        print(f"{GameColors.KEY}Llaves: {', '.join(k['name'] for k in game_state['keys_collected'])}{GameColors.RESET}")
    else:
        print(f"{GameColors.KEY}Llaves: Ninguna{GameColors.RESET}")
    
    # Tesoros
    if game_state["treasure_collected"]:
        print(f"{GameColors.TREASURE}Tesoros: {', '.join(t['name'] for t in game_state['treasure_collected'])}{GameColors.RESET}")
    else:
        print(f"{GameColors.TREASURE}Tesoros: Ninguno{GameColors.RESET}")
    
    # Pistas restantes
    print(f"{GameColors.HINT}Pistas restantes: {game_state['hints_remaining']}{GameColors.RESET}")

def print_inventory(game_state: Dict[str, Any]) -> None:
    """Mostrar el inventario detallado"""
    print(f"\n{GameColors.INVENTORY}═══ INVENTARIO ═══{GameColors.RESET}")
    if not game_state["inventory"]:
        print("El inventario está vacío")
        return
    
    for item in game_state["inventory"]:
        print(f"\n{GameColors.ITEM}{item['name']}{GameColors.RESET}")
        if "description" in item:
            print(f"  {item['description']}")
        if "power" in item:
            print(f"  Poder: {item['power']}")

def print_achievements(game_state: Dict[str, Any]) -> None:
    """Mostrar los logros y su estado"""
    print(f"\n{GameColors.ACHIEVEMENT}═══ LOGROS ═══{GameColors.RESET}")
    for achievement in game_state["achievements"].values():
        status = "✓" if achievement["unlocked"] else "✗"
        color = GameColors.SUCCESS if achievement["unlocked"] else GameColors.ERROR
        print(f"{color}{status} {achievement['name']}: {achievement['description']}{GameColors.RESET}")

def get_hint(game_state: Dict[str, Any], object_relations: Dict[str, List]) -> None:
    """Proporcionar una pista basada en el estado actual del juego"""
    if game_state["hints_remaining"] <= 0:
        print(f"{GameColors.ERROR}No te quedan pistas disponibles.{GameColors.RESET}")
        return
    
    current_room = game_state["current_room"]["name"]
    hints = [
        f"Hay algo interesante en {obj['name']}..." for obj in object_relations[current_room]
    ]
    
    if not game_state["keys_collected"]:
        hints.append("Busca las llaves en los muebles de la habitación.")
    elif len(game_state["treasure_collected"]) < 3:
        hints.append("Aún hay tesoros ocultos por descubrir.")
    
    hint = random.choice(hints)
    game_state["hints_remaining"] -= 1
    print(f"{GameColors.HINT}Pista: {hint}{GameColors.RESET}")
    print(f"Te quedan {game_state['hints_remaining']} pistas.")

def handle_inventory_command(game_state: Dict[str, Any], command: List[str]) -> None:
    """Manejar comandos relacionados con el inventario"""
    if len(command) == 1:
        print_inventory(game_state)
        return
    
    action = command[1]
    if action == "use" and len(command) > 2:
        item_name = " ".join(command[2:])
        use_item(game_state, item_name)
    else:
        print(f"{GameColors.ERROR}Comando de inventario no válido.{GameColors.RESET}")

def use_item(game_state: Dict[str, Any], item_name: str) -> None:
    """Usar un objeto del inventario"""
    for item in game_state["inventory"]:
        if item["name"] == item_name:
            if item["type"] == "key":
                print(f"{GameColors.KEY}Selecciona una puerta para usar la llave.{GameColors.RESET}")
            elif item["type"] == "treasure":
                print(f"{GameColors.TREASURE}Usas el poder de {item['name']}: {item['power']}{GameColors.RESET}")
            return
    print(f"{GameColors.ERROR}No tienes ese objeto en tu inventario.{GameColors.RESET}")

def handle_door(game_state: Dict[str, Any], object_relations: Dict[str, List], door: Dict[str, Any], current_room: Dict[str, Any]) -> None:
    """Manejar interacción con puertas"""
    have_key = any(key["target"] == door for key in game_state["keys_collected"])
    
    if have_key:
        print(f"{GameColors.SUCCESS}¡Tienes la llave! La puerta se abre...{GameColors.RESET}")
        GameSounds.play_door_open()
        next_room = get_next_room_of_door(door, object_relations, current_room)
        if next_room and input(f"{GameColors.HINT}¿Quieres entrar a la siguiente habitación? (si/no): {GameColors.RESET}").strip().lower() == 'si':
            game_state["current_room"] = next_room
            print_map(game_state, object_relations)
    else:
        print(f"{GameColors.ERROR}La puerta está cerrada. {door['mechanism']}{GameColors.RESET}")

def handle_furniture(game_state: Dict[str, Any], object_relations: Dict[str, List], item: Dict[str, Any]) -> None:
    """Manejar interacción con muebles"""
    # Agregar el objeto a los examinados
    game_state["examined_objects"].add(item["name"])
    
    print(f"\n{GameColors.ITEM}{item['description']}{GameColors.RESET}")
    if "interaction" in item:
        print(f"{GameColors.HINT}{item['interaction']}{GameColors.RESET}")
    
    if item["name"] in object_relations and object_relations[item["name"]]:
        found_item = object_relations[item["name"]].pop()
        if found_item["type"] == "key":
            game_state["keys_collected"].append(found_item)
            print(f"{GameColors.SUCCESS}¡Has encontrado {found_item['name']}!{GameColors.RESET}")
            print(f"{GameColors.HINT}{found_item['hint']}{GameColors.RESET}")
            print(f"{GameColors.ITEM}{found_item['story']}{GameColors.RESET}")
            GameSounds.play_key_found()
        elif found_item["type"] == "treasure":
            game_state["treasure_collected"].append(found_item)
            print(GameArt.TREASURE)
            print(f"{GameColors.TREASURE}Has encontrado: {found_item['name']}{GameColors.RESET}")
            print(f"{GameColors.HINT}{found_item['description']}{GameColors.RESET}")
            print(f"{GameColors.ITEM}Poder: {found_item['power']}{GameColors.RESET}")
            GameSounds.play_treasure_found()
        
        game_state["inventory"].append(found_item)
        print_status(game_state)
        check_achievements(game_state)
    else:
        print(f"{GameColors.HINT}No encuentras nada más interesante en este objeto.{GameColors.RESET}")

def push_item(game_state: Dict[str, Any], object_relations: Dict[str, List], item_name: str) -> None:
    """Manejar empuje de objetos"""
    current_room = game_state["current_room"]
    
    for item in object_relations[current_room["name"]]:
        if item["name"] == item_name:
            if item["name"] == "dining table":
                if not any(t["target"] == item for t in game_state["treasure_collected"]):
                    found_treasure = next(t for t in object_relations["dining table"] if t["type"] == "treasure")
                    game_state["treasure_collected"].append(found_treasure)
                    game_state["inventory"].append(found_treasure)
                    print(GameArt.TREASURE)
                    print(f"{GameColors.TREASURE}Has encontrado: {found_treasure['name']}{GameColors.RESET}")
                    print(f"{GameColors.HINT}{found_treasure['description']}{GameColors.RESET}")
                    print(f"{GameColors.ITEM}Poder: {found_treasure['power']}{GameColors.RESET}")
                    GameSounds.play_treasure_found()
                    check_achievements(game_state)
                else:
                    print(f"{GameColors.HINT}Ya encontraste el tesoro aquí.{GameColors.RESET}")
            else:
                print(f"{GameColors.HINT}Nada sucede al empujar este objeto.{GameColors.RESET}")
            return
    
    print(f"{GameColors.ERROR}No encuentras ese objeto en esta habitación.{GameColors.RESET}")

def get_next_room_of_door(door: Dict[str, Any], object_relations: Dict[str, List], current_room: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Obtener la siguiente habitación a través de una puerta"""
    for room in object_relations[door["name"]]:
        if room != current_room:
            return room
    return None

def victory_sequence(game_state: Dict[str, Any]) -> None:
    """Mostrar secuencia de victoria"""
    clear_screen()
    print(GameArt.VICTORY)
    
    # Mostrar resumen final
    print(f"\n{GameColors.TITLE}═══ RESUMEN FINAL ═══{GameColors.RESET}")
    
    # Tiempo total
    elapsed_time = get_elapsed_time(game_state["start_time"])
    print(f"\n{GameColors.PROGRESS}Tiempo total: {elapsed_time}{GameColors.RESET}")
    
    # Puntuación final
    final_score = calculate_score(game_state)
    print(f"{GameColors.SCORE}Puntuación final: {final_score}{GameColors.RESET}")
    
    # Tesoros encontrados
    print(f"\n{GameColors.TREASURE}Tesoros encontrados: {len(game_state['treasure_collected'])}/3{GameColors.RESET}")
    for treasure in game_state["treasure_collected"]:
        print(f"  - {treasure['name']}: {treasure['power']}")
    
    # Logros desbloqueados
    print(f"\n{GameColors.ACHIEVEMENT}Logros desbloqueados:{GameColors.RESET}")
    for achievement in game_state["achievements"].values():
        if achievement["unlocked"]:
            print(f"  ✓ {achievement['name']}")
    
    print(f"\n{GameColors.HINT}¡Gracias por jugar!{GameColors.RESET}")

def start_game(game_state: Dict[str, Any], object_relations: Dict[str, List]) -> None:
    """Iniciar el juego"""
    clear_screen()
    print(GameArt.LOGO)
    
    print(f"{GameColors.HINT}Despiertas en una mansión misteriosa, rodeado de enigmas y secretos.")
    print("No recuerdas cómo llegaste aquí, pero sientes que cada objeto guarda una historia.")
    print(f"Tu misión es escapar, pero ten cuidado: el tiempo corre en tu contra...{GameColors.RESET}\n")
    
    print_help()
    play_room(game_state, game_state["current_room"], object_relations)

def print_help() -> None:
    """Mostrar ayuda del juego"""
    print(f"\n{GameColors.TITLE}═══ COMANDOS DISPONIBLES ═══{GameColors.RESET}")
    print(f"{GameColors.HINT}explore{GameColors.RESET}: Explorar la habitación actual")
    print(f"{GameColors.HINT}examine <objeto>{GameColors.RESET}: Examinar un objeto específico")
    print(f"{GameColors.HINT}push <objeto>{GameColors.RESET}: Empujar un objeto")
    print(f"{GameColors.HINT}take <objeto>{GameColors.RESET}: Tomar un objeto")
    print(f"{GameColors.HINT}inventory{GameColors.RESET}: Ver inventario")
    print(f"{GameColors.HINT}use <objeto>{GameColors.RESET}: Usar un objeto del inventario")
    print(f"{GameColors.HINT}map{GameColors.RESET}: Mostrar el mapa")
    print(f"{GameColors.HINT}status{GameColors.RESET}: Mostrar estado actual")
    print(f"{GameColors.HINT}hint{GameColors.RESET}: Obtener una pista (limitado)")
    print(f"{GameColors.HINT}achievements{GameColors.RESET}: Ver logros")
    print(f"{GameColors.HINT}save{GameColors.RESET}: Guardar partida")
    print(f"{GameColors.HINT}load{GameColors.RESET}: Cargar partida")
    print(f"{GameColors.HINT}help{GameColors.RESET}: Mostrar esta ayuda")
    print(f"{GameColors.HINT}quit{GameColors.RESET}: Salir del juego")

def play_room(game_state: Dict[str, Any], room: Dict[str, Any], object_relations: Dict[str, List]) -> None:
    """Jugar en una habitación"""
    game_state["current_room"] = room
    
    while True:
        # Verificar tiempo límite
        if time.time() - game_state["start_time"] > game_state["time_limit"]:
            print(f"{GameColors.ERROR}¡Se ha agotado el tiempo! Game Over.{GameColors.RESET}")
            print(GameArt.GAME_OVER)
            return
        
        print(f"\n{GameColors.ROOM}Estás en: {room['name']}{GameColors.RESET}")
        command = input(f"{GameColors.HINT}¿Qué quieres hacer? {GameColors.RESET}").strip().lower().split()
        
        if not command:
            continue
            
        action = command[0]
        
        if action == "quit":
            if input("¿Seguro que quieres salir? (si/no): ").lower() == "si":
                print(GameArt.GAME_OVER)
                return
        elif action == "help":
            print_help()
        elif action == "map":
            print_map(game_state, object_relations)
        elif action == "status":
            print_status(game_state)
        elif action == "explore":
            explore_room(object_relations, room)
        elif action == "examine" and len(command) > 1:
            examine_item(game_state, object_relations, " ".join(command[1:]), room)
        elif action == "push" and len(command) > 1:
            push_item(game_state, object_relations, " ".join(command[1:]))
        elif action == "inventory":
            handle_inventory_command(game_state, command)
        elif action == "hint":
            get_hint(game_state, object_relations)
        elif action == "achievements":
            print_achievements(game_state)
        elif action == "save":
            save_game(game_state)
            print(GameArt.SAVE)
        elif action == "load":
            loaded_state = load_game()
            if loaded_state:
                game_state.update(loaded_state)
                print(GameArt.LOAD)
                print_status(game_state)
        else:
            print(f"{GameColors.ERROR}Comando no válido. Escribe 'help' para ver los comandos disponibles.{GameColors.RESET}")
            
        if game_state["current_room"] == game_state["target_room"]:
            victory_sequence(game_state)
            return

def explore_room(object_relations: Dict[str, List], room: Dict[str, Any]) -> None:
    """Explorar una habitación"""
    items = [i["name"] for i in object_relations[room["name"]]]
    print(f"\n{GameColors.ROOM}Exploras {room['name']}.{GameColors.RESET}")
    print(room["description"])
    print(f"{GameColors.ITEM}Objetos encontrados: {', '.join(items)}{GameColors.RESET}")

def examine_item(game_state: Dict[str, Any], object_relations: Dict[str, List], item_name: str, room: Dict[str, Any]) -> None:
    """Examinar un objeto"""
    current_room = game_state["current_room"]
    
    for item in object_relations[current_room["name"]]:
        if item["name"] == item_name:
            if item["type"] == "door":
                handle_door(game_state, object_relations, item, current_room)
            else:
                handle_furniture(game_state, object_relations, item)
            return
    
    print(f"{GameColors.ERROR}No encuentras ese objeto en esta habitación.{GameColors.RESET}")

def save_game(game_state: Dict[str, Any]) -> None:
    """Guardar el estado actual del juego"""
    save_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "game_state": {k: v for k, v in game_state.items() if isinstance(v, (dict, list, str, int, float, bool))}
    }
    with open('savegame.json', 'w') as f:
        json.dump(save_data, f)
    print(f"{GameColors.SUCCESS}¡Partida guardada exitosamente!{GameColors.RESET}")

def load_game() -> Optional[Dict[str, Any]]:
    """Cargar una partida guardada"""
    try:
        with open('savegame.json', 'r') as f:
            save_data = json.load(f)
        print(f"{GameColors.SUCCESS}¡Partida cargada exitosamente!{GameColors.RESET}")
        return save_data["game_state"]
    except FileNotFoundError:
        print(f"{GameColors.ERROR}No se encontró ninguna partida guardada.{GameColors.RESET}")
        return None
