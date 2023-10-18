==================
Exemples commentés
==================

.. contents:: Table des matières
   :depth: 2

Une courbe régulières
=====================

Examinons l'exemple de :class:`lissajous.Lissajous`.

On utilise :
    - des exemples de tracé de points
    - des symétries
    - des tangentes aux points réguliers

On surcharge les méthodes :
    - :meth:`intro` pour annoncer `quelques_points`
    - :meth:`annonce_courbe` et :meth:`variations` comme dans le contrat

Les paramètres utilisés pour le tracé final sont déterminés par les symétries données.
    - l'ordre des symétries est important, on les liste dans le code dans l'odre où on les trouve.
    - l'intervalle `p_range` passé en argument de :class:`Symetrie` est utilisé pour le tracé seulement pour la dernière symétrie, le reste du tracé est déduit en transformant les `p_range` par l'argument `transforme`.

.. literalinclude:: ../lissajous.py
    :language: python

Le résultat en image

.. raw:: html

    <center><video controls=""
    preload="metadata"
    poster="https://prepa.blaise-pascal.fr/media/images/23-24/math/lissajous_coupe.png">
    <source src="https://prepa.blaise-pascal.fr/media/videos/23-24/Lissajous.mp4" type="video/mp4">
    <source src="https://prepa.blaise-pascal.fr/media/videos/23-24/Lissajous.webm" type="video/webm">
    <p>Votre navigateur ne permet pas la lecture de vidéo.Mais vous pouvez
    <a href="https://prepa.blaise-pascal.fr/media/videos/23-24/Lissajous.mp4">télécharger</a> celle ci.
    </p></video></center>

Des points singuliers
=====================


En plus de l'introduction des points singuliers, on utilise ici 
un module :doc:`d'utilitaires LaTeX <tex_commands>` : :mod:`tex_commands.py`

La courbe exemple est une astroïde. Le code donné ci dessous omet les symétries.

.. literalinclude:: ../astroide.py
    :language: python
    :lines: 1-11,53-

qui nous donne

.. raw:: html

    <center><video controls=""
    preload="metadata"
    poster="https://prepa.blaise-pascal.fr/media/images/23-24/math/Astroide_coupe.png">
    <source src="https://prepa.blaise-pascal.fr/media/videos/23-24/Astroide.mp4" type="video/mp4">
    <source src="https://prepa.blaise-pascal.fr/media/videos/23-24/Astroide.webm" type="video/webm">
    <p>Votre navigateur ne permet pas la lecture de vidéo. Mais vous pouvez
    <a href="https://prepa.blaise-pascal.fr/media/videos/23-24/Astroide.mp4">télécharger</a> celle ci.
    </p></video></center>


Des asymptotes et un tableau de variations
==========================================

On utilise cette fois pleinement le module :mod:`tex_commands.py` pour le tracé d'un
tableau de variations (dont le code est dans un fichier annexe). Pour cet exemple,
on utilise le packages `variations` de LaTeX qui est ajouté au préambule par l'Utilisation
de la classe :class:`VTex`.

Cette fois, les paramètres utilisés pour le tracé sont donné dans l'attribut :attr:`P_RANGE`,
sous forme d'une liste d'intervalle pour gérer les discontinuités.

.. literalinclude:: ../bi_exemple.py
    :language: python

.. raw:: html

    <center><video controls=""
    preload="metadata"
    poster="https://prepa.blaise-pascal.fr/media/images/23-24/math/BranchesInfiniesExemple_coupe.png">
    <source src="https://prepa.blaise-pascal.fr/media/videos/23-24/BranchesInfiniesExemple.mp4" type="video/mp4">
    <source src="https://prepa.blaise-pascal.fr/media/videos/23-24/BranchesInfiniesExemple.webm" type="video/webm">
    <p>Votre navigateur ne permet pas la lecture de vidéo. Mais vous pouvez
    <a href="https://prepa.blaise-pascal.fr/media/videos/23-24/BranchesInfiniesExemple.mp4">télécharger</a> celle ci.
    </p></video></center>