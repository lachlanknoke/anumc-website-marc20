# ANUMC Django Website

This repository contains a work‑in‑progress reimplementation of the
[ANU Mountaineering Club](https://anumc.org.au/) website using the
Django web framework.  The goal is to reproduce the features and
content of the existing Drupal site in a modern, maintainable
architecture backed by MariaDB.

## Features

* **Announcements** – editors can add and manage announcements that
  appear on the home page.
* **Events/Trips** – modelled with titles, descriptions, dates,
  fitness/experience requirements and capacity.  Upcoming trips are
  listed on the home page and each has its own detail view.
* **Navigation** – a simple navigation bar reflects the structure of
  the original site (About, Trips & Weekly Events, Gear Store,
  Contact Us).  These pages are placeholders and will be fleshed
  out as development proceeds.
* **Acknowledgement of Country** – the footer includes the
  acknowledgement text from the current ANUMC site【674284794386230†L281-L285】.

## Local development

This project requires Python 3.11+.  To run the development server:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DJANGO_SECRET_KEY="your-secret-key"
python manage.py migrate
python manage.py runserver
```

By default the project uses SQLite to simplify local setup.  To
configure MariaDB, set the environment variable `DJANGO_DATABASE` to
`mariadb` and provide the `DB_NAME`, `DB_USER`, `DB_PASSWORD`,
`DB_HOST` and `DB_PORT` variables as needed.  See
`anumc_website/settings.py` for details.

## Running tests

The project uses Django’s built‑in test framework.  You can run all
tests with:

```bash
python manage.py test
```

The initial test suite focuses on the home page and the event models.
It uses Test‑Driven Development (TDD) principles; as new features are
added, corresponding tests should be written first to define
behaviour.  See `main/tests.py` for examples.

## Roadmap

* **Membership and authentication** – integrate Django’s authentication
  system and extend it to model club memberships and roles.
* **Trip sign‑up and waitlists** – implement booking logic similar to
  the current site.
* **Gear store** – model gear inventory and opening hours.
* **Static pages** – import and manage content such as benefits,
  activities, history, club ethics, contact information and FAQs.
* **Administrative interface** – customise the Django admin to make
  content management intuitive for non‑technical volunteers.【795266301807922†L130-L162】

## Limitations

This repository contains only a minimal skeleton.  It does not yet
include user authentication, forms, front‑end styling or advanced
functionality such as calendar views, member sign‑ups or trip
leadership workflows.  Those features will be added iteratively as
requirements are clarified.