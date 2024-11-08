import time
import threading
import sys


def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def choose_difficulty():
    """
    Ask the player to choose a difficulty level (easy or hard).
    Return Difficulty
    """
    print("Welcome to the game!\n")
    while True:
        try:
            difficulty = input("Choose your difficulty level: 'easy' or 'hard': \n").strip().lower()
            if difficulty not in ["easy", "hard"]:
                raise ValueError("Invalid choice. Please choose 'easy' or 'hard'.\n")
            return difficulty
        except ValueError as e:
            print(e)


def start_timer(time_limit, game_state):
    """
    Starts a timer with the given time limit (in minutes).
    If the timer runs out, it stops and informs the player.
    """
    start_time = time.time()
    while not game_state.get('game_over', False): 
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            print("\nTime's up! You failed to complete the game in time.\n")
            game_state['time_up'] = True
            return
        time_left = time_limit - int(elapsed_time)
        minutes = time_left // 60
        seconds = time_left % 60
        
        sys.stdout.write(f"\rTime left: {minutes:02}:{seconds:02} minutes")
        sys.stdout.flush()

        time.sleep(1)

def start_game(game_state, object_relations):
    """
    Start the game based on selected difficulty.
    Using parameter game_state and object_relations
    Return game in choosen difficulty
    """
    game_state['game_over'] = False

    difficulty = choose_difficulty()
    
    if difficulty == "easy":
        print("You selected Easy mode. You have to escape and maybe if you are good at researching you can find a reward!\n")
        easy_mode(game_state, object_relations)
    elif difficulty == "hard":
        print("\nYou selected Hard mode. You must to escape and find the treasure within the time limit!\n")
        time_limit = 300  # 5 minutes for hard mode
        game_state['time_up'] = False

        # Create a new thread to start the timer in the background
        timer_thread = threading.Thread(target=start_timer, args=(time_limit, game_state))
        timer_thread.daemon = True  # This allows the thread to exit when the main program exits
        timer_thread.start()
        
        # Start the hard mode game loop
        while not game_state.get('time_up', False) and not game_state.get('game_over', False):
            hard_mode(game_state, object_relations)

    if game_state['game_over']:
        print("\nThanks for playing!\n")
    elif game_state['time_up']:
        print("\nGame over due to time limit.\n")


def easy_mode(game_state, object_relations):
    """
    Play the game in easy mode (maybe you can found a reward).
    Using parameter game_state and object_relations
    """
    print("You wake up on a couch and find yourself in a strange house with no windows\n")
    print("You don't remember why you are here and what had happened before. You have to find a way to go out")
    play_room(game_state, game_state["current_room"], object_relations)
    

def hard_mode(game_state, object_relations):
    """
    Play the game in hard mode (includes a timer and the treasure).
    Using parameter game_state and object_relations
    """
    print("\nYou wake up on a couch and find yourself in a strange house...\n")
    print("\nYou don't remember why you are here and what had happened before. You have to find a way to go out")
    play_room(game_state, game_state["current_room"], object_relations)



def play_room(game_state, room, object_relations):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room), examine or push an item found here.
    """
    game_state["current_room"] = room

    while not game_state.get("game_over", False) and not game_state.get("time_up", False):
        if game_state["current_room"] == game_state["target_room"]:
            print("\nCongrats! You escaped the room!\n")
            game_state["game_over"] = True
            return  # Salir de la función si se completa el juego

        print("\nYou are now in " + room["name"])
        intended_action = input("\nWhat would you like to do? Type 'explore', 'examine' or 'push'?\n").strip().lower()
        
        if intended_action == "explore":
            explore_room(object_relations, room)
        elif intended_action == "examine":
            next_room = examine_item(game_state, object_relations, input("\nWhat would you like to examine?\n").strip().lower(), room)
            if next_room:
                game_state["current_room"] = next_room  # Cambiar a la nueva habitación
        elif intended_action == "push":
            item_to_push = input("\nWhat would you like to push?\n").strip().lower()
            push(game_state, object_relations, item_to_push, room)
        else:
            print("\nNot sure what you mean. Type 'explore', 'examine' or 'push'.\n")
        
        linebreak()



def explore_room(object_relations, room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("\nYou explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, object_relations, current_room):
    next_room = None
    for room in object_relations[door["name"]]:
        if room != current_room:
            next_room = room
            break
    return next_room

def examine_item(game_state, object_relations, item_name, room):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have.\n"
                    next_room = get_next_room_of_door(item, object_relations, current_room)
                else:
                    output += "It is locked but you don't have the key.\n"
            else:
                # Ya no buscamos el tesoro al examinar
                if item["name"] == "dining table":
                    output += "There's nothing interesting about this table.\n"
                else:
                    if(item["name"] in object_relations and len(object_relations[item["name"]]) > 0):
                        item_found = object_relations[item["name"]].pop()
                        game_state["keys_collected"].append(item_found)
                        output += "You find " + item_found["name"] + "."
                    else:
                        output += "There isn't anything interesting about it.\n"
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.\n")

    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'\n").strip() == 'yes'):
        play_room(game_state, next_room, object_relations)
    else:
        play_room(game_state, room, object_relations)


def push(game_state, object_relations, item_name, room):
    """
    Push an item to find the treasure.
    """
    current_room = game_state["current_room"]
    output = None

    for item in object_relations[current_room["name"]]:
        if item["name"] == item_name:
            output = "\nYou push " + item_name + ". "
            if item["name"] == "dining table":
                treasure_collected = False  
                for t in game_state["treasure_collected"]:
                    if t["target"] == item:
                        treasure_collected = True
                        break
                
                if treasure_collected:
                    output += "\nYou have already found the treasure.\n"
                else:
                    output += "\nYou find the treasure!"
                    game_state["treasure_collected"].append({"target": item})  
            else:
                output += "\nThere isn't anything interesting about it.\n"
            
            print(output)
            break
    
    if output is None:
        print("\nThe item you requested is not found in the current room.\n")