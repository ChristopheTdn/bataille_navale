"""
Bataille Navale

Petit jeu console pour s'entrainer un peu

Auteur : ToF
years : 2019
"""
# import
import sys
import random
from colorama import init, Fore
init()

# class


class Core():
    """
     Création du coeur de jeu Bataille navale

    """

    def __init__(self, largeur=10, hauteur=10, DEBUG=False):
        """initialise la classe Core de la bataille_navale

        Keyword Arguments:
            largeur {int} -- largeur de la grille en nombre (default: {10})
            hauteur {int} -- hauteur de la grille en nombre (default: {10})
        """
        self.tour = 0
        self.DEBUG = DEBUG
        self.grille_cpu_bateau = dict()
        self.grille_cpu_cherche = dict()
        self.grille_joueur_bateau = dict()
        self.grille_joueur_cherche = dict()
        self.lst_cpu_jouable = []
        self.lst_bateaux_cpu = []
        self.lst_bateaux_joueur = []
        self.largeur = largeur
        self.largeur_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:self.largeur]
        self.hauteur = hauteur
        # rempli les mers de vide (".")
        self.init_grilles()
        # place les bateaux du CPU et du joueur
        self.crea_grille(self.grille_cpu_bateau, self.lst_bateaux_cpu)
        self.crea_grille(self.grille_joueur_bateau, self.lst_bateaux_joueur)
        self.aff_titre()

    def init_grilles(self):
        """Création des grilles et des listes de jeu
        """

        for j in range(1, self.hauteur+1):
            for i in self.largeur_str:
                self.grille_cpu_bateau[(i, j)] = "."
                self.grille_cpu_cherche[(i, j)] = "."
                self.lst_cpu_jouable.append(i+str(j))
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
        """Affiche les grilles passées en parametre cote a côte

        Arguments:
            grille {dict} -- Un dictionnaire au format (A,1) = "." pour la mer
            grille2 {dict} -- idem grille2 - Default = None
        """

        print('\x1b[2J')  # cls
        self.aff_titre()
        # GRILLE 1
        print(GREEN + "   | ", end="")
        for i in self.largeur_str:
            print(GREEN + " " + i + " ", end="")

        # GRILLE 2
        if grille2:
            print('   ', end="")
            print(GREEN + "   | ", end="")
            for i in self.largeur_str:
                print(GREEN + " " + i + " ", end="")

        print("")
        # GRILLE 1
        print(GREEN + "---|-", end="")
        for i in self.largeur_str:
            print(GREEN + "---", end="")
        print("   ", end="")
        # GRILLE 2
        if grille2:
            print(GREEN + "---|-", end="")
            for i in self.largeur_str:
                print(GREEN + "---", end="")

        for j in range(self.hauteur):
            print("")
            # GRILLE 1
            print(GREEN + "{0:2d}".format(j + 1)+" | ", end="")
            for i in self.largeur_str:
                couleur = RED
                if grille[(i, j + 1)] == "X":
                    couleur = BLUE
                if grille[(i, j + 1)] == ".":
                    couleur = CYAN
                print(couleur, grille[(i, j + 1)] + " ", end='')
            # GRILLE 2
            if grille2:
                print("   ", end="")
                print(GREEN + "{0:2d}".format(j + 1)+" | ", end="")
                for i in self.largeur_str:
                    couleur = RED
                    if grille2[(i, j + 1)] == "X":
                        couleur = BLUE
                    if grille2[(i, j + 1)] == ".":
                        couleur = CYAN
                    print(couleur, grille2[(i, j + 1)] + " ", end='')

        print("\n")
        for bateau in self.lst_bateaux_cpu:
            print(bateau.long_name, " (", len(bateau.integrite),
                  "/", bateau.taille, " cases)", sep="")

    def tour_de_jeu(self):
        '''
         Chaque tour un tir du joueur et un tir du CPU
        '''
        self.tour += 1

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
                print(RED + "ERREUR !!! : " +
                      WHITE + "Erreur de coordonnée !!!")

        reponse_joueur = WHITE + "Tir JOUEUR en " + \
            CYAN + X + str(Y) + \
            WHITE + " >>  " + CYAN + \
            (self.salve(X,
                        Y,
                        self.lst_bateaux_cpu,
                        self.grille_joueur_cherche))

        # Le CPU JOUE
        tir = ""

        while tir not in self.lst_cpu_jouable:
            tir = ""
            for bateau in self.lst_bateaux_joueur:
                print("TirIA >>", bateau.long_name, ">>", bateau.ia_cible)
                if len(bateau.ia_cible) > 0:
                    tir = random.choice(bateau.ia_cible)
                    bateau.ia_cible.remove(tir)
                    break
            if tir == "":
                tir = random.choice(self.lst_cpu_jouable)

        X = tir[0]
        Y = int(tir[1:])
        self.lst_cpu_jouable.remove(tir)

        reponse_CPU = WHITE + " | Tir CPU en " + \
            CYAN + X + str(Y) + \
            WHITE + " >>  " + CYAN + \
            self.salve(X, Y, self.lst_bateaux_joueur,
                       self.grille_cpu_cherche)

        # Affiche les resultats

        self.affiche(self.grille_joueur_cherche, self.grille_cpu_cherche)

        print("")
        print(reponse_joueur, reponse_CPU, "\n")

        if self.DEBUG:
            for bateau in self.lst_bateaux_joueur:
                print(GREEN + "TirIA >>", bateau.long_name,
                      "(" + bateau.ia_diposition + ")>>", bateau.ia_cible)

        self.fin_de_jeu()

    def fin_de_jeu(self):
        """
        Test la flote (liste) de chaque joueur pour savoir
        si il reste des bateaux et prononce le gagnant au besoin
        """

        if self.test_victoire(self.lst_bateaux_cpu):
            print("\n",
                  RED + " VICTOIRE !!! " +
                  WHITE + "Vous avez coulé toute la flotte ennemie ! (score=" +
                  RED + "{}".format(self.tour) +
                  WHITE + " tours)",
                  "\n")
            sys.exit(0)
        if self.test_victoire(self.lst_bateaux_joueur):
            print("\n",
                  RED + " DEFAITE !!! " +
                  WHITE + "L ordinateur a coulé tous vos bateaux ! (score=" +
                  RED + "{}".format(self.tour) +
                  WHITE + " tours)",
                  "\n")
            sys.exit(0)
        return False

    def salve(self, X, Y, liste, grille):

        reponse = ""
        tir = X + str(Y)
        for bateau in liste:
            if tir in bateau.position:
                grille[(X, Y)] = bateau.name
                reponse = RED + bateau.test_tir(tir) + WHITE
                if "touché" in reponse and bateau.ia_diposition == "":
                    xx = self.largeur_str.index(X)

                    # determine le sens du bateau si possible
                    if Y > 1:
                        if grille[(X, Y - 1)] == bateau.name:
                            bateau.ia_diposition = "vertical"
                    if Y < self.hauteur:
                        if grille[(X, Y + 1)] == bateau.name:
                            bateau.ia_diposition = "vertical"

                    if xx >= 1:
                        if grille[(self.largeur_str[xx - 1],
                                   Y)] == bateau.name:
                            bateau.ia_diposition = "horizontal"
                    if xx < self.largeur-1:
                        if grille[(self.largeur_str[xx+1], Y)] == bateau.name:
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

        xx = self.largeur_str.index(X)
        lst_cible_possible = bateau.ia_cible
        disposition = bateau.ia_diposition

        if disposition != "vertical":
            if xx - 1 >= 0 and \
               self.largeur_str[xx - 1] + str(Y) in self.lst_cpu_jouable and \
               self.largeur_str[xx - 1] + str(Y) not in lst_cible_possible:
                lst_cible_possible.append(self.largeur_str[xx - 1] + str(Y))

            if xx + 1 < self.largeur and \
               self.largeur_str[xx + 1] + str(Y) in self.lst_cpu_jouable and \
               self.largeur_str[xx + 1] + str(Y) not in lst_cible_possible:
                lst_cible_possible.append(self.largeur_str[xx + 1] + str(Y))

        if disposition != "horizontal":
            if Y - 1 >= 1 and \
                    X + str(Y-1) in self.lst_cpu_jouable and \
                    X + str(Y-1) not in lst_cible_possible:
                lst_cible_possible.append(X + str(Y - 1))

            if Y + 1 <= self.hauteur and \
                    (X + str(Y+1)) in self.lst_cpu_jouable and \
                    (X + str(Y+1)) not in lst_cible_possible:
                lst_cible_possible.append(X + str(Y + 1))

        bateau.ia_cible = lst_cible_possible

    def test_victoire(self, liste):
        """
        Test la victoire de l'un des deux camps
        """
        for bateau in liste:
            if len(bateau.integrite) != 0:
                return False  # Au moins un bateau vivant
        return True

    def aff_titre(self):
        titre = ""
        titre += "  ____        _   _   _       _____ _     _"+"\n"
        titre += " |  _ \      | | | | | |     / ____| |   (_)"+"\n"
        titre += " | |_) | __ _| |_| |_| | ___| (___ | |__  _ _ __"+"\n"
        titre += " |  _ < / _` | __| __| |/ _ \\\___ \| '_ \| | '_ \ "+"\n"
        titre += " | |_) | (_| | |_| |_| |  __/____) | | | | | |_) |"+"\n"
        titre += " |____/ \__,_|\__|\__|_|\___|_____/|_| |_|_| .__/"+"\n"
        titre += "                                           | |"+"\n"
        titre += "                                           |_|"+"\n"
        print(titre)


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

    game = Core(10, 10)
    game.affiche(game.grille_joueur_bateau)
    while "jeu_en_cours":
        game.tour_de_jeu()
