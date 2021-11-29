Proposition de solution
=======================

Contexte
--------

En début de nuit, une réflexion sur un ton exaspéré d'un participant insinuant
que le sujet était trop difficile nous a interloqué. Voyant que d'autres équipes
étaient encore en galère à une heure où nous pensions que la plupart des
participants plancheraient sur la partie créative, nous avons décidé de réaliser
notre propre sujet à partir d'une complète page blanche pour voir s'il y avait
un écueil que nous n'avions pas vu.

En approximativement 1h30 (en programmation en binôme) répartis en 3 phases
(environ 40 minutes pour la saison 1, 20 minutes pour la saison 2, 30 minutes
pour la saison 3 simpliste mais fonctionnelle) incluant le temps passé à
répondre aux questions et attendre l'accès à la structure pour les
vérifications, cela a donné le code suivant:

https://github.com/haum/24hc21/tree/main/on_vous_poutre_tous

Le langage choisi est python, car les deux codeurs impliqués le maîtrisent et
une bibliothèque est disponible pour le protocole SACN. Il est découpé en un
fichier ``controllers.py`` qui réunit les abstractions et des fichiers de script
qui utilisent ce module pour rejouer à souhait les scénarii déjà réalisés.

Abstractions de la saison 1
---------------------------

LedController
'''''''''''''

La première difficulté est la séparation des canaux des leds entre deux univers.
Il serait plus commode d'avoir un seul tableau à considérer, c'est pourquoi nous
créons une abstraction ``LedController``.

Cette classe contient une liste des valeurs ``self.chans``. Par commodité (il
serait préférable de séparer dans un vrai projet, mais pour les 24h optons pour
l'efficacité du prototypage) l'initialisation de la bibliothèque SACN est
réalisée dans le constructeur de la classe, en copiant directement l'exemple de
sa documentation (à part le ``source_name`` pour lequel un peu de lecture a été
nécessaire).

La liste de valeurs peut être remplie avec la fonction ``fill`` qui prend une
liste de trois éléments en paramètre (par défaut [0, 0, 0]) et remplit la liste
avec cette valeur en boucle.

.. note::

   Nous utilisons la multiplication d'une liste par un entier qui, en python,
   continue la liste en la répétant. Le même effet peut être obtenu avec une
   boucle dans d'autres langages. 

   .. code-block::

        In [1]: a = [1, 2, 3]
        In [2]: a*3
        Out[2]: [1, 2, 3, 1, 2, 3, 1, 2, 3]

Il est aussi possible de modifier les trois canaux d'une led en particulier avec
l'opérateur "crochets".

.. note::

   En python, il est possible de définir l'opérateur "crochets" sur une classe
   en définissant la fonction ``__setitem__(self, k, v)`` où ``k`` contiendra la
   valeur passée entre crochets et ``v`` la valeur à affecter. Une fonction
   classique aurait pu être utilisée, toutefois cet opérateur rend le code assez
   naturel à la lecture (e.g. ``leds[3] = [255, 0, 0]``).

   Ici, nous utilisons aussi l'opérateur "crochets" de la liste qui accepte un
   intervalle pour remplacer une partie de ses éléments. Nous aurions aussi pu
   utiliser trois instructions ou une boucle dans un langage qui ne gère pas
   cette fonctionnalité.

   .. code-block::

        In [1]: b = [1, 2, 3, 4, 5, 6]
        In [2]: b[3:6] = [0]*3
        In [3]: b
        Out[3]: [1, 2, 3, 0, 0, 0]

Enfin, une fonction ``blit`` permet de transformer notre représentation commode
dans le formaliste de la bibliothèque qui va se charger d'envoyer les valeurs.
Il s'agit simplement ici de copier une partie du tableau dans le tableau de
l'univers 1 et l'autre partie dans celui de l'univers 2, ce qui est fait avec
une indexation par intervalles mais pourrait être fait avec une boucle ou une
fonction de copie dans des langages n'ayant pas cette expressivité.

Une fonction ``stop`` permet de remettre les canaux à zéro et arrêter le thread
d'envoi de la bibliothèque SACN.

.. important::

   Notez que dès maintenant, l'abstraction nous permet de ne plus nous soucier
   du fonctionnement en univers et que nous n'aurons plus à interagir qu'avec
   notre propre code pour réaliser la suite de la saison.

   L'abstraction permet de passer des termes du problème aux termes de la
   solution (même si le vocabulaire est pour le moment encore à enrichir).

   En codant dans les termes de la solution, il sera plus aisé d'obtenir une
   solution, là où rester dans les termes du problème nous mène plus
   naturellement aux problèmes.

TalController
'''''''''''''

Contrôler les leds, c'est bien, mais avoir une abstraction au niveau des tåls
serait plus pratique. Nous réalisons donc une abstraction minimaliste qui
contient un ``LedController`` et triple la couleur modifiée en ajustant les bons
indices de leds.

Là nous attendons un créneau pour vérifier notre abstraction. Avec python, le
test est rapide puisque nous pouvons lancer le shell interactif, importer notre
module, instancier un objet de la classe et appeler ses méthodes simplement. Un
script de test aurait été une alternative légèrement moins commode.

CubeController
''''''''''''''

Un meilleur vocabulaire pour interagir avec la structure serait de pouvoir
indexer les tåls selon leur position spatiale (x, y, z ou x, y, tranche selon le
choix de chacun).

Initialement, les équipes devaient relever la position des tåls sur la structure.
Il fallait pour cela par exemple allumer les leds une à une dans l'ordre pour
voir comment elles étaient réparties. Nous pouvions alors voir que les leds
étaient chaînées en suivant les descentes de câble, d'abord au centre, puis en
suivant un motif en spirale sur les six branches soutenant le système. Il était
alors possible d'associer numéros et positions.

Remarquant cette construction, il serait possible de définir une formule.
Néanmoins, dans un souci d'efficacité en 24h, une simple LUT (look-up table /
table d'association) est plus simple et peut être plus facilement déverminée.
Cette table a d'ailleurs été publiée sur le site du sujet en début de soirée.
(Certaines équipes avaient réussi cette étape seuls avant la publication.)

Nous avons repris cette table dans la documentation en copiant-collant depuis le
navigateur, et en la formatant en une liste plate à coup d'expressions
régulières (l'avantage de maîtriser ses outils, ici l'éditeur vim). Avec la
bibliothèque ``numpy``, la transformation d'une liste plate en matrice 4×4×4 est
immédiat, mais une fonction d'accès codée manuellement n'est pas beaucoup plus
compliquée. Il aurait aussi été possible d'enregistrer la table sous la forme
d'un tableau de tableau de tableau.

Dès lors, il suffit de passer la valeur de cette matrice en indice de
l'abstraction précédente pour arriver à nos fins, ou plutôt après lui avoir
retiré une unité, car le tableau de la documentation commence à 1 là où notre
code indexe en partant de 0.

Au passage, nous ajoutons un attribut ``autoblit`` permettant de ne pas oublier
d'appeler la fonction ``blit`` et ajoutons des fonctions qui renvoient vers
celles des classes membres (une version plus propre serait à envisager dans un
contexte d'un vrai projet).

Saison 1
--------

Avec ces abstractions, les épisodes de la saison 1 sont rapides à exécuter.

Épisode 1
'''''''''

On initialise notre abstraction, on allume un tål, on attend, on éteint ce tål,
on attend, on boucle. Gagné.

Épisode 2
'''''''''

L'astuce consiste à remarquer que les couleurs sont les mêmes lorsqu'on se
déplace d'un vecteur ``(1, 1, 1)``. Dès lors, il suffit de décrire chaque
branche avec une boucle, dont l'écriture est simplifiée par les symétries.

Épisode 3
'''''''''

Une interface graphique n'étant pas demandée, nous choisissons de réaliser
l'interactivité en console, par une demande de saisie.

La fonction ``input`` renvoie la chaîne de caractères saisie à laquelle nous
appliquons la fonction ``split`` qui revoie une liste de chaînes découpées
d'après le caractère demandé (par défaut un blanc: espace, tabulation, etc.).
Nous appliquons la fonction ``int`` qui transforme une chaine en entier à chacun
des éléments de la liste grâce à la fonction ``map``. Finalement, nous
appliquons la fonction ``tuple`` pour avoir un objet concret.

.. note::

   Décomposé avec une saisie ``1  2 3``

   .. code-block::

        In [1]: c = '1  2 3'

        In [2]: c.split()
        Out[2]: ['1', '2', '3']

        In [3]: map(int, c.split())
        Out[3]: <map at 0x7f54310948b0>

        In [4]: tuple(map(int, c.split()))
        Out[4]: (1, 2, 3)

Nous pouvons alors utiliser les valeurs de position et couleur pour allumer un
tål (dans un vrai projet, il serait nécessaire de vérifier la validité de
l'entrée pour éviter les bugs et attaques).

Épisode 4
'''''''''

Il s'agit simplement de faire varier la couleur en fonction d'un paramètre (ici
l'indice de boucle) qui évolue dans le temps (boucle ralentie par un appel à
``time.sleep``). Une animation dans l'autre sens est ajoutée pour une répétition
plus jolie.

Abstraction de la saison 2
--------------------------

RemoteController
''''''''''''''''

L'abstraction ici consiste à travailler directement avec des nombres, et laisser
l'abstraction s'occuper de la communication et des conversions de et vers des
entiers.

Comme pour les autres abstractions, la gestion des erreurs est omise par
commodité.  Ici, nous créons un socket TCP que nous connectons à l'IP et au port
approprié.  Une petite attente et une lecture permet d'ignorer les premières
données transmises.

L'envoi est réalisé en convertissant le nombre en chaîne puis en tableau
d'octets.

La réception fait appel à la fonction ``select.select`` qui retourne une liste
vide s'il n'y a rien à lire au bout d'un moment. Idéalement, cette fonction
prend l'ensemble des descripteurs à lire (ou écrire) afin d'attendre un
évènement sur l'un ou plusieurs d'entre eux, mais dans un contexte tel que les
24h du code, cette utilisation sous-optimale convient.

S'il y a quelque chose à lire, la chaîne est découpée avec ``split`` et
convertie en liste d'entiers.

Notons que nous manipulons directement les nombres, mais que l'abstraction
aurait pu avantageusement (notamment dans le cadre d'un vrai projet) bénéficier
de fonctions pour tester ces nombres à partir de constantes nommées pour
faciliter la lecture.

Saison 2
--------

Épisode 1
'''''''''

Le programme demande le numéro de la télécommande puis instancie un cube et une
télécommande. En boucle, il lie le statut des boutons et appelle la fonction
``move`` ou quitte la boucle selon le bouton.

.. note::

   Ici, il y a emploi de l'opérateur "ET bit-à-bit". Cet opérateur réalise un ET
   logique entre les bits de même position des deux nombres. En choisissant le
   deuxième opérande avec un seul bit à 1, une valeur non nulle indique que ce
   bit était à 1 dans la valeur du premier opérande. Cette méthode est très
   utilisée en embarqué mais aussi dans d'autres contextes.

   .. code-block::

        6     110           5     101
      & 2   & 010         & 2   & 010
      ----  ------        ----  -------
        2     010           0     000

La fonction ``move`` travaille avec une variable globale (vraiment moche,
corrigé dans l'épisode 2). Elle éteint le tål courant, change la position (avec
un modulo) et allume le tål suivant.

Épisode 2
'''''''''

La structure est similaire à l'épisode 1. La fonction ``move`` gère également la
superposition de deux couleurs et les positions ne sont pas récupérées via des
globales. La gestion des télécommandes se fait l'une après l'autre.

Épisode 3
'''''''''

Le programme lit la position des boutons et allume les leds en conséquence. Il
n'y a pas de gestion des conflits d'appui, mais cela est suffisant pour
démontrer le fonctionnement du pilotage des leds de la télécommande.

Saison 3
--------

Épisode unique
''''''''''''''

Pour la saison 3, nous avons décidé de réaliser un jeu de TRON sur le cube : le
joueur 1 part d'en haut avec une couleur, le joueur 2 part d'en bas avec une
autre couleur. Ils se servent de leur télécommande respective pour se déplacer
et allumer les tåls sur leur passage. S'il revient sur un tål allumé, le joueur
a perdu et le tål clignote.

Remarquons que la base ressemble beaucoup à l'épisode 2 de la saison 2 qui a
donc naturellement servi de base.
