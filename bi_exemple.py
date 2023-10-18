from fractions import Fraction
from pathlib import Path

from manim import *

import construction_courbe as cc
import tex_commands as tc

class VTex(tc.MyTex):
    """
    Utilisation du package variations en plus
    """

    packages = ["{variations}"]

class BranchesInfiniesExemple(cc.PasAPas):

    SKIP = False
    INTERVALLE_LEGENDE = 1.5
    X_RANGE = (-4.8,8.2,1)
    Y_RANGE = (-5.2, 5.2, 1)
    P_RANGE = [(-5,-1-1/10), (-1+1/10, 1-1/6), (1+1/6, 7)]
    POINTS_REGULIERS = [
        ("0", cc.Tangente(0, np.array([0,-1,0], dtype=int), 1)),
        ("2", cc.Tangente(2, np.array([0,-1,0], dtype=int), 1))
    ]
    ASYMPOTES = [
        cc.AsymptoteHorizontale(0),
        cc.AsymptoteVerticale(Fraction(-1,2)),
        cc.Asymptote([Fraction(1,2), -Fraction(3,4)])
    ]

    def x(self, t):
        return t**2 / (t - 1)

    def y(self, t):
        return t / (t**2 - 1)

    def annonce_courbe(self):
        """
        Annonce de la courbe à tracer.
        """
        txt1 = Text(
            "La courbe étudiée ici est"
        ).scale(0.7).move_to(self.TEXT_DROITE)
        courbe = tc.Matrix([tc.Frac("t^2", "t - 1"), tc.Frac("t", "t^2 - 1")])
        txt2 = MathTex(
            f"t \\mapsto {tc.Matrix(['x(t)', 'y(t)'])} = {courbe}"
        ).next_to(txt1, DOWN).scale(0.7)
        self.affiche_texte(
            txt1,
            txt2
        )
        self.wait(self.INTERVALLE_LEGENDE*1.5)
        txt3 = Tex(
            "Cette courbe ne présente pas de symétrie."
        ).next_to(txt2, DOWN).scale(0.7)
        self.affiche_texte(txt3, remplace=False)
    
    def tableau_variations(self):
        self.annonce_episode("Étude des variations", repere_fin=False)
        cases = tc.Env("cases")
        x_prime = "x'(t) = " + tc.Frac("t(t - 2)", "(t - 1)^2")
        y_prime = "y'(t) = " + tc.Frac("-t^2 - 1", "(t^2 - 1)^2")
        txt1 = Tex("On trouve après dérivation : ").move_to(UP*3)
        self.affiche_texte(txt1)
        txt2 = Tex(
            "$" + cases(f"{x_prime} \\\\ {y_prime}") + "$"
        ).next_to(txt1, DOWN)
        self.affiche_texte(txt2, remplace=None)
        self.wait(self.INTERVALLE_LEGENDE*1.2)
        txt3 = Tex("Les limites ne sont pas indéterminées,").next_to(txt2, DOWN)
        self.affiche_texte(txt3, remplace=False)
        txt4 = Tex("et on obtient le tableau suivant").next_to(txt3, DOWN)
        self.affiche_texte(txt4, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*2)
        dossier_courant = Path(__file__).resolve().parent
        # c'est pénible d'écrire du latex dans une fichier python.
        # On lit un fichier externe
        with open(dossier_courant / "variations_bi_exemple.tex") as f:
            variations = f.read()
        txt5 = VTex(variations).scale(0.7)
        self._tableau = Group(txt5)
        self.affiche_texte(txt5)
        self.wait(self.INTERVALLE_LEGENDE*3)
        # self.interactive_embed()
        # mise en évidence des points à étudier.
        # Les positions ont été trouvées grace à la ligne
        # commentée du dessus qui fonctionne seulement avec openGL
        points_reguliers = [
            Ellipse(width=1, height=1).move_to(UP*1.8 + LEFT*0.05),
            Ellipse(width=1, height=1).move_to(UP*1.8 + RIGHT*4.05)
        ]
        self._tableau.add(*points_reguliers)
        self.play(*[FadeIn(pr) for pr in points_reguliers])
        self.wait(self.INTERVALLE_LEGENDE)
        branches = [
            Circle(radius=0.3, color=BLUE_B).move_to(UP*2.35 + LEFT*4.5),
            Circle(radius=0.3, color=BLUE_B).move_to(UP*2.35 + LEFT*2.2),
            Circle(radius=0.3, color=BLUE_B).move_to(UP*2.35 + RIGHT*2),
            Circle(radius=0.3, color=BLUE_B).move_to(UP*2.35 + RIGHT*5.7)
        ]
        self._tableau.add(*branches)
        self.play(*[FadeIn(b) for b in branches])
        self.wait(self.INTERVALLE_LEGENDE)
        # on anime autour du point central du tableau de variations
        self.play(*[
            obj.animate.scale(0.6, about_point=txt5.get_center())
            for obj in self._tableau
            ])
        self.play(*[obj.animate.shift(UP*1.5) for obj in self._tableau])
        # conclusion
        txt = Tex("On étudie 2 points réguliers,").next_to(txt5, DOWN).scale(0.8)
        self.affiche_texte(txt, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE)
        txt = Tex("et 4 branches infinies.").next_to(txt, DOWN).scale(0.8)
        self.affiche_texte(txt, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*1.2)
        self.play(*[FadeOut(c) for c in branches + points_reguliers])
    
    def asymptotes(self):
        txt = Tex("Rappelons tout d'abord les variations.").move_to(UP*3)
        self.affiche_texte(txt)
        self.wait(self.INTERVALLE_LEGENDE)
        # affichage des variations et des points d'étude
        groupe = [
            e.shift(DOWN*1.5) # translation ves le bas
            for i, e in enumerate(self._tableau) if i not in range(1,3)
        ]
        self.affiche_texte(*groupe, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*2)
        self.efface_textes()
        txt = Tex(
            "Lorsque $t \\to \\pm \\infty$, l'étude est immédiate,"
        ).move_to(UP*2)
        txt2 = Tex(
            f"on obtient une {self.ASYMPOTES[0].texte()}."
        ).next_to(txt, DOWN)
        txt3 = Tex(
            "Lorsque $t \\to -1$, l'étude est immédiate,"
        ).next_to(txt2, DOWN)
        txt4 = Tex(
            f"on obtient une {self.ASYMPOTES[1].texte()}."
        ).next_to(txt3, DOWN)
        self.affiche_texte(txt, txt2)
        self.wait(self.INTERVALLE_LEGENDE*2)
        self.affiche_texte(txt3, txt4, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*2)
        # étude en 1
        point_lim = tc.Tend("t", "1")
        limites = tc.Env("cases")(
            f"x(t) {point_lim} \\mp\\infty \\\\ y(t) {point_lim} \\mp\\infty"
        )
        txt = Tex(f"En revanche on a ${limites}$").move_to(UP*3)
        demi = tc.Frac(1, 2)
        quotient = tc.Frac("x(t)", "y(t)") + point_lim + demi
        txt2 = Tex(
            f"Après calcul, on trouve que ${quotient}$."
        ).next_to(txt, DOWN)
        txt3 = Tex(
            f"Nous devons donc étudier la limite de $y(t) - {demi}x(t)$ en 1."
        )
        txt3 = txt3.next_to(txt2, DOWN)
        self.affiche_texte(txt)
        self.wait(self.INTERVALLE_LEGENDE)
        self.affiche_texte(txt2, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*1.5)
        self.affiche_texte(txt3, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*2)
        diff = tc.Frac("t(t+2)", "2(t+1)")
        txt = Tex(
            "On calcule cette différence par mise au même dénominateur,"
        ).move_to(UP*3)
        txt2 = Tex(
            "et après factorisation des polynômes on trouve que"
        ).next_to(txt, DOWN)
        val_lim = tc.Frac(3, 4)
        txt3 = MathTex(
            f"y(t) - {demi}x(t) = -{diff} {point_lim} -{val_lim}"
        ).next_to(txt2, DOWN)
        txt4 = Tex(
            f"On obtient une {self.ASYMPOTES[2].texte()}"
        ).next_to(txt3, DOWN)
        self.affiche_texte(txt)
        self.wait(self.INTERVALLE_LEGENDE)
        self.affiche_texte(txt2, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE)
        self.affiche_texte(txt3, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*2)
        self.affiche_texte(txt4, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*2)
        self.efface_textes()
        # super().asymptotes s'occupe des annonces et du tracé des asymptotes
        # données dans self.ASYMPTOTES
        return super().asymptotes()