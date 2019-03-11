class Bateau():
    """
    Gestion de la creation des bateau avec leur nom,
     identifiant taille et position dans la grille

    """

    def __init__(self, name, long_name, taille):
        """Initialise  la classe Bateau

        Arguments:
            name {str} -- nom du bateau
            long_name {str} -- nom du bateau
            taille {int} -- taille en case
            position {list} -- [liste des cases du bateau]
        """

        self.name = name
        self.long_name = long_name
        self.taille = taille
        self.position = []
        self.integrite = []

    def place_bateau(self, grille, largeur, hauteur):
        import random
        place_bateau = True
        while place_bateau:
            X = random.randint(1, largeur)
            Y = random.randint(1, hauteur)
            ok = True
            if grille[(chr(64+X), Y)] != ".":
                ok = False
            else:
                # determine horizontal ou vertical
                if random.randint(1, 2) == 1 and \
                     (X + self.taille <= largeur):  # horizontal
                    # test si les cases vont bien
                    for i in range(self.taille):
                        if grille[((chr(64+X + i)), Y)] != ".":
                            ok = False
                    if ok:
                        for i in range(self.taille):
                            grille[((chr(64 + X + i)), Y)] = self.name
                            self.integrite.append((chr(64 + X + i)) + str(Y))
                            self.position.append((chr(64 + X + i)) + str(Y))
                            place_bateau = False
                elif Y + self.taille <= hauteur:
                    for i in range(self.taille):
                        if grille[((chr(64+X)), Y+i)] != ".":
                            ok = False
                    if ok:
                        for i in range(self.taille):
                            grille[((chr(64 + X)), Y + i)] = self.name
                            self.integrite.append(chr(64 + X) + str(Y + i))
                            self.position.append(chr(64 + X) + str(Y + i))
                            place_bateau = False

    def test_tir(self, tir):
        '''Test le tir du joueur et renvois l'interface avec la mention touche ou coule

        Arguments:
            tir {str} -- sous la forme LETTRENOMBRE,
                         la lettre va de A a Z et le nombre de 1 a 26
        '''
        if tir in self.integrite:
            self.integrite.remove(tir)

        if len(self.integrite) == 0:
            return (self.long_name + " coulé !!!")
        else:
            return (self.long_name + " touché !!!")
