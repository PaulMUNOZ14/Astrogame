import pygame as py
import time
from random import randint
from Complémentaires import *
from menu_fin_partie import game_over

#---------------------------#
# Déclaration des variables #
#---------------------------#

def initialisation():
    global font, Play, continuer, change, begin, end
    global difficulty, dt, cooldown, timer, speed, nb, player_speed, mémoireOBJ, mémoirePOS_X, mémoirePOS_Y
    global playerX, playerY, player_dimension, player_model, météor_model, background, tableau_score
    '''
    Sorties : font             (py.font.Font) : Police des textes
              Play             (bool)         : Etat de la boucle de jeu
              continuer        (bool)         : Etat de la mise en pause du jeu
              change           (bool)         : Etat du passage entre les difficultés
              begin            (int)          : Ligne gauche de la zone de jeu
              end              (int)          : Ligne droite de la zone de jeu
              difficulty       (str)          : Difficulté de base
              dt               (int)          : Fréquence d'images par seconde, donne la fluidité du jeu
              cooldown         (int)          : Interval de temps entre chaque météorite
              timer            (int)          : Compteur de temps pour atteindre cooldown
              speed            (int)          : Vitesse des météorites
              nb               (int)          : Nombre de météorites, permet leur indexage
              player_speed     (int)          : Vitesse du joueur
              mémoireOBJ       (dict)         : Mémoire des météorites présentes
              mémoirePOS_X     (dict)         : Mémoire des position en x des météorites
              mémoirePOS_Y     (dict)         : Mémoire des position en y des météorites
              playerX          (float)        : Position en x du joueur
              playerY          (float)        : Position en Y du joueur
              player_dimension (Rect)         : Dimensions du joueur
              player_model     (Surface)      : Représentation visuelle du joueur
              météor_model     (Surface)      : Représentation visuelle des météorites
              background       (Surface)      : Image de fond du jeu
              tableau_score    (str)          : Lien du fichier CSV de classement

    Initialise ou réinitialise tout les dictionnaires et variables utilisés par le jeu
    '''

    font = py.font.Font(None, 36)   # initialisation système

    Play = True             #|
    continuer = True        #| initialisation des variables d'état
    change = False          #|

    difficulty = 'easy' #|
    dt = 0              #|
    cooldown = 20       #|
    timer = 0           #| initialisation des variables par défaut
    speed = 4           #|
    nb = 0              #|
    player_speed = 400  #|

    mémoireOBJ = {}     #|
    mémoirePOS_X = {}   #| initialisation des dictionnaires
    mémoirePOS_Y = {}   #|

    player_img = "player_img_fixe.png"                          #|
    bg_img = "fond_jeu.jpg"                                     #| liens des différents fichiers à importer
    météor_img = "météor.png"                                   #|

    playerX = screen_size[0] // 2                                                       #|
    playerY = screen_size[1] // 22 * 17                                                 #|
    player_dimension = py.Rect(playerX, playerY, 80, 100)                               #| dimensions et image du joueur
    player_model = py.image.load(os.path.join(DATA_DIR, player_img)).convert_alpha()    #|
    player_model = py.transform.scale(player_model, (80, 100))                          #|

    météor_model = py.image.load(os.path.join(DATA_DIR, météor_img)).convert_alpha()    #| dimensions et image
    météor_model = py.transform.scale(météor_model, (100, 200))                         #| des météorites

    background = py.image.load(os.path.join(DATA_DIR, bg_img)).convert_alpha()  # importation de l'image de fond du jeu
    background = resize(background)

    begin = center(background)[0]
    end = begin + background.get_width()

#--------------------------#
# Définition des fonctions #
#--------------------------#

def flou(left, top, w, h, color, opac):
    '''
    Entrées : left  (int) : Position en x de la surface
              top   (int) : Position en y de la surface
              w     (int) : Largeur de la surface
              h     (int) : Hauteur de la surface
              color (str) : Couleur de la surface
              opac  (int) : Niveau de transparence

    Applique un effet de flou sur l'arrière plan (la partie) lorsque le jeu se met en pause
    '''

    fond = py.Surface((w, h))   # création de la surface floue
    fond.fill(color)
    fond.set_alpha(opac) # modification de la transparence            
    screen.blit(fond, py.rect.Rect(left, top, w, h))   # affichage de la surface floue

def continu():
    global continuer
    '''
    Entrées : continuer (bool) : Etat de la mise en pause du jeu, toujours False
    
    Sorties : continuer (bool) : Etat de la mise en pause du jeu, toujours True

    Applique le retour au jeu grâce au bouton Continuer
    '''

    continuer = True    # change l'état de la pause

def météor():
    global nb, mémoireOBJ, mémoirePOS_X, mémoirePOS_Y, player_dimension, timer, cooldown, speed, météor_model, Play
    '''
    Entrées : nb               (int)     : Nombre de météorites. Permet leur indexage
              mémoireOBJ       (dict)    : Mémoire des météorites présentes
              mémoirePOS_X     (dict)    : Mémoire des position en x des météorites
              mémoirePOS_Y     (dict)    : Mémoire des position en y des météorites
              player_dimension (Rect)    : Dimensions du joueur
              timer            (int)     : Compteur de temps pour atteindre cooldown
              cooldown         (int)     : Interval de temps entre chaque météorite
              speed            (int)     : Vitesse des météorites
              météor_model     (Surface) : Représentation visuelle des météorites
              Play             (bool)    : Etat de la boucle de jeu

    Sorties : Play             (bool)    : Etat de la boucle de jeu

    Crée une nouvelle météorite, la rentre dans les mémoires avec une position en x aléatoire de sur l'écran,
    puis les fait descendre, et supprime les météorites qui ont dépassé la position y du joueur et qui ne peuvent être touchées
    '''
    
    if timer <= 0:  # condition d'interval de temps
        nb += 1                                                             #|
        name = str(nb)                                                      #|
        mémoirePOS_X[name] = randint(begin, end - 80)                       #| création et mémorisation
        mémoirePOS_Y[name] = -50                                            #| de la nouvelle météorite
        météorite = py.Rect(mémoirePOS_X[name], mémoirePOS_Y[name], 50, 50) #|
        mémoireOBJ[name] = py.draw.rect(screen, 'red', météorite)           #|
        timer = cooldown    # réinitialisation du timer

    suppr = []  # réinitialisation de la liste des météorites à supprimer
    if mémoireOBJ != {}:    # sécutité lorsque la mémoire est vide
        for obj in mémoireOBJ:                                                      #|
            if mémoirePOS_Y[obj] < playerY + 40:                                    #|
                mémoirePOS_Y[obj] = mémoirePOS_Y[obj] + speed                       #| descente des météorites
                météorite = py.Rect(mémoirePOS_X[obj], mémoirePOS_Y[obj], 80, 80)   #|
                mémoireOBJ[obj] = py.draw.rect(screen, 'red', météorite)            #|
                
                if player_dimension.colliderect(météorite): #|
                    Play = False                            #| collision du joueur avec une météorite, met fin à la partie
                    game_over()                             #|
            
            else:                       #| gère les météorites 
                suppr = suppr + [obj]   #| à supprimer

    for obj in suppr:           #|
        del mémoireOBJ[obj]     #| supprime les météorites (existance, 
        del mémoirePOS_X[obj]   #| positions x et y) des mémoires
        del mémoirePOS_Y[obj]   #|

def normal():
    global cooldown, speed, timer, change, mémoireOBJ, difficulty, normal_text
    '''
    Entrées : difficulty  (str)  : Difficulté du jeu
              mémoireOBJ  (dict) : Mémoire des météorites présentes
        
    Sorties : cooldown    (int)  : Interval de temps entre chaque météorite
              speed       (int)  : Vitesse des météorites
              timer       (int)  : Compteur de temps pour atteindre cooldown
              difficulty  (str)  : Difficulté du jeu
              change      (bool) : Etat du passage entre les difficultés
              normal_text (str)  : Texte de difficulté à afficher

    Laisse tomber tomber les météorites pour passer à la difficulté suivante, change le texte, et le cooldown et speed des météorites
    '''

    if difficulty == 'easy':    # condition de passage des difficultés dans le bon ordre
        change = True   # mise en pause de la création de nouvelles météorites
        if mémoireOBJ == {}:        #|
            cooldown = 15           #|
            speed = 6               #| changement de la difficulté
            timer = 0               #|
            difficulty = 'normal'   #|
            change = False  # continue la création de nouvelles météorites
    normal_text = font.render("NORMAL", True, '#FFFF05')    # texte de difficulté à afficher

def hard():
    global cooldown, speed, timer, change, mémoireOBJ, difficulty, hard_text
    '''
    Entrées : difficulty (str)  : Difficulté du jeu
              mémoireOBJ (dict) : Mémoire des météorites présentes
        
    Sorties : cooldown   (int)  : Interval de temps entre chaque météorite
              speed      (int)  : Vitesse des météorites
              timer      (int)  : Compteur de temps pour atteindre cooldown
              difficulty (str)  : Difficulté du jeu
              change     (bool) : Etat du passage entre les difficultés
              hard_text  (str)  : Texte de difficulté à afficher

    Laisse tomber tomber les météorites pour passer à la difficulté suivante, change le texte, et le cooldown et speed des météorites
    '''

    if difficulty == 'normal':  # condition de passage des difficultés dans le bon ordre
        change = True   # mise en pause de la création de nouvelles météorites
        if mémoireOBJ == {}:    #|
            cooldown = 8        #|
            speed = 8           #| changement de la difficulté
            timer = 0           #|
            difficulty = 'hard' #|
            change = False  # continue la création de nouvelles météorites
    hard_text = font.render("HARD", True, '#FF6E00')    # texte de difficulté à afficher

def very_hard():
    global cooldown, speed, timer, change, mémoireOBJ, difficulty, very_hard_text
    '''
    Entrées : difficulty (str)  : Difficulté du jeu
              mémoireOBJ (dict) : Mémoire des météorites présentes
        
    Sorties : cooldown       (int)  : Interval de temps entre chaque météorite
              speed          (int)  : Vitesse des météorites
              timer          (int)  : Compteur de temps pour atteindre cooldown
              difficulty     (str)  : Difficulté du jeu
              change         (bool) : Etat du passage entre les difficultés
              very_hard_text (str)  : Texte de difficulté à afficher

    Laisse tomber tomber les météorites pour passer à la difficulté suivante, change le texte, et le cooldown et speed des météorites
    '''

    if difficulty == 'hard':    # condition de passage des difficultés dans le bon ordre
        change = True   # mise en pause de la création de nouvelles météorites
        if mémoireOBJ == {}:            #|
            cooldown = 4                #|
            speed = 8                   #| changement de la difficulté
            timer = 0                   #|
            difficulty = 'very hard'    #|
            change = False  # continue la création de nouvelles météorites
    very_hard_text = font.render("VERY HARD", True, '#B80F0A')  # texte de difficulté à afficher

def game_loop():
    global Play, background, player, playerX, playerY, continuer, timer, player_dimension, timer_text, elapsed_time
    """
    Entrées : Play             (bool)       : Etat de la boucle de jeu
              background       (py.Surface) : Image de fond du jeu
              player           (py.Rect)    : Zone de colision du joueur
              playerX          (int)        : Position en x du joueur
              playerY          (int)        : Position en y du joueur
              continuer        (bool)       : Etat de la mise en pause du jeu
              timer            (int)        : Compteur de temps pour atteindre cooldown
              player_dimension (py.Rect)    : Dimensions du joueur
              timer_text       (Py.Surface) : Zone de texte du compteur
              elapsed_time     (int)        : Temps ecoule depuis le debut de la partie

    Sorties : playerY          (int)        : Position en y du joueur
              continuer        (bool)       : Etat de la mise en pause du jeu
              timer            (int)        : Compteur de temps pour atteindre cooldown
              player_dimension (py.Rect)    : Dimensions du joueur

    Gère le jeu
    """

    initialisation()    #| initialisation
    start = time.time() #| du jeu

    py.mixer.music.stop()                                           #|
    py.mixer.music.load(os.path.join(DATA_DIR, "ingame.mp3"))   #| changement de musique
    py.mixer.music.play(-1)                                         #|

    while Play:
        for event in py.event.get():    #|
            if event.type == py.QUIT:   #| événement pour arrêter le programme
                exit                    #|
            elif event.type == py.KEYDOWN:                                          #|
                if event.key == py.K_ESCAPE:                                        #|
                    if continuer == True:                                           #|
                        continuer = False                                           #| mise en pause ou
                        py.mouse.set_pos(screen_size[0] // 2, screen_size[1] // 2)  #| retour au jeu
                    else:                                                           #|
                        continuer = True                                            #|
                        start = time.time() - elapsed_time                          #|
                        
        screen.fill('black')                                            #|
        playerY = screen_size[1] - 180                                  #| ajustements à définir en boucle
        player_dimension = py.Rect(playerX - 35, playerY - 45, 70, 90)  #|

        if not(continuer):  # si pause
            from main import main_menu
            py.mixer.music.pause()  # musique mise en pause
            py.mouse.set_visible(True)  # apparition de la souris
            screen.blit(background, center(background))                                         #|
            screen.blit(player_model, (player.x, player.y))                                     #|
            for obj in mémoireOBJ:                                                              #| tout les objets se trouvent figés en arrière plan
                screen.blit(météor_model, (mémoirePOS_X[obj] - 11, mémoirePOS_Y[obj] - 105))    #|
            screen.blit(timer_text, (center(background)[0] + 10, 10))                           #|

            flou(0, 0, screen_size[0], screen_size[1], 'white', 128)  # application de l'effet de flou
            bouton('Continuer', 50, 'darkgrey', 'lightgrey', screen_size[0] / 2 - 300, screen_size[1] / 2 - 110, 600, 100, continu) #| création 
            bouton('Quitter', 50, 'darkgrey', 'lightgrey', screen_size[0] / 2 - 300, screen_size[1] / 2 + 10, 600, 100, main_menu)  #| des boutons

        else:
            py.mixer.music.unpause()    # musique continuant de tourner
            keys = py.key.get_pressed()                                                 #|
            if keys[py.K_LEFT] and player_dimension.x > begin:                          #|
                playerX -= player_speed * dt                                            #| mouvements gauche et droite du joueur
            if keys[py.K_RIGHT] and player_dimension.x + player_dimension.width < end:  #|
                playerX += player_speed * dt                                            #|

            if Play:    # sécurité anti-crash 
                météor()    # création de nouvelles météorites
            if change == False: #|
                timer -= 1      #| sécurité : change le sens du timer
            else:               #| lorsque la difficulté change
                timer += 1      #|

            elapsed_time = int(time.time() - start)                                                     #|
            minutes = elapsed_time // 60                                                                #| calcul du
            seconds = elapsed_time % 60                                                                 #| temps de jeu
            timer_text = font.render("{:02d}:{:02d}".format(minutes, seconds), True, (255, 255, 255))   #|

            player = py.draw.rect(screen, 'black', player_dimension)   # hitbox du joueur

            screen.blit(background, center(background))                                         #|
            screen.blit(player_model, (player.x, player.y))                                     #|
            for obj in mémoireOBJ:                                                              #| affichage des différents éléments
                screen.blit(météor_model, (mémoirePOS_X[obj] - 11, mémoirePOS_Y[obj] - 105))    #|
            screen.blit(timer_text, (center(background)[0] + 10, 10))                           #|
            py.mouse.set_visible(False) # disparition de la souris

        if (minutes >= 3 and seconds >= 29) or minutes >= 4:                                                #|
            very_hard()                                                                                     #|
            screen.blit(very_hard_text, (center(background)[0] + 10, 40))                                   #|
                                                                                                            #|
        elif (2 <= minutes <= 3 and seconds >=2) or (minutes >= 3 and seconds <= 29):                       #|
            hard()                                                                                          #|
            screen.blit(hard_text, (center(background)[0] + 10, 40))                                        #|
                                                                                                            #| choix de la difficulté selon le temps
        elif (1 <= minutes < 2) or (2 <= minutes <= 3 and seconds <=2) or (seconds >= 59 and minutes < 1):  #|
            normal()                                                                                        #|
            screen.blit(normal_text, (center(background)[0] + 10, 40))                                      #|
                                                                                                            #|
        else:                                                                                               #|
            easy_text = font.render("EASY", True, '#219F1D')                                              #|
            screen.blit(easy_text, (center(background)[0] + 10, 40))                                        #|

        py.display.flip()   # mise à jour de l'affichage
        dt = clock.tick(120) / 1000 # mise à jour de la fluidité