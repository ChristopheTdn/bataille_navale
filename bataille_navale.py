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
        self.liste_cpu_jouable = []
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
                self.liste_cpu_jouable.append(i+str(j))
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

    def tour_de_jeu(self):
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
            except (IndexError, ValueError):
                self.affiche(self.grille_joueur_cherche,
                             self.grille_cpu_cherche)
                print(RED + "Erreur de coordonnée !!!")

        reponse_joueur = (self.salve(
            X, Y, self.list_bateaux_cpu, self.grille_joueur_cherche))

        # Le CPU JOUE
        while tir not in self.liste_cpu_jouable:
            tir = ""
            for bateau in self.list_bateaux_joueur:
                print("TirIA >>", bateau.long_name, ">>", bateau.ia_cible)
                if len(bateau.ia_cible) > 0:
                    tir = random.choice(bateau.ia_cible)
                    bateau.ia_cible.remove(tir)
                    break
            if tir == "":
                tir = random.choice(self.liste_cpu_jouable)

        X = tir[0]
        Y = int(tir[1:])
        self.liste_cpu_jouable.remove(tir)

        reponse_CPU = WHITE + " | Tir CPU en " + \
            CYAN + X + str(Y) + \
            WHITE + ">>  " + CYAN + \
            self.salve(X, Y, self.list_bateaux_joueur,
                       self.grille_cpu_cherche)

        # Affiche les resultats

        self.affiche(self.grille_joueur_cherche, self.grille_cpu_cherche)

        print("")
        print(reponse_joueur, reponse_CPU)
        for bateau in self.list_bateaux_joueur:
            print("TirIA >>", bateau.long_name, "(" + bateau.ia_diposition +
                  ")>>", bateau.ia_cible)

    def salve(self, X, Y, liste, grille):

        reponse = ""
        tir = X + str(Y)
        for bateau in liste:
            if tir in bateau.position:
                grille[(X, Y)] = bateau.name
                reponse = RED + bateau.test_tir(tir)
                if "touché" in reponse and bateau.ia_diposition == "":
                    # determine le sens du bateau si possible
                    if grille[(X, Y+1)] == bateau.name or grille[(X, Y-1)] == bateau.name:
                        bateau.ia_diposition = "vertical"
                    if grille[(self.largeur_string[self.largeur_string.index(X) - 1], Y)] == bateau.name or \
                            grille[(self.largeur_string[self.largeur_string.index(X) + 1], Y)] == bateau.name:
                        bateau.ia_diposition = "horizontal"

                if "coulé" in reponse:
                    bateau.ia_cible = []
                else:
                    self.IA_cpu(X, Y, bateau)

        if reponse == "":
            reponse = CYAN + "A l eau..."
            grille[(X, Y)] = "X"
        return reponse

    def IA_cpu(self, X, Y, bateau):
        """Gestion des tirs suivants si on trouve un bateau

        Arguments:
            X {STR} -- Tir au format "ABCDEF..."
            Y {INT} -- Tir ordonnée
        """

        xx = self.largeur_string.index(X)
        liste_cible_possible = bateau.ia_cible
        disposition = bateau.ia_diposition

        if disposition != "vertical":
            if xx - 1 >= 0 and \
                    self.largeur_string[xx - 1] + str(Y) in self.liste_cpu_jouable and \
                    self.largeur_string[xx - 1] + str(Y) not in liste_cible_possible:
                liste_cible_possible.append(self.largeur_string[xx - 1] + str(Y))

            if xx + 1 < self.largeur and \
                    self.largeur_string[xx + 1] + str(Y) in self.liste_cpu_jouable and \
                    self.largeur_string[xx + 1] + str(Y) not in liste_cible_possible:
                liste_cible_possible.append(self.largeur_string[xx + 1] + str(Y))

        if disposition != "horizontal":
            if Y - 1 >= 1 and \
                    X + str(Y-1) in self.liste_cpu_jouable and \
                    X + str(Y-1) not in liste_cible_possible:
                liste_cible_possible.append(X + str(Y - 1))

            if Y + 1 <= self.hauteur and \
                    (X + str(Y+1)) in self.liste_cpu_jouable and \
                    (X + str(Y+1)) not in liste_cible_possible:
                liste_cible_possible.append(X + str(Y + 1))

        bateau.ia_cible = liste_cible_possible


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
        game.tour_de_jeu()
