import pygame as py
from Complémentaires import *
from Jeu import game_loop
from menu_options import help_options
from menu_crédits import show_credits

#---------------------------#
# Déclaration des variables #
#---------------------------#

astrogame_back = py.image.load(os.path.join(DATA_DIR, 'fond_3.jpg')).convert()  #| importation et mise à l'échelle
astrogame_back = resize(astrogame_back)                                         #| de l'image de fond du menu

astrogame_title = py.image.load(os.path.join(DATA_DIR, 'ASTROGAME.png')).convert_alpha()    #| importation et 
astrogame_title = resize(astrogame_title, 1200)                                             #| mise à l'échelle
astrogame_title_center = center(astrogame_title)                                            #| du titre du jeu

button_width = 0.4 * screen_size[0]     #|
button_height = 0.12 * screen_size[1]   #| dimensions des boutons et de leur espacement
button_spacing = 0.10 * screen_size[1]  #|

#--------------------------#
# Définition des fonctions #
#--------------------------#

def to_game():
    global menu
    """
    Entrées : menu (bool) : Boucle du menu principal, toujours True
    
    Sorties : menu (bool) : Boucle du menu principal, toujours False

    Met fin au menu principal et renvoi vers la partie jeu
    """
    
    menu = False
    game_loop()

def main_menu(): 
    global menu
    """
    Sorties : menu (bool) : Boucle du menu principal

    Affiche le menu principal du jeu
    """

    py.mouse.set_pos((screen_size[0] // 2), screen_size[1] // 2)    #|
    blocked_time = 5                                                #| sécurité de retour au menu principal
    menu = True                                                     #|

    py.mixer.music.stop()                                           #|
    py.mixer.music.load(os.path.join(DATA_DIR, "background.mp3"))   #| changement de musique
    py.mixer.music.play(-1)                                         #|

    while menu:
        for event in py.event.get():    #|
            if event.type == py.QUIT:   #| événement pour arrêter le programme
                menu = False            #|

        py.mouse.set_visible(True)  # sécurité d'affiche de souris

        screen.fill('black')

        screen.blit(astrogame_back, center(astrogame_back))             #|
        astrogame_title_center[1] = - astrogame_title.get_height() / 4  #| affichage du fond et du titre
        screen.blit(astrogame_title, astrogame_title_center)            #|

        if blocked_time > 0 :   #| sécurité contre
            blocked_time -= 1   #| l'appui prolongé

        if blocked_time <= 0 :
            bouton("Jouer", 50, 'darkgrey', 'lightgrey', screen_size[0] // 2 - button_width // 2, screen_size[1] // 2 - button_height / 2 - 3/2 * button_height, button_width, button_height, to_game)          #|
            bouton("Options & Aide", 50, 'darkgrey', 'lightgrey', screen_size[0] // 2 - button_width // 2, screen_size[1] // 2 - button_height / 2, button_width, button_height, help_options)                  #| création des
            bouton("Crédits", 50, 'darkgrey', 'lightgrey', screen_size[0] // 2 - button_width // 2, screen_size[1] // 2 - button_height / 2 + 3/2 * button_height, button_width, button_height, show_credits)   #| bontons
            bouton("Quitter le jeu", 50, 'darkgrey', 'lightgrey', screen_size[0] // 2 - button_width // 2, screen_size[1] // 2 - button_height / 2 + 3 * button_height, button_width, button_height, exit)      #|

        py.display.update() #| mise à jour
        clock.tick(60)      #| de l'affichage
    
    py.quit()

#------------------------#
# Lancement du programme #
#-------------------- ---#

if __name__ == '__main__':
    main_menu()