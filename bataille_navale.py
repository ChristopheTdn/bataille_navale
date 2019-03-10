"""
Bataille Navale

Petit jeu console pour s'entrainer un peu

Auteur : ToF
years : 2019
"""
# import
import random
from colorama import init, Fore
init()

# class


class Core():
    """
     Création du coeur de jeu Bataille navale

    """

    def __init__(self, largeur=10, hauteur=10):
        self.grille_cpu_bateau = dict()
        self.grille_cpu_cherche = dict()
        self.grille_joueur_bateau = dict()
        self.grille_joueur_cherche = dict()
        self.list_bateaux_cpu = []
        self.list_bateaux_joueur = []
        self.largeur = largeur
        self.largeur_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:self.largeur]
        self.hauteur = hauteur
        # rempli les mers de vide (".")
        self.init_grilles()
        # place les bateaux du CPU et du joueur
        self.crea_grille(self.grille_cpu_bateau, self.list_bateaux_cpu)
        self.crea_grille(self.grille_joueur_bateau, self.list_bateaux_joueur)

    def init_grilles(self):
        for j in range(1, self.hauteur+1):
            for i in self.largeur_string:
                self.grille_cpu_bateau[(i, j)] = "."
                self.grille_cpu_cherche[(i, j)] = "."
                self.grille_joueur_bateau[(i, j)] = "."
                self.grille_joueur_cherche[(i, j)] = "."

    def crea_grille(self, grille, liste):
        """
        Création de la grille a l'aide de l'Objet Bateau

        Arguments:
            grille {[dict]} -- Un dictionnaire au format (A,1) = "."
            liste {[list]} -- La liste des objets 'Bateau' placé sur la grille.
        """

        liste.extend([Bateau("P", "Porte-Avions", 6),
                      Bateau("D", "Destroyer", 5),
                      Bateau("C", "Corvette", 4),
                      Bateau("S", "Sous-Marin", 3),
                      Bateau("E", "Escorteur", 2)])
        for bateau in liste:
            bateau.place_bateau(grille, self.largeur, self.hauteur)

    def affiche(self, grille, grille2=None):
        """Affiche les grilles passées en parametre

        Arguments:
            grille {dict} -- Un dictionnaire au format (A,1) = "." pour la mer
        """
        print('\x1b[2J')  # cls
        # GRILLE 1
        print(GREEN + "   | ", end="")
        for i in self.largeur_string:
            print(GREEN + " " + i + " ", end="")
        # GRILLE 2
        print('   ', end="")
        print(GREEN + "   | ", end="")
        for i in self.largeur_string:
            print(GREEN + " " + i + " ", end="")

        print("")
        # GRILLE 1
        print(GREEN + "---|-", end="")
        for i in self.largeur_string:
            print(GREEN + "---", end="")
        print("   ", end="")
        # GRILLE 2
        if grille2 is not None:
            print(GREEN + "---|-", end="")
            for i in self.largeur_string:
                print(GREEN + "---", end="")

        for j in range(self.hauteur):
            print("")
            print(GREEN + "{0:2d}".format(j + 1)+" | ", end="")
            for i in self.largeur_string:
                couleur = RED
                if grille[(i, j + 1)] == "X":
                    couleur = BLUE
                if grille[(i, j + 1)] == ".":
                    couleur = CYAN
                print(couleur, grille[(i, j + 1)] + " ", end='')
            # GRILLE2
            if grille2 is not None:
                print("   ", end="")
                print(GREEN + "{0:2d}".format(j + 1)+" | ", end="")
                for i in self.largeur_string:
                    couleur = RED
                    if grille2[(i, j + 1)] == "X":
                        couleur = BLUE
                    if grille2[(i, j + 1)] == ".":
                        couleur = CYAN
                    print(couleur, grille2[(i, j + 1)] + " ", end='')

        print("\n")
        for bateau in self.list_bateaux_cpu:
            print(bateau.long_name, " (", len(bateau.integrite),
                  "/", bateau.taille, " cases)", sep="")

    def round(self):
        '''
         Chaque tour un tir du joueur et un tir du CPU
        '''
        # Le JOUEUR COMMENCE

        tir_joueur = False
        while not tir_joueur:
            print(WHITE + "\nEntrer votre salve: ", end="")
            tir = input()
        # parse tir
            try:
                tir = tir.upper()
                X = tir[0]
                Y = int(tir[1:])
                tir_joueur = True
            except ValueError:
                self.affiche(self.grille_joueur_cherche,
                             self.grille_cpu_cherche)
                print(RED + "Erreur de coordonnée !!!")

        reponse_joueur = (self.salve(
            X, Y, self.list_bateaux_cpu, self.grille_joueur_cherche))

        # Le CPU JOUE
        tir_cpu = False
        while not tir_cpu:
            X = self.largeur_string[random.randint(0, self.largeur-1)]
            Y = random.randint(1, self.hauteur)
            if self.grille_cpu_cherche[(X, Y)] == ".":
                tir_cpu = True

        reponse_CPU = WHITE + " | Tir CPU en " + \
            CYAN + X + str(Y) + \
            WHITE + ">>  " + CYAN + \
            self.salve(X, Y, self.list_bateaux_joueur,
                       self.grille_cpu_cherche)

        self.affiche(self.grille_joueur_cherche, self.grille_cpu_cherche)

        print("")
        print(reponse_joueur, reponse_CPU)

    def salve(self, X, Y, liste, grille):

        reponse = ""
        tir = X + str(Y)
        for bateau in liste:
            if tir in bateau.position:
                grille[(X, Y)] = bateau.name
                reponse = RED + bateau.test_tir(tir)
        if reponse == "":
            reponse = CYAN + "A l eau..."
            grille[(X, Y)] = "X"
        return reponse


if __name__ == "__main__":

    # CONSTANTES

    from class_bateau import Bateau
    RED = Fore.RED
    BLUE = Fore.BLUE
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Fore.RESET

    game = Core(12, 12)
    game.affiche(game.grille_joueur_cherche, game.grille_joueur_bateau)
    while "jeu_en_cours":
        game.round()
