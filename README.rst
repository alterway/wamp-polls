==========
WAMP polls
==========

This is a small demo of a web application with WAMP powered real time notifications. Polls are
updated live on any relevant page.

------------

Installation
============

This application may run on any platform that runs Python 3.4 or a later version.

Get that code
-------------

We assume that you're reading this from the Git Web front that host this project. So, either you
download and inflate the archive that may be available from the project home page (the "Clone or
download" green button above), or get the Git repo URL of the project that shoud be availabe from
the page you're reading and:

.. code:: console

   cd /anywhere/you/want
   git clone <the Git repo URL>

From now, we'll name with the environment variable ``PROJECT_HOME`` the root directory that you
just created and should contain a copy of the ``README.rst`` file you're actually reading.

.. code:: console

   cd wamp-polls
   export PROJECT_HOME=$(pwd)

Create and activate a dedicated Python virtual environment
----------------------------------------------------------

Create and activate a virtualenv for that project. You may use any Python virtual environment
software. Python comes with the ``venv`` module that does the job correctly.

.. code:: console

   python3 -m venv venv
   source venv/bin/activate

Install the requirements
------------------------

.. code:: console

   pip install -r $PROJECT_HOME/requirements.txt

If you want to contribute, thes additional packages may be useful:

.. code:: console

   pip install -r $PROJECT_HOME/dev-requirements.txt

Build the database
------------------

We're actually using SQLite3 that is shipped with the Python bundle. We don't need big database
engines like MySQL or PostgreSQL for that demo.

.. code:: console

   ./manage.py migrate

Will report the database creation. This database should sit in the
``$PROJECT_HOME/var/db/db.sqlite3`` file.

You will need a admin account to add some polls using the Django admin pages:

.. code:: console

   ./manage.py createsuperuser

You may - or not - populate the database with some fuzzy stupid polls:

.. code:: console

   ./manage.py addquestions --help

Will give you the opportunity to customize a little these default questions.

Now we need to export the static files out of Django world to let the static Web server publish
them:

.. code:: console

   ./manage.py collectstatic

Run the beast
=============

Before the first run, just make these quick checks:

.. code:: console

   ./manage.py check
   crossbar check

Both commands should report that everything is OK. Now you can run the beast.

.. code:: console

   crossbar start

Open a browser at http://localhost:8080 and follow the instructions of the home page.

Engineering focus
=================

Where we explain how we use the WAMP PUB/SUB in this app, where and how the various software
pieces deal with it.

Django implementation
---------------------

The server side app is just a classical `Django <https://www.djangoproject.com/>`_ app that mimics
the official Django polls tutorial with some WAMP cookies. I jut used it because I'm familiar with
it and Django paradigms fit my criteria about good frameworks.

.. admonition:: Disclaimer

   This Django app is a demo. As such, I didn't pay any attention to what is considered "good
   practice" for a Django professional implementation. No cache, permissive security, no race
   condition protection and no database I/O optims are in the box. Just KISS (Keep It Stupid
   Simple)

Note that the same demo, including the WAMP router connection could be made with other languages
or frameworks that have a WAMP client.

Crossbar config
---------------

The crossbar config is in the ``.crossbar/config.yaml`` file. Yes it's a YAML file though Crossbar
defaults to JSON config files. But YAML is better suited to configuration files and allows
comments, replacements and others.

There's only one worker - enough for this demo - that manages the **polls** realm. It has a very
permissive security policy.

It exposes:

- A WSGI host service at the ``/`` root path that runs the Django app.
- A static HTTP server at ``/static/...`` that serves Web media (CSS, assets, JS including
  Autobahn|JS).
- A REST/HTTP publication bridge at ``/publish`` for the **polls** realm.

Please read http://crossbar.io/docs/Node-Configuration/ for more details about Crossbar
configuration.

The WAMP publication in Python
------------------------------

Nearly all WAMP stuffs in the Web server app happens in the ``apps/polls/views.py`` module.

Posting a new valid vote form triggers the ``VoteView.form_valid()`` method.

After saving the updated vote to the database, it builds the JSON object message reflecting the
question and choices changes in that form:

.. code:: json

   {
     "question_id": <PK of the question in database>,
     "total_votes": <Total votes on all choices>,
     "choices":
        [  // Repeated for all question related choices
           {"id": <PK of the choice in the database>,
            "votes": <Votes count for this choice>,
            "percent": <Percent for this choice>}
        ]
   }

This message is then managed by ``wamp_publish()`` function that wraps this Python/JSON object
into the envelope expected by the Crossbar HTTP/REST bridge and posts it to the
``question.update`` WAMP URI of the ``polls`` realm.

The HTML view template
----------------------

Now have a look at the HTML template ``apps/polls/templates/polls/index.html``.

.. admonition:: Hey wait! There's another template!

   Only this template is explained here. It's the simplest one of both, since it just requires to
   update one HTML element per page. Once you get the enlightenment, you could read the more
   complex template and associated script in ``apps/polls/templates/polls/vote.html``.


You notice in the template that each vote count in the list is displayed by this template
construct:

.. code:: html

   <span class="badge" id="responses-count-{{ question.id }}">
     {{ question.responses_count }}
   </span>

This instructs to render the votes count of each row with the id being like
``response-count-133``, the ``133`` being the primary key of that question in the database.

The WAMP subscription in JS
---------------------------

You can see in the same template a commented Javascript dedicated to this view.

This JS registers a session in the WAMP router on the ``polls`` realm. Then a subscription hook for the ``question.update`` WAMP URI is asigned to the

This is a simple JS function that receive the above mentioned JSON object, that includes notably
the primary key of the changed question and the new total count of votes. It searches with a
jQuery selector the element with the corresponding ``responses-count-<primary key>`` id and
changes its content with the onr provided by the provided JSON object (key "``total_votes``").

Considered improvements (Todo?)
===============================

Lots of things could be improved here:

- A more restrictive security policy, denying votes coming from anywho or anywhere.
- A more "state of the art" JS part. JS gurus may notice I'm not one of them ;o)
- More "noob friendly" comments in the code.
- Better unit tests coverage.
- Use a more clever WAMP URI scheme policy.
- Refactor the subscription pattern such we could use the same JS wrapping envelope for all
  subscriptions. Need the help of a JS guru too.
- CRUD forms to add, remove, edit questions and choices, replacing Django OTB admin stuffs.
- ...

Any help (fork / pull request) in these fields will be appreciated.

How to...
=========

Manage questions and choices
----------------------------

I didn't provide views dedicated to questions and choices management. So click the **Admin** link
at top right of all pages, provide the credentials you supplied with the ``./manage.py
createsuperuser`` when installing this software. Then click the **Questions of polls** link.

Questions and choices management forms are self explanative.

Exits about WAMP, Crossbar and Autobahn
=======================================

Main sites (docs, etc.)
-----------------------

The WAMP protocol
  http://wamp-proto.org/

Crossbar.io
  http://crossbar.io/

Autobahn|Python
  http://autobahn.readthedocs.io/en/latest/

Autobahn|JS
  https://github.com/crossbario/autobahn-js/tree/master/doc

Community support
-----------------

Google groups
  https://groups.google.com/forum/#!forum/crossbario and
  https://groups.google.com/forum/#!forum/autobahnws

Some articles (French)
  http://sametmax.com/tag/wamp/

More Crossbar demos
-------------------

With various other client languages (JS, PHP, Golang, ...), frameworks, architectures
  https://github.com/crossbario/crossbar-examples

Live demos of some of above source codes(just browse and play)
  https://demo.crossbar.io/

Python with cypher, auth, WAMP components, etc.
  https://github.com/crossbario/autobahn-python/tree/master/examples

Credits
=======

This demo is an open source contribution by `Alter Way
<https://www.alterway.fr/>`_ developed by `Gilles Lenfant
<mailto:gilles.lenfant@alterway.fr>`_.

Kudos to:

- my mates from Alter Way for the functional tests and directions,
- the Crossbar and Autobahn contributors for their help on Github tracker

License
=======

MIT License

Copyright (c) 2017 Gilles Lenfant for Alter Way

.. code:: text

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
