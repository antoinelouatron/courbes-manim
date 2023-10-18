from manim import *
from construction_courbe import PasAPas
import numpy as np

class CercleUnite(PasAPas):
    
        X_RANGE = (-1.2, 1.2)
        Y_RANGE = (-1.2, 1.2)
        P_RANGE = (-np.pi, np.pi)

        def x(self, t):
            return np.cos(t)
        
        def y(self, t):
            return np.sin(t)
        
        def annonce_courbe(self):
             # un premier texte, placé à droite du repère
             t1 = Tex("On étudie la courbe").move_to(self.TEXT_DROITE)
             self.affiche_texte(t1)
             # un deuxième texte, sous le premier
             t2 = Tex("$x(t) = \\cos(t),\\ y(t) = \\sin(t)$").next_to(t1, DOWN)
             self.affiche_texte(t2, remplace=False) # ne pas remplacer le premier texte.
             # Un temps de lecture
             self.wait(self.INTERVALLE_LEGENDE)
             # une conclusion, qui efface les deux premiers textes.
             self.affiche_texte(Tex("On l'étudie sur $[-\\pi, \\pi]$.").move_to(
                  self.TEXT_DROITE
             ))
