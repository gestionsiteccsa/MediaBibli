# CLAUDE.md

Ce fichier contient les instructions et conventions pour le développement de ce projet.

## Contexte du projet

**MediaBib** est un Système Intégré de Gestion de Bibliothèque (SIGB) open source développé en Django, conçu pour les réseaux de lecture publique. Clone moderne de PMB.

### Objectifs
- Centraliser la gestion (catalogue, lecteurs, prêts, acquisitions, statistiques)
- Faciliter le travail quotidien des bibliothécaires
- Portail OPAC pour les lecteurs
- Support multi-sites avec transferts de documents
- Normes : UNIMARC, Z39.50, SRU/SRW, SIP2
- Conformité : RGPD, WCAG 2.1 AA

### Public cible
- Bibliothèques publiques et médiathèques
- Réseaux de bibliothèques multi-sites
- Documents : livres, CD, DVD, revues, jeux vidéo, partitions, ressources numériques

## Stack technique

- **Framework**: Django 5.2
- **Localisation**: Français (fr-fr)
- **Base de données**: SQLite (dev) / PostgreSQL (prod)

## Commands

```bash
# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Run tests
python manage.py test
python manage.py test home  # Single app

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

## Architecture

```
MediaBiB/
├── app/                    # Django project configuration
│   ├── settings.py         # Main settings
│   ├── urls.py             # Root URL routing
│   └── wsgi.py / asgi.py
├── home/                   # Main application
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   └── templates/home/     # App-specific templates
├── templates/              # Global templates
│   └── base.html           # Base template
├── skills/                 # Documentation technique
│   └── [skill-name]/[skill-name].md
└── manage.py
```

## Key Conventions

- Templates use Django's template inheritance (`{% extends 'base.html' %}`)
- App templates are in `home/templates/home/` following Django's app template pattern
- Global templates (like `base.html`) are in the root `templates/` directory
- The `skills/` folder contains reference documentation for various technologies (Django, HTMX, React, etc.)

### Normes et conformité
- **UNIMARC** : Format de catalogage bibliographique
- **RGPD** : Protection des données personnelles des lecteurs
- **WCAG 2.1 AA** : Accessibilité web

