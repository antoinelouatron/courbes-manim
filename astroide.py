from manim import *

import construction_courbe as cc
import tex_commands as tc

# deux chaînes utiles pour la suite, utilisées dans des
# f-string
PI_2 = tc.Frac("\\pi", 2)
PI_4 = tc.Frac("\\pi", 4)

class Astroide(cc.PasAPas):

    INTERVALLE_LEGENDE = 1.4
    PARAMS = [] # valeurs du paramètre
    LEGENDES = [] #positions des légendes pour les points
    TEXTES_POINTS = [] # textes affichés en haut
    # présentation des symétries
    SYMETRIES = [
        cc.Symetrie(
            lambda t: -t,
            lambda M: np.array([M[0], -M[1], 0]),
            "-t",
            (1,2),
            Tex("On a $M(-t) = "+ tc.Matrix(["x(t)", "-y(t)"]) +"$").scale(0.7).move_to(cc.PasAPas.TEXT_DROITE),
            Tex("M(-t) est le symétrique de M(t) par rapport à (Ox)").scale(0.7).move_to(cc.PasAPas.TEXT_DROITE),
            ["$[-\\pi, \\pi]$", "$[0, \\pi]$", "$[-\\pi, 0]$"],
            (0, np.pi), # p_range
            couleur=BLUE
        ),
        cc.Symetrie(
            lambda t: np.pi - t,
            lambda M: np.array([-M[0], M[1], 0]),
            "$\\pi-t$",
            (0, 0.8),
            Tex("On a $M(\\pi-t) = " + tc.Matrix(["-x(t)", "y(t)"]) + "$").scale(0.7).move_to(cc.PasAPas.TEXT_DROITE),
            Tex("$M(\\pi-t)$ est le symétrique de M(t)\\\\ par rapport à (Oy)").scale(0.7).move_to(cc.PasAPas.TEXT_DROITE + LEFT*0.3),
            ["$[0, \\pi]$", f"$[0, {PI_2}]$", f"$[{PI_2}, \\pi]$"],
            (0, np.pi/2),
            couleur=ORANGE
        ),
        cc.Symetrie(
            lambda t: np.pi/2 - t,
            lambda M: np.array([M[1], M[0], 0]),
            f"${PI_2}-t$",
            (0.2, 0.6),
            Tex(f"On a $M({PI_2}-t) = " + tc.Matrix(["y(t)", "x(t)"]) + "$").scale(0.7).move_to(cc.PasAPas.TEXT_DROITE),
            Tex(f"$M({PI_2} - t)$ est le symétrique de M(t)\\\\ par rapport à $D : y = x$").scale(0.7).move_to(cc.PasAPas.TEXT_DROITE),
            [f"$[0, {PI_2}]$", f"$[0, {PI_4}]$", f"$[{PI_4}, {PI_2}$"],
            (0, np.pi/4),
            couleur=GREEN
        )
    ]
    POINTS_REGULIERS = [
        (
            f"${PI_4}$",
            cc.Tangente(
                np.pi/4,
                np.array([-1,1,0], dtype=int),
                1/5/np.sqrt(2)
            )
        )
    ]
    POINTS_SINGULIERS = [ # étude d'un point singulier
        cc.PointSingulier(
            "0", # en 0
            cc.Tangente(0, np.array([-3,0,0], dtype=int), 1/15),
            2, # p = 2
            3, # q = 3
            cc.POINT_REBROUSSEMENT1 # type du point
        )
    ]

    def x(self, t):
        return np.cos(t)**3

    def y(self, t):
        return np.sin(t)**3

    def annonce_courbe(self):
        """
        Annonce de la courbe à tracer.
        """
        txt1 = Text("La courbe étudiée ici est").scale(0.7).move_to(self.TEXT_DROITE)
        txt2 = MathTex(
            "t \\mapsto" + tc.Matrix(["x(t)", "y(t)"]) +
            " = " + tc.Matrix(["\\cos^3(t)", "\\sin^3(t)"])
        ).next_to(txt1, DOWN).scale(0.7)
        self.affiche_texte(
            txt1,
            txt2
        )
        self.wait(self.INTERVALLE_LEGENDE)
        txt3 = Tex("Comme $M(t+2\\pi) = M(t)$,").next_to(txt2, DOWN).scale(0.7)
        self.affiche_texte(
            txt3,
            Tex("on l'étudie sur $[-\\pi, \\pi]$").next_to(txt3, DOWN).scale(0.7),
            remplace=False
        )
    
    def variations(self):
        txt1 = Tex(
            f"$x$ est décroissante sur $[0, {PI_4}]$."
        ).move_to(self.TEXT_DROITE).scale(0.7)
        self.affiche_texte(txt1)
        self.wait(self.INTERVALLE_LEGENDE)
        txt2 = Tex(
            "$y$ est croissante sur $[0, {PI_4}]$,"
        ).next_to(txt1, DOWN).scale(0.7)
        self.affiche_texte(txt2, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*1.5)