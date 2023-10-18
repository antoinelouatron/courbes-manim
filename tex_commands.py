"""
Les classes de ce modules sont quelques utilitaires pour afficher plus facilement
du LaTeX avec manim.


La première classe est MyTex qui premet d'ajouter facilement des packages pour la
compilation et de choisir le compilateur latex a utiliser (lualatex par défaut).

Viennent ensuite les classes Command et Env qui permettent de créer des fonctions
retournant les commandes ou environnements voulus.

Matrix est un raccourci pratique pour Env("pmatrix"). La fonction Matrix prend 
une liste ou une liste de liste comme argument.

Les commandes déjà créées pour l'instant sont :
    - `Frac` : comme en latex, mais avec un majuscule :)
    - `Vect` : ajoute une flèche au dessus de son argument
    - `Tend` : fonction à 2 paramètres retournant \\underset{#1 \\to #2}{\\to}

D est un raccourci pour \\text{d}. Utile pour les notations physique de dérivation.
"""

import typing

import manim
from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL
import numpy as np

class ExtendPackageMetaclass(ConvertToOpenGL): # TODO metaclass conflict
    """
    Metaclass pour les classes définissant un attribut de classe "packages".

    Les classes filles peuvent ajouter de nouveaux packages à charger dans le préambule de
    chaque compilation latex.

    Pour toute utilisation, hériter de MyTex ou définir les attributs de classe
    - tex_compiler
    - package_command
    """

    def __new__(cls, name, bases, dictionary):
        # récupération des packages définis dans les classes parents
        # L'ordre d'apparition sera le même que l'ordre d'héritage
        packages_herites = {}
        for base in bases:
            packages_herites.update(getattr(base, "packages", {}))

        nouveaux_packages = dictionary.get("packages", {})
        # on converti les packages donnés en dictionnaires qui conservent l'ordre
        # mais préservent l'unicité
        if isinstance(nouveaux_packages, list):
            nouveaux_packages = {e: True for e in nouveaux_packages}
        packages_herites.update(nouveaux_packages)
        dictionary["packages"] = packages_herites

        nouvelle_cls = super().__new__(cls, name, bases, dictionary)
        L = [r"\{}{}".format(nouvelle_cls.package_command, pack) for pack in packages_herites]
        preamble = "".join(L)
        template = manim.TexTemplate(
            tex_compiler=nouvelle_cls.tex_compiler,
            preamble=preamble
        )
        nouvelle_cls.template = template
        return nouvelle_cls

class MyTex(manim.Tex, metaclass=ExtendPackageMetaclass):
    """
    Classe de base pour importer d'autres packages lors de la compilation latex.

    Les classes filles peuvent surcharger les attributs de classe:
        - tex_compiler : la commande latex à invoquer
        - package_command : usepackage ou RequirePackage suivant les goûts
        - packages : l'utilisation est plus délicates. Les packages de base sont
            babel (en français), amsmath et amssymb.
    
    Si une classe fille surcharge cet attribut
    les packages seront ajoutés à cette liste, dans l'ordre d'ajout
    """

    packages = [
        "[french]{babel}",
        "{amsmath}",
        "{amssymb}"
    ]
    tex_compiler = "lualatex"
    package_command = "usepackage"

    def __init__(self,*args, **kwargs):
        super().__init__(*args, tex_template=self.template, **kwargs)

class Command():
    """
    Crée une fonction prennant une nombre arbitraire d'arguments er retournant la
    chaine "\\name{arg1}{arg2}..."
    """

    def __init__(self, nom: str):
        self.nom = nom # nom de la commande
    
    def __call__(self, *args) -> str:
        base = f"\\{self.nom}"
        buff = [base]
        for arg in args:
            buff.append("{" + str(arg) + "}")
        return "".join(buff)

class Env():
    """
    Crée une fonction dont le nom est donné à l'initialisation de l'instance
    et qui prend comme argument le contenu d'un environnement.

    Cette fonction ajoute begin/end autour du contenu qui doit être une chaîne.
    """

    def __init__(self, nom: str):
        self.nom = nom # nom de la commande
    
    def __call__(self, contenu) -> str:
        debut = f"\\begin{{{self.nom}}}"
        fin = f"\\end{{{self.nom}}}"
        buff = [debut, contenu, fin]
        return "".join(buff)

# direction par défaut pour une matrice donnée par une seule liste
COL = 0
LIGNE = 10

def Matrix(data: typing.Union[np.array, list], direction: int=COL) -> str:
    """
    :param data: Si une liste simple est donnée, elle sera interprété comme 
        une ligne ou une colonne suivant la valeur de
    :param direction: la direction pour interpréter une liste simple.
        peut prendre les valeurs COL ou LIGNE 
    """
    np_data = np.array(data)
    s = np_data.shape
    if len(s) == 1 :
        if direction == COL:
        # conversion en matrice colonne
            data = [[e] for e in data]
        else:
            data = [data]
    lignes = [" & ".join(str(e) for e in ligne) for ligne in data]
    return "\\begin{pmatrix}" + "\\\\".join(lignes) + "\\end{pmatrix}"


Frac = Command("frac")
Vect = Command("overrightarrow")
#préparation de Tend
_Tend = Command("underset")
def Tend(var, lim):
    return _Tend(f"{var} \\to {lim}", "\\to")
# D est une chaîne constante
D = Command("text")("d")


