import pygame as py
from Complémentaires import *
from Jeu import flou

#---------------------------#
# Déclaration des variables #
#---------------------------#

credits_image = py.image.load(os.path.join(DATA_DIR, 'fond_2.jpg')).convert()   #| importation et mise à l'échelle
credits_image = resize(credits_image)                                           #| de l'image de fond des options

#--------------------------#
# Définition des fonctions #
#--------------------------#

def show_credits():
    """
    Affiche le menu des crédits
    """

    credits_loop = True                                                 #|
    line_height = 50                                                    #|
    credits_text = [                                                    #|
        "Crédits :",                                                    #|
        "",                                                             #|
        "Paul MUNOZ",                                                   #|
        "Noah LARZILLIÈRE",                                             #| textes et variables du menu de crédits
        "JOAN GUILBERT",                                                #|
        "",                                                             #|
        "Projet NSI 2024 - ASTROGAME",                                  #|
        "Institut Lemonnier Caen"                                       #|
    ]                                                                   #|
    escape_text = "Appuyez sur ECHAP pour retourner au menu principal"  #|

    while credits_loop:
        for event in py.event.get():                                    #|
            if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:   #| événement pour revenir au menu principal
                credits_loop = False                                    #|

        screen.blit(credits_image, center(credits_image))
        flou(screen_size[0] * 2/5, 0, screen_size[0] * 1/5, screen_size[1], 'black', 128)    # application d'un fond flou sous le texte

        for i in range(len(credits_text)):                                                                  #|
            line = credits_text[i]                                                                          #|
            TextSurf, TextRect = text(line, 30, 'white')                                                    #| création et affichage des différents textes
            TextRect.center = (screen_size[0] / 2, screen_size[1] / 2 + i * line_height - 4 * line_height)  #|
            screen.blit(TextSurf, TextRect)                                                                 #|

        escapeSurf, escapeRect = text(escape_text, couleur='white') #|
        escapeRect.topleft = (center(escapeSurf)[0], 10)            #| création et affichage du texte pour quitter le menu
        screen.blit(escapeSurf, escapeRect)                         #|

        py.display.update() #| mise à jour de
        clock.tick(60)      #| l'affichage