from manim import *

from construction_courbe import PasAPas, Symetrie, Tangente

class Lissajous(PasAPas):

    # on place 3 points en préambule
    # pour illustrer l'interprétation de x et y
    PARAMS = [0, 1, 2]
    LEGENDES = [
        {"x": DOWN/3, "y": LEFT/3, "M": UP/2},
        {"x": DOWN/3, "y": LEFT/3, "M": UP/2},
        {"x": UP/3, "y": RIGHT/3, "M": DOWN/2}
    ] #positions des légendes pour les points
    TEXTES_POINTS = [
        Text("Plaçons M(0)").move_to(3.2*UP+3*RIGHT),
        # placement dans la scene
        Text("puis M(1)").move_to(3.2*UP+2*RIGHT),
        Text("et M(2)").move_to(3.2*UP+2*RIGHT)
    ] # textes affichés en haut
    # présentation des symétries
    SYMETRIES = [
        Symetrie(
            #transforme
            lambda t: -t,
            #sym_M, retourne M(-t)
            lambda M: np.array([M[0], -M[1], 0]),
            # texte à afficher dans M(...)
            "-t",
            #deux paramètres pour animer M(t) et M(-t)
            (0.2, 1),
            # presentation, mise à l'échelle et placement
            Tex(
                "On a $M(-t) = \\begin{pmatrix}x(t) \\\\ -y(t) \\end{pmatrix}$"
            ).scale(0.7).move_to(PasAPas.TEXT_DROITE),
            # conclusion
            Tex(
                "M(-t) est le symétrique de M(t) par rapport à (Ox)"
            ).scale(0.7).move_to(PasAPas.TEXT_DROITE),
            # les intervalles
            ["$[-\\pi, \\pi]$", "$[0, \\pi]$", "$[-\\pi, 0]$"],
            (0, np.pi), # p_range
            couleur=BLUE_B
        ),
        Symetrie(
            lambda t: np.pi - t,
            lambda M: np.array([-M[0], -M[1], 0]),
            "$\\pi-t$",
            (0.3, 1.2),
            Tex(
                "On a $M(\\pi-t) = \\begin{pmatrix}-x(t) \\\\ -y(t) \\end{pmatrix}$"
            ).scale(0.7).move_to(PasAPas.TEXT_DROITE),
            Tex(
                "$M(\\pi-t)$ est le symétrique de M(t) par rapport à O"
            ).scale(0.7).move_to(PasAPas.TEXT_DROITE),
            ["$[0, \\pi]$", "$[0, \\frac{\\pi}{2}]$", "$[\\frac{\\pi}{2}, \\pi]$"],
            (0, np.pi/2),
            couleur=GREEN_B
        )
    ]
    POINTS_REGULIERS = [
        (
            "0", # au paramètre 0
            Tangente(0, np.array([0,2,0], dtype=int), 1/5)
            # la tangente en 0 est dirigée par (0, 2) et on trace
            # (0, 2/5) dans le repère
        ),
        (
            "$\\frac{\\pi}{4}$",
            Tangente(np.pi/4, np.array([-1,0,0], dtype=int), 2/5)
        ),
        (
            "$\\frac{\\pi}{2}$",
            Tangente(np.pi/2, np.array([-1,-2,0], dtype=int), 2/5/np.sqrt(5))
        )
    ]

    def x(self, t):
        return np.cos(t)

    def y(self, t):
        return np.sin(2*t)
    
    def intro(self):
        super().intro()
        self.wait(self.INTERVALLE_LEGENDE)
        self.affiche_texte(Paragraph(
            "Rappelons tout d'abord l'interprétation",
            "graphique des fonctions coordonnées.",
            "On note M(t) le point de paramètre t.",
            alignment="center"))
        self.wait(self.INTERVALLE_LEGENDE*4)
        self.efface_textes()

    def annonce_courbe(self):
        """
        Annonce de la courbe à tracer.
        """
        # self.TEXT_DROITE est la position en haut de la colonne de droite
        # une fois le repère déplacé. Attention à la longueur du texte.
        txt1 = Text(
            "La courbe étudiée ici est"
        ).scale(0.7).move_to(self.TEXT_DROITE)
        # MathTex insère les $ automatiquement
        txt2 = MathTex(
            "t \\mapsto\\begin{pmatrix}x(t) \\\\ y(t)\\end{pmatrix}" +
            "= \\begin{pmatrix}\\cos(t) \\\\ \\sin(2t)\\end{pmatrix}"
        ).next_to(txt1, DOWN).scale(0.7) # placement en dessous.
        self.affiche_texte(
            txt1,
            txt2
        )
        self.wait(self.INTERVALLE_LEGENDE)
        txt3 = Tex(
            "Comme $M(t+2\\pi) = M(t)$,"
        ).next_to(txt2, DOWN).scale(0.7)
        self.affiche_texte(
            txt3,
            Tex(
                "on l'étudie sur $[-\\pi, \\pi]$"
            ).next_to(txt3, DOWN).scale(0.7),
            remplace=False
        )
    
    def variations(self):
        """
        Présentation rapide des variations, on se passe de
        self.tableau_variations
        """
        txt1 = Tex(
            "$x$ est décroissante sur $[0, \\frac{\\pi}{2}]$."
        ).move_to(self.TEXT_DROITE).scale(0.7)
        self.affiche_texte(txt1)
        self.wait(self.INTERVALLE_LEGENDE)
        txt2 = Tex(
            "$y$ est croissante sur $[0, \\frac{\\pi}{4}]$,"
        ).next_to(txt1, DOWN).scale(0.7)
        self.affiche_texte(
            txt2,
            Tex(
                "puis décroissante sur $[\\frac{\\pi}{4}, \\frac{\\pi}{2}]$"
            ).next_to(txt2, DOWN).scale(0.7),
            remplace=False
        )
        self.wait(self.INTERVALLE_LEGENDE*1.5)