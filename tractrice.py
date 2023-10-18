from manim import *

import construction_courbe as cc
import tex_commands as tc

TH = tc.Command("operatorname")("th")
CH = tc.Command("operatorname")("ch")
SH = tc.Command("operatorname")("sh")
EQUIVALENT = tc.Command("underset")("+\\infty", "\\sim")

class VTex(tc.MyTex):
    """
    Utilisation du package variations en plus de la base
    """

    packages = ["{variations}"]

class Tractrice(cc.PasAPas):

    SKIP = False
    INTERVALLE_LEGENDE = 1.4
    X_RANGE = (-3.9,3.9)
    Y_LENGTH = 2
    Y_RANGE = (-0.2, 1.8)
    PARAMS = [] # valeurs du paramètre
    LEGENDES = [] #positions des légendes pour les points
    TEXTES_POINTS = [] # textes affichés en haut
    # présentation des symétries
    SYMETRIES = [
        cc.Symetrie(
            lambda t: -t,
            lambda M: np.array([-M[0], M[1], 0]),
            "-t",
            (2,3),
            Tex("On a $M(-t) = "+ tc.Matrix(["-x(t)", "y(t)"]) +"$").scale(0.7).move_to(cc.PasAPas.TEXT_DROITE),
            Tex("M(-t) est le symétrique de M(t) par rapport à (Oy)").scale(0.7).move_to(cc.PasAPas.TEXT_DROITE),
            ["$\mathbb{R}$", "$[0, +\\infty[$", "$]-\\infty, 0]$"],
            (0, 4), # p_range pour la partie à étudier
            couleur=BLUE # couleur du symétrique
        )
    ]
    POINTS_REGULIERS = [
        #("$\\ln(1 + \\sqrt{2})$", cc.Tangente(np.log(1 + np.sqrt(2)), np.array([1,-1,0], dtype=int), 1/np.sqrt(2)))
    ]
    POINTS_SINGULIERS = [
        cc.PointSingulier("0", cc.Tangente(0, np.array([0,-1,0], dtype=int), 1/2), 2, 3, cc.POINT_REBROUSSEMENT1)
    ]
    ASYMPOTES = [
        cc.AsymptoteHorizontale(0)
    ]

    def x(self, t):
        return t - np.tanh(t)
    
    def y(self, t):
        return 1 / np.cosh(t)
    
    def intro(self):
        super().intro()
        self.wait(self.INTERVALLE_LEGENDE*0.5)
        self.affiche_texte(Text("La tractrice"))
        self.wait(self.INTERVALLE_LEGENDE*1.5)
    
    def annonce_courbe(self):
        """
        Annonce de la courbe à tracer.
        """
        txt1 = Text("La courbe étudiée ici est").scale(0.7).move_to(self.TEXT_DROITE)
        courbe = tc.Matrix([f"t - {TH}(t)", tc.Frac("1", f"{CH}(t)")])
        txt2 = MathTex(f"t \\mapsto {tc.Matrix(['x(t)', 'y(t)'])} = {courbe}").next_to(txt1, DOWN).scale(0.7)
        self.affiche_texte(
            txt1,
            txt2
        )
        self.wait(self.INTERVALLE_LEGENDE*1.5)
    
    def tableau_variations(self):
        self.annonce_episode("Étude des variations", repere_fin=False)
        cases = tc.Env("cases")
        x_prime = f"x'(t) = {TH}^2(t)"
        y_prime = "y'(t) = -" + tc.Frac(f"{SH}(t)", f"{CH}^2(t)")
        txt1 = Tex("On trouve après dérivation : ").move_to(UP*3)
        self.affiche_texte(txt1)
        txt2 = Tex("$" + cases(f"{x_prime} \\\\ {y_prime}") + "$").next_to(txt1, DOWN)
        self.affiche_texte(txt2, remplace=None)
        self.wait(self.INTERVALLE_LEGENDE*1.2)
        eq_sh = tc.Frac("e^t", 2)
        txt3 = Tex(f"On utilise ${CH}(t){EQUIVALENT}{SH}(t){EQUIVALENT}{eq_sh}$,").next_to(txt2, DOWN)
        self.affiche_texte(txt3, remplace=False)
        txt4 = Tex("et on obtient le tableau suivant").next_to(txt3, DOWN)
        self.affiche_texte(txt4, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*2)
        dossier_courant = Path(__file__).resolve().parent
        # c'est pénible d'écrire du latex dans une fichier python.
        # On lit un fichier externe
        with open(dossier_courant / "variations_tractrice.tex") as f:
            variations = f.read()
        txt5 = VTex(variations).scale(0.7)
        self._tableau = Group(txt5)
        self.affiche_texte(txt5)
        self.wait(self.INTERVALLE_LEGENDE*3)
        self.play(txt5.animate.scale(0.8))
        self.play(txt5.animate.shift(UP*1.5))
        txt = Tex("On étudie 1 point singulier,").next_to(txt5, DOWN).scale(0.8)
        self.affiche_texte(txt, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE)
        txt = Tex("et 1 branche infinie.").next_to(txt, DOWN).scale(0.8)
        self.affiche_texte(txt, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*1.2)
    
    def asymptotes(self):
        lim = tc.Tend('t', '+\\infty')
        limites = tc.Env("cases")(
            f"x(t) {lim} +\\infty \\\\"
            f"y(t) {lim} 0"
        )
        txt1 = Tex(f"On a ${limites}$").move_to(UP)
        txt2 = Tex(f"Et on obtient une {self.ASYMPOTES[0].texte()}").next_to(txt1, DOWN)
        self.affiche_texte(txt1)
        self.wait(self.INTERVALLE_LEGENDE*1.5)
        self.affiche_texte(txt2, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*2)
        self.efface_textes()
        super().asymptotes()
    
    def interpretation(self):
        """
        Texte d'intro à l'interprétation cinématique
        """
        self.annonce_episode("Interprétation cinématique", repere_fin=False)
        txt1 = Tex("Monsieur F. se promène avec son chien Doug.").move_to(UP*1.5)
        txt2 = Tex("Doug est tenu en laisse.").next_to(txt1, DOWN)
        self.affiche_texte(txt1, txt2)
        self.wait(self.INTERVALLE_LEGENDE*2)
        self.play(FadeOut(txt1), FadeOut(txt2)) # attention ils ne sont pas effacés
        self.affiche_repere()

        point_M = Dot(point=self.repere.c2p(0,3), color=ORANGE)
        txt_M = Tex("F").scale(0.8).next_to(point_M, (RIGHT)*0.5)
        point_N = Dot(point=self.repere.c2p(0,2), color=ORANGE)
        txt_N = Tex("D").scale(0.8).next_to(point_N, (DOWN)*0.5)
        laisse = Line(point_M.get_center(), point_N.get_center(), color=ORANGE)
        laisse_groupe = VGroup(point_M, point_N, txt_M, txt_N, laisse)
        self.add(laisse_groupe)
        self.play(laisse_groupe.animate(run_time=2, rate_func=linear).shift(
            self.repere.c2p(0,-4/3)  # mystère !
        ))
        self.wait(self.INTERVALLE_LEGENDE)
        self.play(FadeOut(laisse_groupe), self.cache_repere(joue=False))
        self.play(FadeIn(txt1), FadeIn(txt2))
        txt3 = Tex("À l'instant t=0, Doug apperçoit un écureuil.").next_to(txt2, DOWN)
        self.affiche_texte(txt3, remplace=False)
        self.wait(self.INTERVALLE_LEGENDE*1.5)
        self.efface_textes()
        self.play(FadeIn(laisse_groupe), self.affiche_repere(joue=False))

        point_E = Dot(point=self.repere.c2p(2, 0), color=ORANGE)
        txt_E = Tex("E").scale(0.8).next_to(point_E, (DOWN)*0.5)
        self.play(FadeIn(point_E), FadeIn(txt_E))
        self.wait(self.INTERVALLE_LEGENDE)
        fuite = Tex("L'écureuil fuit !").next_to(self.repere, DOWN*2)
        self.affiche_texte(fuite)
        self.wait(self.INTERVALLE_LEGENDE)
        self.dir_ecureuil = Arrow(
            self.repere.c2p(0,0),
            self.repere.c2p(2,0)
            ).next_to(txt_E, RIGHT)
        self.play(Create(self.dir_ecureuil))
        self.wait(self.INTERVALLE_LEGENDE*2)
        self.efface_textes()
        self.play(
            FadeOut(point_E),
            FadeOut(txt_E),
            FadeOut(self.dir_ecureuil),
            FadeOut(laisse_groupe),
            self.cache_repere(joue=False)
        )
        hypotheses = [
            Tex("Quelle sera la trajectoire de Monsieur F., entraîné par Doug ?").move_to(UP*2),
            Tex("On suppose que : "),
            Tex(f"- La laisse est de longueur constante : $\|{tc.Vect('FD')}\|=1$"),
            Tex("- Elle donne la direction du mouvement (tangente)"),
            Tex("- Doug court à vitesse constante")
        ]
        for i in range(len(hypotheses) - 1):
            hypotheses[i + 1] = hypotheses[i + 1].next_to(hypotheses[i], DOWN)
        for h in hypotheses:
            self.affiche_texte(h, remplace=False)
            self.wait(self.INTERVALLE_LEGENDE)
        self.wait(self.INTERVALLE_LEGENDE)
        self.efface_textes()
        self.affiche_repere()


    def bouge_points(self):
        t_range = self.SYMETRIES[0].p_range

        point_M = Dot(point=self.repere.c2p(0,1), color=ORANGE)
        txt_M = Tex("F").scale(0.8).next_to(point_M, (UP + RIGHT)*0.5)
        point_N = Dot(point=self.repere.c2p(0,0), color=ORANGE)
        txt_N = Tex("D").scale(0.8).next_to(point_N, (DOWN)*0.5)
        point_E = Dot(point=self.repere.c2p(0,0), color=ORANGE)
        txt_E = Tex("E").scale(0.8).next_to(point_E, (DOWN)*0.5)
        param = ValueTracker(0)

        point_M.add_updater(lambda m: m.move_to(
            self.repere.c2p(*self.courbe(param.get_value()))
        ))
        txt_M.add_updater(lambda m: m.next_to(point_M, (UP + RIGHT)*0.5))
        point_N.add_updater(lambda m: m.move_to(
            self.repere.c2p(param.get_value(), 0, 0)
        ))
        txt_N.add_updater(lambda m: m.next_to(point_N, (DOWN)*0.5))
        point_E.add_updater(lambda m: m.move_to(
            self.repere.c2p(2 + param.get_value()*0.8, 0, 0)
        ))
        txt_E.add_updater(lambda m: m.next_to(point_E, (DOWN)*0.5))

        def dessine_laisse():
            return Line(point_M.get_center(), point_N.get_center(), color=ORANGE)

        laisse = always_redraw(dessine_laisse)
        self.add(point_M, txt_M, point_N, txt_N, laisse, point_E, txt_E)
        anim = param.animate(run_time=4, rate_func=linear).set_value(t_range[1])
        self.play(anim)
        self.wait(self.INTERVALLE_LEGENDE)
        conclusion = Tex("Monsieur F. suit notre courbe, appelée tractrice.").next_to(self.repere, DOWN)
        self.affiche_texte(conclusion)
        self.wait(self.INTERVALLE_LEGENDE*3)
    
    def construct(self):
        super().construct()
        self.interpretation()
        self.bouge_points()

    
    

