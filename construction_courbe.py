"""
Module de base pour la construction de courbes paramétrée animée par manim.
"""
import abc
import collections.abc
from fractions import Fraction

import tex_commands as tc
# import logging_conf

from manim import *
import numpy as np

__version__ = 0.4


# pour l'instant on utilise seulement print pour les log
def logger():
    pass

logger.info = print

class Symetrie():
    """
    Les instances de cette classe représentent les éventuelles symétrie
    de la courbe étudiée.
    
    :param transforme: est une fonction qui prend un paramètre t
        et renvoie la valeur du paramètre du point symétrique.
    :param sym_M: est une fonction qui prend un np.array de taille 3
        et renvoie son symétrique sous forme de np.array
    :param texte: est le texte à afficher comme paramètre pour
        le symétrique de M(t). Peut contenir du Latex
    :type texte: str
    :param parametres: est une liste ou un tuple de deux paramètres (nombres)
        à utiliser comme exemple pour afficher deux M(t) ainsi que leurs symétriques.
    :param presentation: est un Text (ou Tex) de description du point symétrique.
        Par exemple "M(-t) = (-x(t), y(t))"
    :param conclusion: est un Text de conclusion sur la symétrie.
        "M(-t) est le symétrique de M(t) par rapport à (Oy)"
    :param intervalles: est une liste de 3 str contenant les intervalles :
        complet, pour M(t), pour son symétrique. Le premier intervalle
        n'est pas utilisé pour l'instant.
    :param p_range: donne les bornes (nombres) de l'intervalle réduit
        pour le futur tracé. Séquence de longueur 2 qui prendra le pas sur
        les paramètres donnés à :class:`PasAPas`.
    :param couleur: (optionnel) est chaîne de couleur à utiliser pour le tracé
        du morceau de courbe symétrique.
    """

    def __init__(self, transforme, sym_M, texte, parametres,
                 presentation, conclusion, intervalles,
                 p_range, couleur="#FFFFFF"):
        self.transforme = transforme
        self.sym_M = sym_M
        self.texte = texte
        self.params = parametres
        self.presentation = presentation  # Un Text
        self.conclusion = conclusion # un Text
        self.intervalles = intervalles # 3 Text : complet, moitié1, moitié2
        self.p_range = p_range
        self.couleur = couleur
    
    def anime_symetrie(self, scene):
        # scene est la scene de référence qui est une sous classe de PasAPas
        # Fait bouger un point et son symétrique entre les deux paramètres
        # passés à l'initialisation
        t1, t2 = self.params
        M = Dot(point=scene.repere.coords_to_point(*scene.courbe(t1)))
        txt_M = Tex("M(t)").next_to(M, UP/2)
        sym = Dot(point=scene.repere.coords_to_point(
            *scene.courbe(self.transforme(t1))
        ))
        txt_sym = Tex("M({})".format(self.texte)).next_to(sym, UP/2)
        GM = Group(M, txt_M)
        Gsym = Group(sym, txt_sym)
        self.groups = [GM, Gsym]
        scene.add(*self.groups)
        scene.wait(scene.INTERVALLE_LEGENDE)
        scene.play(
            GM.animate.move_to( scene.repere.coords_to_point(*scene.courbe(t2)) ),
            Gsym.animate.move_to(
                scene.repere.coords_to_point(*scene.courbe(self.transforme(t2)) )
            )
        )
        scene.wait(scene.INTERVALLE_LEGENDE)
    
    def reduit_intervalle(self, scene):
        complet, moitie1, moitie2 = self.intervalles
        t1 = Tex(f"Lorsque t parcourt {moitie1}").move_to(3*UP + 3*RIGHT).scale(0.7)
        t2 = Tex(
            "M(t) décrit une partie de la courbe."
        ).scale(0.7).next_to(t1, DOWN)
        t3 = Tex(
            f"{self.texte} parcourt alors {moitie2}"
        ).scale(0.7).next_to(t2, DOWN)
        t4 = Tex(
            f"et M({self.texte}) décrit l'autre partie"
        ).scale(0.7).next_to(t3, DOWN)
        t5 = Tex("de la courbe.").scale(0.7).next_to(t4, DOWN)
        scene.affiche_texte(t1, t2, remplace=True)
        scene.wait(scene.INTERVALLE_LEGENDE*2)
        scene.affiche_texte(t3, t4, t5, remplace=False)
        scene.wait(scene.INTERVALLE_LEGENDE*3.5)
        scene.affiche_texte(
            Tex(
                f"On étudie la courbe sur {moitie1}."
            ).move_to(3*UP + 3*RIGHT).scale(0.7))
        scene.play(*[FadeOut(g) for g in self.groups])

    
    def play(self, scene):
        """
        Présente la symétrie, anime un point et son symétrique,
        puis conclue sur la symétrie trouvée.
        """
        scene.affiche_texte(self.presentation, remplace=True)
        scene.wait(scene.INTERVALLE_LEGENDE*1.2)
        self.anime_symetrie(scene)
        scene.affiche_texte(self.conclusion, remplace=True)
        scene.wait(scene.INTERVALLE_LEGENDE*1.2)
        self.reduit_intervalle(scene)
        scene.wait(scene.INTERVALLE_LEGENDE)


class Tangente():
    """
    Tangente à une courbe paramétrée, en un paramètre donné et
    spécifiée par un vecteur directeur.
    
    :param param: la valeur du paramètre où la tangente est à placer.
    :type param: float
    :param vect: un vecteur numpy utilisé pour l'affichage et le tracé
        d'un vecteur directeur de la tangente.
    :param echelle: un facteur d'échelle pour le tracé du vecteur directeur.
    """

    def __init__(self, param, vect, echelle = 1):
        self.vect = vect * echelle
        self.vect_affiche = vect
        self.param = param
    
    def trace(self, scene, point=True, joue=True, couleur="#FFFFFF"):
        # scene est une instance de PasAPas
        
        if point:
            pt_M = Dot(
                point=scene.repere.coords_to_point(*scene.courbe(self.param)),
                color=couleur
            ).scale(0.7)
            scene.groupe_repere.add(pt_M)
            scene.add(pt_M)
        vect = Arrow(
            scene.repere.coords_to_point(*scene.courbe(self.param)),
            scene.repere.coords_to_point(*(scene.courbe(self.param)) +  self.vect),
            buff=0,
            color=couleur
        )
        scene.groupe_repere.add(vect)
        if joue:
            scene.play(FadeIn(vect))
        else:
            return FadeIn(vect)
    
    def symetrique(self, sym: Symetrie):
        """
        Calcule l'image de self par la symétrie donnée. Renvoie une Tangente
        """
        return Tangente(sym.transforme(self.param), sym.sym_M(self.vect))
        # echelle 1

class TypePoint():
    """
    Classe de base pour les points faisant l'objet d'une étude locale.
    Ces classes sont utilisées pour l'affichage.

    Quatres instances sont fournies dans ce module :
        - POINT_ORDINAIRE
        - POINT_INFLEXION
        - POINT_REBROUSSEMENT1
        - POINT_REBROUSSEMENT2
    """

    def __init__(self, p, q, etiquette):
        self.p = p
        self.q = q
        self.etiquette = etiquette
    
    def __str__(self):
        return f"p est {self.p} et q est {self.q}. Il s'agit d'un point {self.etiquette}."

POINT_ORDINAIRE = TypePoint("impair", "paire", "ordinaire")
POINT_INFLEXION = TypePoint("impair", "impair", "d'inflexion")
POINT_REBROUSSEMENT1 = TypePoint("pair", "impair", "de rebroussement de 1ère espèce")
POINT_REBROUSSEMENT2 = TypePoint("pair", "pair", "de rebroussement de 2ème espèce")


class PointSingulier():
    """
    Point faisant l'objet d'une étude locale.

    :param txt_param: une chaîne représentant la valeur du paramètre.
    :param tangente: la :class:`Tangente` à tracer
    :param p:
    :param q: les entiers déterminant le type du point
    :param type_point: le :class:`TypePoint` après étude.

    Les trois derniers arguments ne sont utilisés que pour l'affichage.
    """
    
    def __init__(self, txt_param: str, tangente: Tangente,
                 p: int, q: int, type_point: TypePoint) -> None:
        self.txt_param = txt_param
        self.tgte = tangente
        self.p = p
        self.q = q
        self.type = type_point
    
    def presente(self):
        textes = []
        if self.p > 1:
            textes.append(
                f"Le point de paramètre {self.txt_param} est singulier."
            )
            textes.append(
                "On trouve $" + tc.Frac(
                    tc.D + f"^{self.p}" + tc.Vect("OM"),
                    tc.D + f"t^{self.p}"
                    ) + f"({self.txt_param})=" + 
                tc.Matrix(
                    self.tgte.vect_affiche[:2]) +
                    "\\ne " + tc.Vect("0") + "$"
                )
        else:
            textes.append(f"Étudions le point de paramètre {self.txt_param}.")
            textes.append(
                "On trouve $" + 
                tc.Frac(tc.D + " " + tc.Vect("OM"), tc.D + "t") + 
                f"({self.txt_param})=" + 
                tc.Matrix(self.tgte.vect_affiche[:2]) +
                "\\ne " + tc.Vect("0") + "$"
            )
        textes.append(
            "De plus, $" +
            tc.Frac(
                tc.D + f"^{self.q}" + tc.Vect("OM"),
                tc.D + f"t^{self.q}"
            ) + f"({self.txt_param})$ ne lui est pas colinéaire."
        )
        textes.append(f"Au paramètre {self.txt_param}, {self.type}")
        textes.append(
            "La tangente est dirigée par $" +
            tc.Matrix(self.tgte.vect_affiche[:2]) + "$"
        )
        return textes
    
    def trace(self, scene, point=True, joue=True):
        self.tgte.trace(scene, point=point, joue=joue)


class Droite():

    def __init__(self, equation, type_ligne=Line):
        """
        Equation est un triplet (a, b, c) avec (a, b) != (0, 0).
        type_line est la classe à utiliser pour l'affichage. Line ou hérité

        La droite représentée est d'équation ax + by + c = 0 
        """
        self.equation = equation
        self.type_ligne = type_ligne
    
    def trace(self, repere: CoordinateSystem, couleur="#FFFFFF"):
        """
        Trace dans les limites du repère donné

        Retourne un objet manim Line (ou hérité) prêt à être affiché
        ou None si aucun point de la droite n'est affichable
        """
        a, b, c = self.equation
        min_x, max_x = repere.x_range[0:2]
        min_y, max_y = repere.y_range[0:2]
        # cas particulier des droites verticales
        if a == 0:
            if (-c/b) > max_y or (-c/b) < min_y:
                return None
            point1 = np.array([min_x, -c/b, 0])
            point2 = np.array([max_x, -c/b, 0])
        elif b == 0: # horizontales
            if (-c/a) > max_x or (-c/a) < min_x:
                return None
            point1 = np.array([-c/a, min_y, 0])
            point2 = np.array([-c/a, max_y, 0])
        else: # cas général
            # calcul des 4 points d'intersection avec les droites délimitant
            # notre repère affiché.
            # On doit trouver 2 points d'intersections convenables
            X_inter = [min_x, max_x, (-b*min_y - c)/a, (-b*max_y - c)/a]
            Y_inter = [(-a*min_x - c)/b, (-a*max_x - c)/b, min_y, max_y]
            convenables = [] # liste des points d'intersections dans le repère affiché
            for x, y in zip(X_inter, Y_inter):
                if (min_x <= x <= max_x) and (min_y <= y <= max_y):
                    # ce point d'intersection est affichable
                    convenables.append(np.array([x, y, 0]))
            if len(convenables) < 2:
                return None
            point1, point2 = convenables[:2]
        return self.type_ligne(
            start=repere.coords_to_point(*point1),
            end=repere.coords_to_point(*point2),
            color=couleur)


class BrancheInfinie(abc.ABC):
    """
    Classe abstraite, de base pour toutes les branches infinies.
    Donne l'interface minimale
    """

    def __init__(self, nom):
        self.nom = nom
    
    def trace(self):
        """
        Retourne un object manim à tracer ou None
        """
        return None

    def texte(self):
        return self.nom

class BrancheParabolique(BrancheInfinie):
    """
    Pour l'instant cette classe n'est pas utilisée directement pour le tracé.

    Elle peut servir de constructeur pour générer une chaîne de conclusion de
    l'étude.

    :param axe: est une chaîne de caracté décrivant l'axe de cette branche parabolique.
        "(Ox)", "(Oy)", "$D : y = \\alpha x$" sont les valeurs attentues
    """

    def __init__(self, axe):
        self.axe = axe # pour une éventuelle futur référence
        super().__init__(f"branche parabolique d'axe {axe}")
    
class Asymptote(BrancheInfinie):
    """
    :param equation: est un triplet (a, b, c) tel que l'équation de
        l'asymptote est ax + by + c = 0, XOR une paire (a, b) telle que
        l'équation est y = ax+b
    :type equation: tuple ou list
    :param couleur: est optionnel et permet de choisir la couleur de tracé
    :type couleur: str

    Les nombres passés seront utilisés pour l'affichage et le calcul.
    Utiliser fractions.Fraction si nécessaire.
    Dans certains cas, les nombres seront divisés les uns par les autres.

    L'équation sera affichée sous la forme y=ax+b ou x=c
    """

    def __init__(self, equation, couleur="#FFFFFF"):
        if len(equation) == 2:
            equation = [-equation[0], 1, -equation[1]]
        # conversion des entiers en Fraction
        a, b, c = [Fraction(e) if isinstance(e, int) else e for e in equation]
        self.droite = Droite(equation, type_ligne=DashedLine)
        if a == 0:
            eqtion = "$y={}$".format(self._converti_nombre(-c/b, ""))
            precision = " horizontale"
        elif b == 0:
            eqtion =  "$x={}$".format(self._converti_nombre(-c/a, ""))
            precision = " verticale"
        else:
            if c == 0:
                eqtion = "$y={}$".format(
                    self._converti_nombre(-a/b, "x"),
                )
            else:
                signe = "+" if -c/b > 0 else "-"
                eqtion = "$y={}{}{}$".format(
                    self._converti_nombre(-a/b, "x"),
                    signe,
                    self._converti_nombre(abs(-c/b), "")
                )
            precision = ""
        self.couleur = couleur
        super().__init__(f"asymptote{precision} d'équation {eqtion}")
    
    def _converti_nombre(self, nb, chaine):
        """
        Retourne une chaîne de caractère affichable pour représenter nb*chaine

        Cette chaine devra être dans des délimiteur de math LaTeX
        """
        signe = ""
        if nb < 0:
            signe = "-"
            nb = -nb
        if isinstance(nb, Fraction):
            if nb.numerator == 1:
                num = chaine or nb.numerator
            else:
                num = str(nb.numerator) + chaine
            if nb.denominator == 1:
                return num
            return signe + tc.Frac(num, nb.denominator)
        if nb == 1:
            return signe + (chaine or str(nb))
            # si la chaine est vide on retourne 1
        return signe + str(nb) + chaine
    
    def trace(self, repere: CoordinateSystem, couleur=None):
        """
        Trace la droite asymptote dans les limites du repère fourni.
        """
        couleur = couleur or self.couleur
        return self.droite.trace(repere, couleur=couleur)

class AsymptoteHorizontale(Asymptote):
    """
    Asymptote horizontale d'équation y = c
    """

    def __init__(self, c):
        super().__init__([0, 1, -c])

class AsymptoteVerticale(Asymptote):
    """
    Asymptote verticale d'équation x = c
    """

    def __init__(self, c):
        super().__init__([1, 0, -c])


class PasAPas(Scene):
    """
    Classe de base à sous-classer pour obtenir une vidéo.
    
    En plus des méthodes, le comportement de cette classe est donné par
    ses attributs de classe.

    Gestion du repère et du tracé
    -----------------------------

    .. py:attribute:: X_RANGE
        :type: tuple de longueur 2 ou 3
        :value: (-1.2, 1.2, 1)

        Extrémités de l'axe des abscisses, plus un pas optionnel.
    
    .. py:attribute:: Y_RANGE
        :type: tuple de longueur 2 ou 3
        :value: (-1.2, 1.2, 1)

        Extrémités de l'axe des ordonnées, plus un pas optionnel.
    
    .. py:attribute:: P_RANGE
        :type: tuple de longueur 2, ou liste de tels tuples
        :value: None

        Bornes de l'intervalle de paramètres à utiliser pour le tracé.
        Voir les discontinuités pour l'utilisation d'une liste.
    
    .. py:attribute:: DISCONTINUITES
        :type: list
        :value: None

        Liste des paramètres où la courbe n'est pas continue.
        A utiliser en lien avec :attr:`DT`
    
    .. py:attribute:: DT
        :type: float
        :value: 1e-1

        tolérance à gauche et à droite aux points de discontinuité.
            Pour gérer les discontinuité nous avons 2 choix :
            - Donner plusieurs intervalles de paramètres
            - Utiliser :attr:`DISCONTINUITES` et :attr:`DT` comme
            le fait manim de base. Ce rendu peut être non symétrique
            et l'animation peut varier en vitesse si les intervalles
            de tracé ne sont pas de même longueur.
    
    Les étapes de la construction
    -----------------------------

    Explication d'une construction de courbe
    ........................................
    L'utilisation des attributs suivants est implémenté dans la méthode
    :meth:`quelques_points`.

    .. py:attribute:: PARAMS
        :type: list
        :value: []

        Une liste de paramètres où afficher les points de la courbe,
        ainsi que les points sur les axes correspondants.
    
    .. py:attribute:: TEXTES_POINTS
        :type: list
        :value: []

        Une liste de même longueur que ::attr:`PARAMS` qui donne les
        objets manim texte à afficher comme explication à droite du repère.
    
    .. py:attribute:: LEGENDES
        :type: list
        :value: []

        Une liste de même longueur que ::attr:`PARAMS` qui contient des
        dictionnaires dont les clées sont "x", "y", "M" et donne les
        positions relatives des légendes pour les trois points placés
        pour chaque paramètre.
    
    Les propriétés de la courbe
    ...........................

    .. py:attribute:: SYMETRIES
        :type: list
        :value: []

        La liste des :py:class:`Symetrie` présentées par la courbe,
        éventuellement vide.
    
    .. py:attribute:: POINTS_REGULIERS
        :type: list
        :value: []
    
        La liste de tuple (str, :class:`Tangente`) où on veut l'étude
        des tangentes, éventuellement vide. Le premier élément
        est la chaîne représentant le paramètre.

    .. py:attribute:: POINTS_SINGULIERS
        :type: list
        :value: []

        La liste des :py:class:`PointSingulier` étudiés, éventuellement vide
    
    .. py:attribute:: ASYMPTOTES
        :type: list
        :value: []

        La liste des :py:class:`ASYMPTOTES` que possède la courbe,
        éventuellement vide.
    
    Gestion de la vidéo
    ...................

    .. py:attribute:: INTERVALLE_LEGENDE
        :type: float
        :value: 1.2

        Temps en seconde à attendre avant de poursuivre l'affichage.

    .. py:attribute:: EPISODES
        :type: bool
        :value: True

        Annonce ou non des parties de l'étude sous forme d'épisodes numérotés.
    
    .. py:attribute:: SKIP
        :type: bool
        :value: False

        Ne génére pas la partie étude de courbe, mais seulement la partie tracé.
    """

    SKIP = False # devons nous passer directement au tracé
    TEXT_DROITE = 3*(UP + RIGHT) # décalage de base du texte pour la colonne de droite
    EPISODES  = True # annonce des épisodes
    INTERVALLE_LEGENDE = 1.2 # nombre de seconde entre l'affichage d'un texte et l'affichage du prochain objet
    #spécification du repère
    X_RANGE = (-1.2, 1.2, 1)
    Y_RANGE = (-1.2, 1.2, 1)
    X_LENGTH = 6
    Y_LENGTH = 6
    # les paramètres qui seront passés à la fonction quelques_points.
    # mettre des listes vides pour supprimer ce passage
    PARAMS = [] # valeurs du paramètre
    LEGENDES = [] #positions des légendes pour les points
    TEXTES_POINTS = [] # textes affichés en haut
    # présentation des symétries
    SYMETRIES = [] # Une liste de Symetrie
    POINTS_REGULIERS = [] # Une liste de
    # (txt_parametre : str, Tangente)
    # le vecteur numpy est utilisé pour l'affichage d'un texte,
    # puis mis à l'échelle pour afficher la flèche
    POINTS_SINGULIERS = [] # Une liste de PointSingulier
    ASYMPOTES = [] # une liste d'Asymptote
    # les 3 paramètre suivants controlent le tracé si aucune symétrie n'est présente.
    P_RANGE = None # bornes (2-uple) de l'intervalle de tracé ou listes de bornes
    # Une troisième élément optionnel est une couleur de tracé
    DISCONTINUITES = None # liste des paramètres où la fonction n'est pas continue
    DT = 1e-1 # tolérance à gauche et à droite aux points de discontinuité
    # Pour gérer les discontinuité nous avons 2 choix : 
    # - Donner plusieurs intervalles de paramètres
    # - Utiliser DISCONTINUITES et DT comme le fait manim de base. Ce rendu peut être
    # non symétrique et l'animation peut varier en vitesse si les intervalles de tracé
    # ne sont pas de même longueur
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textes_courrants = []
        self.groupe_repere = Group()
        self.repere_affiche = False
        self._num_episode = 0
    
    def x(self, t):
        """
        Fonction abscisse.
        """
        return 

    def y(self, t):
        """
        Fonction ordonnée.
        """
        return 

    def courbe(self, t):
        return np.array([
            self.x(t),
            self.y(t),
            t-t,
        ])

    def efface_textes(self):
        """
        Efface tous les textes courrants.
        """
        # une animation pour tout effacer
        if self.textes_courrants:
            self.play(*[FadeOut(txt) for txt in self.textes_courrants])
        self.textes_courrants = []
    
    def affiche_texte(self, *textes, remplace=True):
        """
        Affiche les textes passés en arguments. Attention à positionner les
        textes au préalable.

        :param remplace: si True (par défaut), commence par effacer les
            textes déjà présents
        """
        if remplace:
            self.efface_textes()
            self.textes_courrants = list(textes)
        else:
            self.textes_courrants.extend(textes)
        # affichage de tous les nouveaux textes
        self.play(*[FadeIn(txt) for txt in textes])
    
    def cache_repere(self, joue=True):
        """
        Cache le repère et la construction courrante.

        :param joue: si True, joue l'animation, sinon retourne l'animation
            prête à être jouée.
        """
        if self.repere_affiche:
            self.repere_affiche = False
            if joue:
                self.play(FadeOut(self.groupe_repere))
            else:
                return FadeOut(self.groupe_repere)
    
    def affiche_repere(self, joue=True):
        """
        Affiche le repère et la construction courrante.

        :param joue: si True, joue l'animation, sinon retourne l'animation
            prête à être jouée.
        """
        if not self.repere_affiche:
            self.repere_affiche = True
            if joue:
                self.play(FadeIn(self.groupe_repere))
            else:
                return FadeIn(self.groupe_repere)
    
    def annonce_episode(self, titre, repere_fin=True):
        """
        Annonce une séquence de la vidéo par un numéro + titre en plein écran.

        Efface tous les textes courrants.

        :param titre: le titre de l'épisode
        :param repere_fin: si vrai, affiche le repère à la fin de l'annonce.
        """
        numero = self._num_episode
        logger.info(f"Épisode {numero}")
        self.efface_textes()
        self.cache_repere()
        num = Tex(f"Épisode {numero}").move_to(UP)
        titre_txt = Tex(titre).next_to(num, DOWN)
        self.play(FadeIn(num), FadeIn(titre_txt))
        self.wait(self.INTERVALLE_LEGENDE)
        if repere_fin and not self.repere_affiche:
            self.play(
                FadeOut(num),
                FadeOut(titre_txt),
                self.affiche_repere(joue=False)
            )
        else:
            self.play(FadeOut(num), FadeOut(titre_txt))
        self._num_episode += 1

    
    def intro(self):
        self.affiche_texte(Text("Étude et tracé d'une courbe paramétrée"))
        self.wait(self.INTERVALLE_LEGENDE)
        self.efface_textes()

    def quelques_points(self, parametres: list, legendes, textes=None):
        """
        Prend en argument :
        une liste de paramètres des points à placer,
        une liste de dictionnaires donnant les positions relatives des légendes : 
        {'x': , 'y': , 'M': }
        une liste optionnelle de textes à afficher avant de placer chaque point
        """
        if textes is not None and len(parametres) != len(textes):
            raise ValueError(
                "Le nombre de points à placer ne correspond pas au nombre de légendes"
            )
        warn_gpe = None
        if len(parametres) > 0:
            warn_txt = Text(
                "Remarquer que la valeur du"
            ).move_to(4*RIGHT + UP).scale(0.5)
            warn_gpe = Group(
                warn_txt,
                Text(
                    "paramètre n'apparaît pas"
                ).next_to(warn_txt, DOWN*0.25).scale(0.5),
                Text(
                    "directement sur le tracé."
                ).next_to(warn_txt, DOWN*2.5).scale(0.5)
            )
            self.play(FadeIn(warn_gpe))
            for i, t in enumerate(parametres):
                if textes is not None:
                    txt = textes[i]
                    self.affiche_texte(txt)
                    self.wait(self.INTERVALLE_LEGENDE)
                if i == 0:
                    px = Dot(point=self.repere.coords_to_point(self.x(t), 0, 0))
                    txt_x = Text(f"x({t})").next_to(px, legendes[i]["x"]).scale(0.5)
                    py = Dot(point=self.repere.coords_to_point(0, self.y(t), 0))
                    txt_y = Text(f"y({t})").next_to(py, legendes[i]["y"]).scale(0.5)
                    pM = Dot(point=self.repere.coords_to_point(*self.courbe(t)))
                    txt_M = Text(f"M({t})").next_to(pM, legendes[i]["M"]).scale(0.7)
                    self.add(px, py, pM)
                    self.add(txt_x, txt_y, txt_M)
                else:
                    self.play(FadeOut(txt_x), FadeOut(txt_y), FadeOut(txt_M))
                    self.play(
                        px.animate.move_to(
                            self.repere.coords_to_point(self.x(t), 0, 0)
                        ),
                        py.animate.move_to(
                            self.repere.coords_to_point(0, self.y(t), 0)
                        ),
                        pM.animate.move_to(
                            self.repere.coords_to_point(*self.courbe(t))
                        )
                    )
                    txt_x = Text(f"x({t})").next_to(px, legendes[i]["x"]).scale(0.5)
                    txt_y = Text(f"y({t})").next_to(py, legendes[i]["y"]).scale(0.5)
                    txt_M = Text(f"M({t})").next_to(pM, legendes[i]["M"]).scale(0.7)
                    self.add(txt_x, txt_y, txt_M)
                self.wait(self.INTERVALLE_LEGENDE)
            self.wait(self.INTERVALLE_LEGENDE)
            self.remove(px, py, pM, txt_x, txt_y, txt_M)
            if textes is not None:
                self.play(FadeOut(warn_gpe), FadeOut(txt))
                # méchant hack. il ne devrait pas y avoir d'autres textes
                self.textes_courrants = []
            else:
                self.play(FadeOut(warn_gpe))
    
    def place_repere(self):
        """
        Construction et affichage du repère.
        """
        self.repere = Axes(
            # x_min, x_max, pas
            x_range=self.X_RANGE,
            y_range=self.Y_RANGE,
            x_length=self.X_LENGTH,
            y_length=self.Y_LENGTH,
            axis_config = {
                "tip_width": 0.2,
                "tip_height": 0.2,
                "stroke_opacity": 1
            }
        )
        self.play(FadeIn(self.repere))
        self.repere_affiche = True
        self.groupe_repere.add(self.repere)
        self.play(self.repere.animate.move_to(3*LEFT))
    
    def annonce_courbe(self):
        """
        Annonce de la courbe à tracer.

        Utiliser de préférence pas méthode affiche_texte
        """
        return
    
    def symetries(self):
        """
        Présentation des symétries de la courbe
        """
        self.affiche_repere()
        for sym in self.SYMETRIES:
            sym.play(self)
    
    def tableau_variations(self):
        """
        Trace éventuellement un tableau de variations (avec ou sans texte). Fait
        en plein écran.

        Pour l'annoncer par un épisode, utiliser self.annonce_episode
        """
        return 
    
    def points_reguliers(self):
        if len(self.POINTS_REGULIERS) > 0:
            self.cache_repere()
            txt1 = Tex(
                "S'il est non nul, le vecteur $\\frac{\\text{d}\\overrightarrow{OM}}{\\text{d}t}(t_0)$"
            ).move_to(UP*3)
            txt2 = Tex("dirige la tangente à l'instant $t_0$.").next_to(txt1, DOWN)
            txt3 = Tex(
                "Il s'agit du vecteur vitesse instantanée."
            ).next_to(txt2, DOWN)
            self.affiche_texte(txt1, txt2)
            self.wait(self.INTERVALLE_LEGENDE)
            self.affiche_texte(txt3, remplace=False)
            self.wait(self.INTERVALLE_LEGENDE*2)
            self.efface_textes()
            self.affiche_repere()
        for txt_t0, tgte in self.POINTS_REGULIERS:
            # trace la tangente en M(t0), dirigée par v
            t0 = tgte.param
            pt_M = Dot(
                point=self.repere.coords_to_point(*self.courbe(t0))
            ).scale(0.7)
            txt_M = Tex(f"M({txt_t0})").next_to(pt_M, UP/2).scale(0.5)
            self.groupe_repere.add(pt_M)
            self.play(FadeIn(pt_M))
            self.play(FadeIn(txt_M))
            lgd = Tex(
                f"Au paramètre {txt_t0}, la tangente"
            ).move_to(self.TEXT_DROITE).scale(0.7)
            self.affiche_texte(
                lgd,
                Tex(
                    f"est dirigée par ${tc.Matrix(tgte.vect_affiche[:2])}$"
                ).next_to(lgd, DOWN).scale(0.7)
            )
            self.wait(self.INTERVALLE_LEGENDE)
            self.play(FadeOut(txt_M), tgte.trace(self, joue=False, point=False))
            self.wait(self.INTERVALLE_LEGENDE*0.7)
            self.efface_textes()
    
    def points_singuliers(self):
        self.cache_repere()
        for i, ps in enumerate(self.POINTS_SINGULIERS):
            textes = ps.presente()
            txt_courrant = Tex(textes[0]).move_to(UP*3)
            self.affiche_texte(txt_courrant)
            self.wait(self.INTERVALLE_LEGENDE*1.5)
            for t in textes[1:]:
                txt_courrant = Tex(t).next_to(txt_courrant, DOWN)
                self.affiche_texte(txt_courrant, remplace=False)
                self.wait(self.INTERVALLE_LEGENDE*1.5)
            self.wait(self.INTERVALLE_LEGENDE)
            self.efface_textes()
            self.affiche_repere()
            ps.trace(self, point=True, joue=True)
            self.wait(self.INTERVALLE_LEGENDE)
            if i < len(self.POINTS_SINGULIERS) - 1:
                self.cache_repere()

    def asymptotes(self):
        """
        Trace les éventuelles asymptotes.

        Pour montrer une étude de branche infinie, surcharger la méthode puis
        finir par un appel a super().asymptotes()
        """
        txt = Text("En image").move_to(self.TEXT_DROITE + UP).scale(0.5)
        self.affiche_repere()
        for i, asymp in enumerate(self.ASYMPOTES):
            ligne = asymp.trace(self.repere)
            if i == 0:
                debut = "Traçons"
            else:
                debut = "puis"
            if i == len(self.ASYMPOTES) - 1:
                fin = "."
            else:
                fin = ","
            txt = Tex(f"{debut} l'{asymp.nom}{fin}").next_to(txt, DOWN).scale(0.7)
            self.affiche_texte(txt, remplace=False)
            self.wait(self.INTERVALLE_LEGENDE)
            self.groupe_repere.add(ligne)
            self.play(FadeIn(ligne))
            self.wait(self.INTERVALLE_LEGENDE)
        self.wait(self.INTERVALLE_LEGENDE)

    def variations(self):
        """
        A surcharger. Rappel ou annonce des variations dans la colonne de droite
        juste avant le tracé.
        """
        return

    def _trace_morceau(self, p_range, transforme=lambda t: t, couleur="#FFFFFF"):
        if len(p_range) == 3: # couleur fournie dans l'intervalle
            # celle-ci prend le pas sur l'argument optionnel.
            couleur = p_range[2]
            p_range = p_range[:2]
        courbe = ParametricFunction(
            lambda t: self.repere.coords_to_point(*self.courbe(transforme(t))),
            t_range=p_range,
            use_vectorized=False,
            discontinuities=self.DISCONTINUITES,
            dt = self.DT,
            color=couleur
        )
        self.play(Create(courbe, run_time=2))
        self.groupe_repere.add(courbe)
        self.wait(self.INTERVALLE_LEGENDE)

    def trace_complet(self):
        txt_courrant = Tex(
            "On obtient finalement le tracé"
        ).move_to(self.TEXT_DROITE).scale(0.7)
        self.affiche_texte(txt_courrant)
        self.wait(self.INTERVALLE_LEGENDE)
        if len(self.SYMETRIES) == 0:
            if isinstance(self.P_RANGE[0], collections.abc.Sequence):
                # on a donné une liste d'intervalles
                for p_range in self.P_RANGE:
                    self._trace_morceau(p_range)
            else:
                self._trace_morceau(self.P_RANGE)
        else:
            tangentes_supp = [(None, ps.tgte) for ps in self.POINTS_SINGULIERS]
            # tangentes placées par symétrie, dont il faut caluler
            # des autres symétriques éventuels.
            for i, sym in enumerate(reversed(self.SYMETRIES)):
                if i == 0:
                    txt_courrant = Tex(
                        f"d'abord sur l'intervalle {sym.intervalles[1]},"
                    ).scale(0.7).next_to(txt_courrant, DOWN)
                    self.affiche_texte(txt_courrant, remplace=False)
                    self._trace_morceau(sym.p_range)
                fin = "," if i < len(self.SYMETRIES) else "."
                txt_courrant = Tex(
                    f"puis sur {sym.intervalles[0]} en traçant les M({sym.texte})" + fin,
                    color=sym.couleur
                ).scale(0.7).next_to(txt_courrant, DOWN)
                self.affiche_texte(txt_courrant, remplace=False)
                # tangentes symétriques
                tgtes = []
                for _ , tgte in self.POINTS_REGULIERS + tangentes_supp:
                    # trace la tangente en M(t0), dirigée par v
                    tgte_sym = tgte.symetrique(sym)
                    tgte_sym.trace(self, couleur=sym.couleur)
                    tgtes.append([None, tgte_sym])
                tangentes_supp.extend(tgtes)
                
                self._trace_morceau(
                    sym.p_range,
                    transforme=sym.transforme,
                    couleur=sym.couleur
                )
        self.wait(2*self.INTERVALLE_LEGENDE)
        self.efface_textes()
        self.play(*[e.animate.shift(RIGHT*3) for e in self.groupe_repere])
        self.play(*[e.animate.scale(1.2, about_point=self.repere.c2p(0,0,0)) for e in self.groupe_repere])
        self.wait(2*self.INTERVALLE_LEGENDE)
    
    def construct(self):
        """
        Enchaîne les appels à toutes les méthodes précédentes.

        Si `self.SKIP` est vrai, se contente de tracer la courbe
        """
        if not self.SKIP:
            self.next_section("Intro")
            self.intro()
            self.next_section("Quelques points")
            if len(self.PARAMS) > 0:
                self.annonce_episode("Placer un point d'une courbe", repere_fin=False)
                self.place_repere()
                self.quelques_points(
                    self.PARAMS,
                    self.LEGENDES,
                    self.TEXTES_POINTS
                )
            else:
                self._num_episode = 1
            self.next_section("Annonce courbe")
            logger.info("Repère : {}".format(self.repere_affiche) )
            self.annonce_episode(
                "La courbe à étudier", repere_fin=len(self.PARAMS) != 0
            )
            logger.info("Repère : {}".format(self.repere_affiche) )
            self.wait(self.INTERVALLE_LEGENDE)
            self.efface_textes()
            if len(self.PARAMS) == 0:
                self.place_repere()
            self.annonce_courbe()
            self.wait(2*self.INTERVALLE_LEGENDE)
            logger.info("Repère : {}".format(self.repere_affiche) )
            self.next_section("Symetries")
            self.symetries()
            self.wait(self.INTERVALLE_LEGENDE)
            self.tableau_variations()
            if len(self.POINTS_REGULIERS) > 0:
                self.annonce_episode(
                    "Étude de quelques points réguliers",
                    repere_fin=False
                )
            self.next_section("Points reguliers")
            self.points_reguliers()
            if len(self.POINTS_SINGULIERS) > 0:
                pluriel = "s" if len(self.POINTS_SINGULIERS) > 1 else ""
                self.annonce_episode(f"Étude locale{pluriel}", repere_fin=False)
            self.next_section("Points singuliers")
            self.points_singuliers()
            if len(self.ASYMPOTES) > 0:
                pluriel = "s" if len(self.ASYMPOTES) > 1 else ""
                self.annonce_episode(
                    f"Étude de{pluriel} branche{pluriel} infinie{pluriel}",
                    repere_fin=False
                )
            self.next_section("Asymptotes")
            self.asymptotes()
            self.annonce_episode("Tracé")
            self.next_section("(Rappels) variations")
            self.variations()
            self.next_section("Tracé")
        else:
            self.place_repere()
            self.play(self.repere.animate.move_to(3*LEFT))
        self.trace_complet()
