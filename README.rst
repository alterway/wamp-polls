================
Polls temps réel
================

Ce projet est une démonstration du protocole WAMP basée sur le tutoriel "Polls" de Django.

.. attention::

   N'installez pas ce logiciel tel-quel en production. Pour des raisons pédagogiques, celui-ci n'incorpore que les sécurités minimales requises pour la démonstration.

Installation
============

Nous supposons que vous venez d'obtenir une copie de travail depuis le dépôt source Git. Nous désignons par la variable d'enfironnement ``PROJECT_HOME`` le répertoire racine de ce dépôt local.

L'installation de ce logiciel nécessite Python 3.5 ou une version ultérieure. Il est préférable, comme pour toute application Python, de créer un environnement virtuel à cet effet.

.. code:: console

   cd $PROJECT_HOME
   python3 -m venv venv
   source venv/bin/activate

.. note:: console

   Notez que toute la suite de cette documentation suppose que vous tapez les commandes avec cet environnement virtuel activé.

Installez les dépendances :

.. code:: console

   pip install -r $PROJECT_HOME/requirements.txt

Si vous voulez modifier ce projet, il est également recommandé d'installer les dépendances de développement :

.. code:: console

   pip install -r $PROJECT_HOME/dev-requirements.txt

Lancer le serveur
=================

On lance en premier les services Crossbar.io

.. code:: console

   crossbar start

Puis dans une autre console, le serveur Web Django

.. code:: console

   $PROJECT_HOME/manage.py runserver

Utilisation
===========

Visiter le site
---------------

Ouvrez http://<host>:8000

Créer un utilisateur superuser
------------------------------

Un superuser dispose des droits pour viiter les formulaires d'administration du site accessibles depuis l'adresse http://<host>:8000/admin

.. code:: console

   $PROJECT_HOME/manage.py createsuperuser

Les formulaires d'administration vous permettent - entre autres - de gérer les authentifications et permissions des utilisateurs.

Exits framework
===============

Le protocole WAMP
  http://wamp-proto.org/

Le client WAMP Autobahn (Python et JS)
  http://autobahn.ws/

Le routeur WAMP Crossbar.io
  http://crossbar.io/

Le framework Web Django
  https://www.djangoproject.com/

Liens développement
===================

Django Debug Toolbar
  http://django-debug-toolbar.readthedocs.io/en/stable/index.html

Bootstrap 3
  https://realpython.com/blog/python/getting-started-with-bootstrap-3/

Articles en Français chez Sam et Max
  http://sametmax.com/tag/wamp/

Slides en Français
  https://www.slideshare.net/sametmax/introduction-wampws-le-protocole-websocket-pour-faire-du-pubsub-et-rpc-over-websocket-en-tempr
