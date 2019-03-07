"""
Bataille Navale

Petit jeu console pour s'entrainer un peu

Auteur : ToF
years : 2019
"""

#class
class Core():
    """
     Creation du coeur de jeu Bataille navale

    """
    def __init__(self,largeur=10,hauteur=10):
        self.grille_cpu_bateau = dict()
        self.grille_cpu_cherche = dict()
        self.grille_joueur_bateau = dict()
        self.grille_joueur_cherche = dict()
        self.list_bateaux_cpu = []
        self.largeur = largeur
        self.largeur_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:self.largeur]
        self.hauteur = hauteur
        # remplir grille de .
        self.init_grilles()
        self.crea_grille_cpu()

    def init_grilles(self):
        for j in range(1, self.hauteur+1):
            for i in self.largeur_string:
                self.grille_cpu_bateau[(i, j)] = "."
                self.grille_cpu_cherche[(i, j)] = "."
                self.grille_joueur_bateau[(i, j)] = "."
                self.grille_joueur_cherche[(i, j)] = "."

    def crea_grille_cpu(self):
        bateau1 = Bateau("P", "Porte-Avions", 6)
        bateau1.place_bateau(self.grille_cpu_bateau, self.largeur, self.hauteur)
        bateau2 = Bateau("D", "Destroyer", 5)
        bateau2.place_bateau(self.grille_cpu_bateau,self.largeur, self.hauteur)
        bateau3 = Bateau("C", "Corvette", 4)
        bateau3.place_bateau(self.grille_cpu_bateau,self.largeur, self.hauteur)
        bateau4 = Bateau("S", "Sous-Marin", 3)
        bateau4.place_bateau(self.grille_cpu_bateau,self.largeur, self.hauteur)
        bateau5 = Bateau("E", "Escorteur", 2)
        bateau5.place_bateau(self.grille_cpu_bateau, self.largeur, self.hauteur)
        self.list_bateaux_cpu.append(bateau1)
        self.list_bateaux_cpu.append(bateau2)
        self.list_bateaux_cpu.append(bateau3)
        self.list_bateaux_cpu.append(bateau4)
        self.list_bateaux_cpu.append(bateau5)

    def affiche(self, grille):
        """Affiche la grille passée en parametre
        
        Arguments:
            grille {dict} -- Un dictionnaire au format (A,1) = "." pour la mer
        """
        print('\x1b[2J') #cls
        print ("    ",end="")
        for i in self.largeur_string:
            print (GREEN + i + "  ",end="")
        for j in range(self.hauteur):
            print("")
            print (GREEN + "{0:2d}".format(j + 1)+" ",end="")
            for i in self.largeur_string:
                couleur= RED               
                if grille[(i, j + 1)]=="X" :
                    couleur = BLUE
                if grille[(i, j + 1)]=="." :
                    couleur = CYAN
                print(couleur,grille[(i, j + 1)]+" ", end='')
        print("")
        print ("")
        for bateau in self.list_bateaux_cpu:
            print(bateau.long_name, " (", len(bateau.integrite), "/", bateau.taille," cases)",sep="")
                    
    def salve(self):

        print(WHITE + "\nEntrer votre salve: ", end="")
        tir = input()
        #parse tir
        try:
            tir = tir.upper()
            X=tir[0]
            Y=int(tir[1:])
        except:
            print("Erreur de coordonnée !!!")
            return
        reponse = ""
        for bateau in self.list_bateaux_cpu:
            if tir in bateau.position :
                self.grille_joueur_cherche[(X, Y)]=bateau.name
                reponse = RED + bateau.test_tir(tir)
        if reponse == "":
            reponse = CYAN + "A l eau..."
            self.grille_joueur_cherche[(X, Y)] = "X"

        self.affiche(self.grille_joueur_cherche)
        print("")
        print (reponse)



if __name__ == "__main__":

    # import
    from colorama import init, Fore
    init() 
    # CONSTANTES



    from class_bateau import Bateau
    RED = Fore.RED
    BLUE = Fore.BLUE
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Fore.RESET

    game = Core(12,12)
    game.affiche(game.grille_joueur_cherche)
    while "jeu_en_cours":
        game.salve()
            
