import pygame as py
import os

#---------------------------#
# Déclaration des variables #
#---------------------------#

py.init()                                                                       #|
screen_size = py.display.get_desktop_sizes()[0]                                 #| initialisation de la
min_size = min(screen_size[0], screen_size[1])                                  #| fenêtre et de ses dimensions
screen = py.display.set_mode((screen_size[0], screen_size[1]), py.RESIZABLE)    #|

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datas')    # chemin vers le répertoire data

py.display.set_caption('Astrogame')                                     #|
logo = py.image.load(os.path.join(DATA_DIR, 'casque.png')).convert()    #| titre et logo de la fenêtre 
py.display.set_icon(logo)                                               #|

clock = py.time.Clock() # fréquence d'images du programme

py.mixer.init()                         #|
volume_level = 0.5                      #| initialisation du système audio
py.mixer.music.set_volume(volume_level) #|

active_button = None    # défini l'appui de bouton à nul

#--------------------------#
# Définition des fonctions #
#--------------------------#

def text(text, taille_police = 20, couleur = 'BLACK'):
    """
    Entrées : text                      (str)                   : Texte à afficher
              taille_police             (int)                   : Taille du texte
              couleur                   ((int, int, int) / str) : Couleur du texte en RGB

    Sorties : texte_surface             (pygame.Surface)        : Surface contenant le texte rendu
              texte_surface.get_rect()  (pygame.Rect)           : Dimensions de la surface de texte
    
    Renvoie la surface et les dimensions d'un texte donné pour pouvoir l'afficher
    """

    font = py.font.Font(None, taille_police)   # crée le système d'écriture
    texte_surface = font.render(text, True, couleur)    # crée la surface du texte
    return texte_surface, texte_surface.get_rect()

def bouton(txt, font_size, color_inactive, color_active, x_position, y_position, largeur, hauteur, action = None):
    global active_button
    """
    Entrées : txt               (str)                   : Texte contenu dans le bouton
              font_size         (int)                   : Taille du texte
              color_inactive    (str)                   : Nom du fichier image pour l'état normal du bouton
              color_active      (str)                   : Nom du fichier image pour l'état survolé du bouton
              x_position        (int)                   : Position horizontale du coin supérieur gauche du bouton
              y_position        (int)                   : Position verticale du coin supérieur gauche du bouton
              largeur           (int)                   : Largeur du bouton
              hauteur           (int)                   : Hauteur du bouton
              action            (function)              : Fonction à exécuter lorsqu'on clique sur le bouton, None si aucune fonction n'est à appeler
              active_button     ((int, int, int, int))  : Zone du bouton en cours d'appui, None si aucun bouton n'est appuyé

    Sorties : active_button     ((int, int, int, int))  : Zone du bouton en cours d'appui, None si aucun bouton n'est appuyé

    Crée et affiche un bouton interatif avec une couleur pour chaque état (normal et actif) et qui effectue une action donnée
    """
    
    mouse_pos = py.mouse.get_pos()  # position de la souris
    mouse_pressed = py.mouse.get_pressed()  # pressions des clics et boutons de la souris
    survol = x_position < mouse_pos[0] < x_position + largeur and y_position < mouse_pos[1] < y_position + hauteur  # si la souris se trouve sur la zone du bouton ou non

    image_inactive_surface = py.Surface((largeur, hauteur)) #| charge les images
    image_active_surface = py.Surface((largeur, hauteur))   #| associées au bouton

    image_inactive_surface.fill(color_inactive)
    image_active_surface.fill(color_active)

    text_surf, text_rect = text(txt, font_size)         #|
    x = x_position + largeur / 2 - text_rect.width / 2  #| crée et positionne le texte
    y = y_position + hauteur / 2 - text_rect.height / 2 #|

    if not image_active_surface.get_locked() or not image_inactive_surface.get_locked():
        if survol:  # affiche le bouton comme actif
            screen.blit(image_active_surface, (x_position, y_position))            
        else:       # affiche le bouton comme normal
            screen.blit(image_inactive_surface, (x_position, y_position))
    screen.blit(text_surf, (x, y))

    if survol and mouse_pressed[0]: # si le joueur clic sur la zone du bouton
        if active_button is None:   # si aucun autre bouton n'est appuyé
            active_button = (x_position, y_position, largeur, hauteur)
    
    if active_button == (x_position, y_position, largeur, hauteur): # si le bouton appuyé est le bouton actuel
        if not survol:  # si la souris n'est plus sur le bouton
            active_button = None    # annule l'appui
            return
        if not mouse_pressed[0]:    # si le bouton est relâché
            if survol and action is not None:   # si une action est donnée et si la souris est encore sur la zone du bouton
                active_button = None
                action()  # Appel la fonction donnée

def resize(rect = py.Surface, m_width = -1, m_height = -1):
    """
    Entrées : rect     (py.Surface) : Surface a redimensionner
              m_width  (int)        : Largeur maximale, aucune par défaut
              m_height (int)        : Hauteur maximale, aucune par défaut

    Sorties : (null)   (py.Surface) : Surface redimensionnée

    Redimensionne la surface donn"e pour s'adapter à l'écran ou correspondre à des dimensions données
    """
    
    rat = 0 # coeficient de proportionnalité

    if m_width > 0: # s'il y a une limite de largeur
        rat = m_width / rect.get_width()
    elif m_height > 0:  # s'il y a une limite de hauteur
        rat = m_height / rect.get_height()
    elif min_size == screen_size[0]:    # si l'écran est plus haut que large
        rat = screen_size[0] / rect.get_width()
    else:   # si l'écran est plus large que haut
        rat = screen_size[1] / rect.get_height()

    return py.transform.scale(rect, (rect.get_width() * rat, rect.get_height() * rat))  # redimensionne selon le rapport

def center(rect = py.Surface):
    """
    Entrées : rect   (py.Surface)    : Surface à centrer

    Sorties : [x, y] tuple(int, int) : Coordonnées centrées

    Renvoi les coordonnées pour centrer une surface donnée par rapport à l'écran
    """
    
    x = round(screen_size[0] / 2 - rect.get_width() / 2)
    y = round(screen_size[1] / 2 - rect.get_height() / 2)
    return [x, y]