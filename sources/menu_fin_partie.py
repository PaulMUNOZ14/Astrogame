import pygame as py
import csv
from Complémentaires import *

#--------------------------#
# Definition des fonctions #
#--------------------------#

def lire_score(tableau_score):
    """
    Entrées : tableau_score (str)  : Lien du fichier CSV de classement

    Sorties : Liste         (list) : Liste de dictionnaires contenant les pseudos associés aux scores
    
    Gère la lecture du fichier CSV pour le classement
    """

    Liste = []  # initialisation de la liste
    with open(tableau_score, 'r', encoding = 'utf-8') as file:  #|
        tab = csv.DictReader(file, delimiter = ',')             #| lis le fichier CSV pour en
        for ligne in tab:                                       #| extraire les informations
            Liste.append(dict(ligne))                           #| sous forme de dictionnaires
        file.close()                                            #|
    return Liste

def classement(Liste):
    """
    Entrées : Liste (list) : Liste de dictionnaires contenant les pseudos associés aux scores
    
    Sorties : Liste (list) : Liste de dictionnaires contenant les pseudos associés aux scores

    Classifie les pseudos en fonction des scores
    """

    for i in range(len(Liste)):         #|
        val = int(Liste[i]['Score'])    #| parcours sur chaque dictionnaire
        j = i                           #|
        while j > 0 and int(Liste[j - 1]['Score']) < val:   #| 
            Liste[j], Liste[j - 1] = Liste[j - 1], Liste[j] #| modifie la position des dictionnaires selon les scores
            j = j - 1                                       #|
    return Liste

def transforme_score(Name, Score, Liste, tableau_score):
    global limite
    """
    Entrées : limite        (bool) : Sécurité empêchant l'affectation multiple de l'enregistrement des scores
              Name          (str)  : Pseudo du joueur
              Score         (int)  : Score obtenu par le joueur
              Liste         (list) : Liste de dictionnaires contenant les pseudos associés aux scores
              tableau_score (str)  : Lien du fichier CSV de classement

    Sorties : limite        (bool) : Sécurité empêchant l'affectation multiple de l'enregistrement des scores
    
    Crée un nouveau dictionnaire pseudo;score ou le modifie s'il est déjà présent dans la liste
    """

    recu = False
    Score = str(Score)                                  #|
    if len(Liste) == 0:                                 #| ajoute lorsqu'il n'y a pas de scores enregistrés dans le fichier CSV
        Liste.append({'Pseudo': Name, 'Score': Score})  #|
    else:
        recu = True
        for i in range(len(Liste)): # parcours des dictionnaires
            if Name == Liste[i]['Pseudo']:                  #|
                if int(Liste[i]['Score']) < int(Score) :    #| 
                    Liste[i]['Score'] = Score               #| modifie le score s'il est supérieur à celui déjà enregistré
                recu = False                                #|
                break                                       #|
    if recu:
        Liste.append({'Pseudo': Name, 'Score': Score})  # ajoute un dictionnaire pseudo;score si inexistant
    limite = False  # applique la limite d'enregistrement
    retourne_score(tableau_score, Liste)    # enregistre les modifications

def affiche_classement(Liste):
    """
    Entrées : Liste (list) : Liste de dictionnaires contenant les pseudos associés aux scores

    Affiche les 10 premiers du classement avec leur score
    """

    décalage = 0    # décalage en y de l'affichage entre chaque joueur
    Liste = classement(Liste)   # classifie avec les nouveaux scores
    if len(Liste) >= 10:    #|
        limite = 10         #| limite le nombre de 
    else:                   #| joueurs à afficher à 10
        limite = len(Liste) #|
    for i in range(limite):                                                         #|
        name = Liste[i]['Pseudo']                                                   #|
        score = Liste[i]['Score']                                                   #|
        ClassementSurf, Classement_Rect = text(f'{name} -- {score}', 50, 'black')   #| affiche chaque joueur
        Classement_Rect.x = screen_size[0] // 2 + 360                               #| dans le classement
        Classement_Rect.y = screen_size[1] // 2 - 190 + décalage                    #|
        screen.blit(ClassementSurf, Classement_Rect)                                #|
        décalage += 50                                                              #|

def retourne_score(tableau_score, Liste):
    """
    Entrées : tableau_score (str)  : Lien du fichier CSV de classement
              Liste         (list) : Liste de dictionnaires contenant les pseudos associés aux scores

    Inscrit les dictionnaires pseudo;score dans le fichier CSV
    """
    Liste = classement(Liste)   # classifie les scores par sécurité
    with open(tableau_score, 'w', encoding = 'utf-8') as file:  #|
        file.write('Pseudo,Score\n')                            #|
        for i in range(len(Liste)):                             #|
            Pseudo = Liste[i]['Pseudo']                         #| recrée chaque ligne du fichier CSV avec les nouvelles données
            Score = Liste[i]['Score']                           #|
            file.write(f'{Pseudo},{Score}\n')                   #|
        file.close()                                            #|
        affiche_classement(lire_score(tableau_score))   # affiche le classement une fois le fichier relu

def enter():
    global insert, limite
    """
    Entrées : limite (bool) : Sécurité empêchant l'affectation multiple de l'enregistrement des scores

    Sorties : insert (bool) : Etat de la zone de texte, sélectionnée ou non

    Sert de pont sécurisé pour récupérer le pseudo et sortir de la zone de texte
    """

    if limite:
        insert = False  # sort de la zone de texte
        récup_pseudo()  # récupère le texte entré

def récup_pseudo():
    global texte, tableau_score
    from Jeu import elapsed_time
    """
    Entrées : texte (str): Texte inséré dans la zone de texte par le joueur
              tableau_score (str): Lien du fichier CSV de classement
              elapsed_time (int): Temps de jeu, utilisé comme score

    Récupère le pseudo inséré dans la zone de texte pour l'envoyer à classifier
    """

    condition = False                       #|
    for lettre in texte:                    #|
        if lettre != " " or lettre != " ":  #| vérifie que le pseudo 
            condition = True                #| est bien valide
            break                           #|
    if condition and texte != 'INVALIDE':   #|
        Pseudo = texte                                                                      #|
        texte = ""                                                                          #| envoie le pseudo et le score dans le processus de classification
        transforme_score(Pseudo, elapsed_time, lire_score(tableau_score), tableau_score)    #|
    else:                   #| si le pseudo
        texte = "INVALIDE"  #| est invalide

def game_over():
    global insert, texte, tableau_score, limite
    from Jeu import elapsed_time, player, background, player_model, mémoireOBJ, mémoirePOS_X, mémoirePOS_Y, météor_model, flou, game_loop
    from main import main_menu, button_height, button_spacing, button_width
    """
    Entrées : elapsed_time   (int)        : Temps ecoule depuis le debut de la partie
              player         (py.Rect)    : Zone de colision du joueur
              background     (py.Surface) : Image de fond du jeu
              player_model   (py.Surface) : Représentation visuelle du joueur
              memoireOBJ     (dict)       : Mémoire des météorites présentes
              memoirePOS_X   (dict)       : Mémoire des position en x des météorites
              memoirePOS_Y   (dict)       : Mémoire des position en y des météorites
              meteor_model   (py.Surface) : Représentation visuelle des météorites
              flou           (function)   : Applique un effet de flou
              game_loop      (function)   : Renvoi vers une nouvelle partie
              main_menu      (function)   : Renvoi vers le menu principal
              button_height  (float)      : Hauteur standard d'un bouton
              button_spacing (float)      : Espace standard entre deux boutons
              button_width   (float)      : Largeur standard d'un bouton

    Sorties : insert         (bool)       : Insertion en cours
              texte          (str)        : Contenu de la zone de saisie
              tableau_score  (str)        : Lien du fichier CSV de classement
              limite         (bool)       : Sécurité empêchant l'affectation multiple de l'enregistrement des scores

    Gere la fin de partie, avec menu et classement
    """

    game_over_loop = True   #|
    insert = False          #|
    limite = True           #| initialisation des états et du pseudo
    texte = ''              #|
    color = 'grey'          #|

    tableau_score = os.path.join(DATA_DIR, "liste_score.csv")

    py.mouse.set_pos(screen_size[0] / 2, screen_size[1] / 2)    #| apparition de la souris
    py.mouse.set_visible(True)                                  #| et recentrage par sécurité
    py.mixer.music.stop()   # fin de la musique

    while game_over_loop:
        scoreSurf, score_Rect = text(str(elapsed_time), 200, 'black')           #|
        score_Rect.x = screen_size[0] // 2 + 200 - 40 * len(str(elapsed_time))  #| création de la surface et du texte de score final
        score_Rect.y = screen_size[1] // 2 - 150                                #|

        screen.fill('black')
        screen.blit(background, center(background))                                         #|
        screen.blit(player_model, (player.x, player.y))                                     #| affichage des éléments 
        for obj in mémoireOBJ:                                                              #| de la partie figés
            screen.blit(météor_model, (mémoirePOS_X[obj] - 11, mémoirePOS_Y[obj] - 105))    #|
        flou(0, 0, screen_size[0], screen_size[1], 'white', 128)  # application de l'effet de flou

        py.draw.rect(screen, 'white', (screen_size[0] // 2 + 40, screen_size[1] // 2 - 200, 800, 550))                                                      #|
        py.draw.aaline(screen, 'black', (screen_size[0] // 2 + 350, screen_size[1] // 2 - 200), (screen_size[0] // 2 + 350, screen_size[1] // 2 + 350), 2)  #| création et affichage de la zone de classent et du score
        screen.blit(scoreSurf, score_Rect)                                                                                                                  #|

        affiche_classement(lire_score(tableau_score))   # affiche les 10 premiers au classement

        Pseudo_entry = py.draw.rect(screen,color, (screen_size[0] // 2 + 45, screen_size[1] // 2 + 50, 300, 60), 1) #|
        PseudoSurf, Pseudo_Rect = text(texte, 50, 'black')                                                          #|
        Pseudo_Rect.x = screen_size[0] // 2 + 45                                                                    #| création et affichage de la zone d'enrée du pseudo
        Pseudo_Rect.y = screen_size[1] // 2 + 65                                                                    #|
        screen.blit(PseudoSurf, Pseudo_Rect)                                                                        #|

        bouton('ENTRER', 50, 'darkgrey', 'lightgrey', screen_size[0] // 2 + 105, screen_size[1] // 2 + 190, 175, 60, enter) # création du bouton de confirmation du pseudo
        
        for event in py.event.get():    # appel des événements
            if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:   #| retour rapide au
                game_over_loop = False                                  #| menu principal

            if event.type == py.MOUSEBUTTONDOWN:            #|
                if Pseudo_entry.collidepoint(event.pos):    #| sécurité de zone de 
                    insert = True                           #| texte sélectionnée
                    texte = ""                              #|

            if event.type == py.KEYDOWN:
                if insert:
                    if event.key == py.K_BACKSPACE: # enlève 1 caractère au texte
                        texte = texte[:-1]
                    elif event.key == py.K_ESCAPE:  # sort de la zone de texte
                        insert = False
                    elif event.key == py.K_RETURN:  # confirme le choix du pseudo
                        enter()
                    elif event.key != py.K_TAB:                             #|
                        if Pseudo_Rect.width <= Pseudo_entry.width - 30:    #| écriture du pseudo dans la zone de texte
                            texte += event.unicode                          #|

            if insert:          #|
                color = 'black' #| changement de couleur lors du 
            else:               #| survolage du bouton de confirmation
                color = 'grey'  #|
    
        TextSurf, TextRect = text("VOUS AVEZ PERDU", 70, 'black')       #|
        TextRect.center = ((screen_size[0] / 2), (screen_size[1] / 6))  #| titre de la fin de partie
        screen.blit(TextSurf, TextRect)                                 #|

        bouton("Rejouer", 50, 'darkgrey', 'lightgrey', screen_size[0] / 3 - button_width * 0.5 / 2, screen_size[1] / 2 - button_height - button_spacing, button_width * 0.5, button_height, game_loop)  #|
        bouton("Menu Principal", 50, 'darkgrey', 'lightgrey', screen_size[0] / 3 - button_width * 0.5 / 2, screen_size[1] / 2, button_width * 0.5, button_height, main_menu)                            #| création des boutons
        bouton("Quitter", 50, 'darkgrey', 'lightgrey', screen_size[0] / 3 - button_width * 0.5 / 2, screen_size[1] / 2 + button_height + button_spacing, button_width * 0.5, button_height, exit)       #|
        
        py.display.update() #| mise à jour de
        clock.tick(60)      #| l'affichage