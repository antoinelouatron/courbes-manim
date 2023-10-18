.. Courbes paramétrées en manim documentation master file, created by
   sphinx-quickstart on Fri Oct 13 07:30:41 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============================================
Construction de courbes paramétrées avec manim.
===============================================

.. contents:: Table des matières
   :depth: 2

Pré-requis
==========

    - Utiliser python version 3.7 ou supérieur (ce module a été écrit en utilisant python 3.11)
    - Installer manim_

.. _manim: https://docs.manim.community/en/stable/installation.html


Utilisation minimale
====================

Il suffit de créer une classe héritant de :class:`PasAPas` et surcharger quelques attributs
de classe et queslques méthodes pour obtenir un premier tracé.

Les attributs principaux sont :
    - :py:attr:`X_RANGE` tuple de longueur 2 qui donne les extrémités de l'axe (Ox)
    - :attr:`Y_RANGE` tuple de longueur 2 qui donne les extrémités de l'axe (Ox)
    - :attr:`P_RANGE` tuple de longueur 2 qui donne l'intervalle de paramètres à utiliser pour le tracé

Les trois méthodes à surcharger, au minimum:
    - :meth:`x` qui prend un paramètre comme argument et retourne l'abscisse
    - :meth:`y` idem pour l'ordonnée
    - :meth:`annonce_courbe` qui affiche un texte de présentation de la courbe à étudier

Pour tracer le cercle unité on pourrait donc définir::

   import numpy as np
   from manim import *
   from construction_courbe import PasAPas

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
         

Il suffit ensuite de lance la commande (en supposant que le fichier python soit `cercle.py`)

   manim -pql cercle.py

qui va créer une vidéo et la lancer dans le programme par défaut.


Les étapes de la construction
=============================

Voir :doc:`la documentation <construction_courbe>` de :class:`PasAPas` pour les détails sur chaque classe.

L'ordre des méthodes
--------------------

Pour construire la vidéo complète, une instance de :class:`PasAPas` va appeler ses méthodes dans l'ordre suivant.

   - :meth:`intro`
   - :meth:`quelques_points` si :attr:`PARAMS` est non vide
   - :meth:`annonce_courbe` qu'il faut surcharger
   - :meth:`symetries` si des :class:`Symetrie` sont données
   - :meth:`tableau_variations` qu'on peut surcharger
   - :meth:`points_reguliers` si :attr:`POINT_REGULIERS` est non vide
   - :meth:`points_singuliers` si :attr:`POINT_SINGULIERS` est non vide
   - :meth:`variations` qu'il faut surcharger
   - :meth:`trace_complet`


Des exemples
------------

   - Voir les sources de :class:`lissajous.Lissajous` pour un exemple utilisant des symétries et des points réguliers.
   - Voir les sources de :class:`astroide.Astroide` pour un exemple utilisant en plus des points singuliers.
   - Voir les sources de :class:`bi_exemple.BranchesInfiniesExemple` pour un exemple de fonction discontinue ayant des asymptotes, et un tableau de variations.


.. toctree::
    :maxdepth: 1

    exemples
    modules

Index et références
===================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
