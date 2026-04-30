import pygame as py
from Complémentaires import *
from Jeu import flou 

#---------------------------#
# Déclaration des variables #
#---------------------------#

VOLUME_BAR_WIDTH = 400                                          #|
VOLUME_BAR_HEIGHT = 10                                          #| dimensions et positions
VOLUME_BAR_X = (screen_size[0] - VOLUME_BAR_WIDTH) // 2         #| de la barre de son
VOLUME_BAR_Y = (screen_size[1] / 2 - VOLUME_BAR_WIDTH/2) * 1.05 #|

option_image = py.image.load(os.path.join(DATA_DIR, 'fond_1.jpg')).convert()    #| importation et mise à l'échelle
option_image = resize(option_image)                                             #| de l'image de fond des options

#--------------------------#
# Définition des fonctions #
#--------------------------#

def volume_bar(volume_level):
    """
    Entrées : volume_level (float) : Niveau sonore

    Crée et affiche la barre de son remplie selon le niveau sonore
    """

    py.draw.rect(screen, 'gray', (VOLUME_BAR_X, VOLUME_BAR_Y, VOLUME_BAR_WIDTH, VOLUME_BAR_HEIGHT)) # fond de la barre
    volume_bar_fill = int(VOLUME_BAR_WIDTH * volume_level)
    py.draw.rect(screen, (30, 144, 255), (VOLUME_BAR_X, VOLUME_BAR_Y, volume_bar_fill, VOLUME_BAR_HEIGHT))  # niveau sonore

def sound_circle(volume_level):
    """
    Entrées : volume_level (float) : Niveau sonore

    Crée le point de niveau sonore
    """

    circle_x = VOLUME_BAR_X + int(VOLUME_BAR_WIDTH * volume_level)
    circle_y = VOLUME_BAR_Y + VOLUME_BAR_HEIGHT // 2
    py.draw.circle(screen, (30, 144, 255), (circle_x, circle_y), 10)

def help_options(): 
    global volume_level
    """
    Entrées : volume_level (float) : Niveau sonore
    
    Sorties : volume_level (float) : Niveau sonore

    Affiche le menu d'options
    """

    help_loop = True                                                    #|
    mouse_pressed = False                                               #|
    line_height = 45                                                    #|
    help_text = [                                                       #|
        "OPTIONS & AIDES",                                              #|
        "",                                                             #|
        "  MUSIQUE :",                                                  #|
        "",                                                             #|
        "_____________________________________________",                #| textes et variables du
        "",                                                             #| menu d'options et aides
        "  BUT DU JEU :",                                               #|
        "En tant qu’astronaute, il est essentiel de",                   #|
        "faire face aux pluies de météorites.",                         #|
        "Pour y échapper,",                                             #|
        "il faut se déplacer vers la droite ou la gauche.",             #|
        "Les pluies de météorites durent",                              #|
        "très longtemps sur la planète Mars.",                          #|
        "Bonne chance !"                                                #|
    ]                                                                   #|
    escape_text = "Appuyez sur ECHAP pour retourner au menu principal"  #|

    while help_loop:
        for event in py.event.get():                                                                #|
            if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):    #| événement pour revenir au menu principal
                help_loop = False                                                                   #|

            elif event.type == py.MOUSEBUTTONDOWN:                                                                                              #|
                mouse_x, mouse_y = py.mouse.get_pos()                                                                                           #|
                if VOLUME_BAR_X <= mouse_x <= VOLUME_BAR_X + VOLUME_BAR_WIDTH and VOLUME_BAR_Y <= mouse_y <= VOLUME_BAR_Y + VOLUME_BAR_HEIGHT:  #| changement du niveau sonore
                    mouse_pressed = True                                                                                                        #| lorsque le point est sélectionné
            elif event.type == py.MOUSEBUTTONUP:                                                                                                #|
                mouse_pressed = False                                                                                                           #|

        if mouse_pressed:                                                   #|
            mouse_x, mouse_y = py.mouse.get_pos()                           #|
            if mouse_x < VOLUME_BAR_X:                                      #|
                volume_level = 0                                            #| changement du niveau
            elif mouse_x > VOLUME_BAR_X + VOLUME_BAR_WIDTH:                 #| sonore et du remplissage 
                volume_level = 1                                            #| de la barre de son
            else:                                                           #|
                volume_level = (mouse_x - VOLUME_BAR_X) / VOLUME_BAR_WIDTH  #|
            py.mixer.music.set_volume(volume_level)                         #|

        screen.blit(option_image, center(option_image))
        flou(screen_size[0] * 2/5, 0, screen_size[0] * 1/5, screen_size[1], 'black', 128)    # application d'un fond flou sous le texte

        for i in range(len(help_text)):                                                                         #|
                line = help_text[i]                                                                             #|
                TextSurf, TextRect = text(line, 30, 'white')                                                    #| création et affichage des différents textes
                TextRect.center = (screen_size[0] // 2, screen_size[1] / 2 + i * line_height - 7 * line_height) #|
                screen.blit(TextSurf, TextRect)                                                                 #|


        escapeSurf, escapeRect = text(escape_text, couleur='white') #|
        escapeRect.topleft = (center(escapeSurf)[0], 10)            #| création et affichage du texte pour quitter le menu
        screen.blit(escapeSurf, escapeRect)                         #|

        volume_bar(volume_level)    #|
        sound_circle(volume_level)  #| mise à jour de
        py.display.update()         #| l'affichage
        clock.tick(60)              #|