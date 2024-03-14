import random
from collections import deque
from pynput import keyboard
import threading
import time
import os

game_speed = 0.6
columns = 5
rows = 5
board = []
direction = "a"

keys_currently_pressed = {}

currently_direction  = ["\'d\'"]

def on_press(key):
    global keys_currently_pressed
    # print(list(keys_currently_pressed[0]))
    if key not in keys_currently_pressed:
        keys_currently_pressed[key] = time.time()
        teste = str(list(keys_currently_pressed.keys())[0])

        currently_direction[0] = teste
        # print(currently_direction[0],"==",teste,"?")
        # print(currently_direction[0]==teste)


def on_release(key):
    global keys_currently_pressed
    if key in keys_currently_pressed:
        duration = time.time() - keys_currently_pressed[key]
        # print(f"A tecla {key} foi pressionada por {duration:.2f} segundos")
        del keys_currently_pressed[key]




def create_board():
    for I in range(0,len(board)):
        board.pop()
    x_player = 0
    y_player = 0
    for I in range(rows):
        board.append([])
        for II in range(columns):
            board[I].append(".")
    board[x_player][y_player] = "▷"
    for I in range(rows):
        print(board[I])


def play_again():
    continue_playing = input("Continuar jogando?  s/n")
    while continue_playing!="s" and continue_playing!="S" and continue_playing!="N" and continue_playing!="n":
        continue_playing = input("Continuar jogando?  s/n")
    if(continue_playing=="n" or continue_playing=="NS"):
        print("Até logo")
        exit()
    else:
        game(columns, rows)





def create_fruit():
    continuar=1
    while(continuar==1):
        continuar=0
        x_fruit = random.randint(0,columns-1)
        y_fruit = random.randint(0,rows-1)
        if(board[y_fruit][x_fruit]!="."):
            continuar=1
    # print(x_fruit,y_fruit)
    return x_fruit, y_fruit



def game(columns,rows):
    create_board()
    x_player = 0
    y_player = 0
    x_queue = deque([])
    y_queue = deque([])
    lenght = 1
    directions = ["w","W","a","A","s","S","d","D",
                  "\'w\'","\'W\'","\'a\'","\'A\'","\'s\'","\'S\'","\'d\'","\'D\'"]
    x_fruit, y_fruit = create_fruit()

    while True:
        time.sleep(game_speed)
        os.system('clear') or None
        symbol = "▷"
        try:
            direction_aux = direction
        except:
            direction_aux = "d"
            
        try:
            direction = currently_direction[0]
        except:
            direction = direction_aux

        x_aux = x_player
        y_aux = y_player


        if(direction not in directions):
            direction = direction_aux    
        if direction == "\'w\'" or direction == "W":
            y_player-=1
            symbol = "△"
        elif direction == "\'a\'" or direction == "A":
            x_player-=1
            symbol = "◁"
        elif direction == "\'s\'" or direction == "S":
            y_player+=1
            symbol = "▽"
        elif direction == "\'d\'" or direction == "D":
            x_player+=1
            symbol = "▷"

        
            

        if(x_player>=columns):
            x_player=0
        elif(x_player<=-1):
            x_player=columns-1

        if(y_player>=rows):
            y_player=0
        elif(y_player<=-1):
            y_player=rows-1

    

        if (x_fruit==x_player and y_fruit==y_player):
        
            # print("pegou a fruta mano.")
            if(lenght==0):
                lenght+=2
            else:
                lenght+=1
            # print("PEGOU A FRUTA")
            if (lenght<=rows*columns-1):
                x_fruit, y_fruit = create_fruit()
            else:
                print("PARABÉNS VOCÊ VENCEU!")
                symbol="✌"
            

        print("Tamanho:",lenght)
        if(lenght>0):
            x_queue.append(x_aux)
            y_queue.append(y_aux)
            
            if(len(x_queue)==lenght):
                x_queue.popleft()
                y_queue.popleft()

        for I in range(0,rows):
            for II in range(0,columns):
                board[I][II] = "."

        board[y_fruit][x_fruit] = "✤"

        
        for I in range(0,len(x_queue)):
                if(x_queue[I]==x_player and y_queue[I]==y_player):
                    symbol="☠"
                    board[y_player][x_player] = symbol
                    print("\n"*12)
                    print("VOCÊ PERDEU!")
                    print("PONTUAÇÃO FINAL:", lenght)
                    print("   ")
                    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                    play_again()
                    board[y_player][x_player] = symbol
                    return continue_playing
                    
        board[y_player][x_player] = symbol
        if(symbol=="✌"):
            play_again()
            
        for I in range(0,len(x_queue)):
            board[y_queue[I]][x_queue[I]]="o"

        for I in range(0,rows):
            for II in range(0,columns):
                board[I][II]== "." 

        for I in range(rows):
            print ( '[%s]' % ', '.join(map(str, board[I])))

        
            
def ouvir():
    # Inicia o listener para capturar as teclas
    with keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        listener.join()  # Aguarda até que o listener seja encerrado



thread_listener = threading.Thread(target=ouvir)

thread_listener.start()

continue_playing = game(columns, rows)
while continue_playing=="s" or continue_playing=="S":
    continue_playing = game(columns, rows)


