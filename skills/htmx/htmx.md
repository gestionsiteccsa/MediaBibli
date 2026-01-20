# HTMX

## Installation

```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
```

## Attributs principaux

### Requêtes HTTP
```html
<!-- GET -->
<button hx-get="/api/data">Charger</button>

<!-- POST -->
<button hx-post="/api/submit">Envoyer</button>

<!-- PUT -->
<button hx-put="/api/update/1">Mettre à jour</button>

<!-- DELETE -->
<button hx-delete="/api/delete/1">Supprimer</button>

<!-- PATCH -->
<button hx-patch="/api/partial/1">Modifier</button>
```

### Cible de mise à jour
```html
<!-- Mettre à jour un élément spécifique -->
<button hx-get="/data" hx-target="#result">Charger</button>
<div id="result"></div>

<!-- Cibles spéciales -->
<button hx-get="/data" hx-target="this">Remplacer ce bouton</button>
<button hx-get="/data" hx-target="closest tr">Ligne parente</button>
<button hx-get="/data" hx-target="next .content">Élément suivant</button>
<button hx-get="/data" hx-target="find .item">Premier enfant</button>
```

### Swap (mode d'insertion)
```html
<!-- Remplacer le contenu intérieur (défaut) -->
<div hx-get="/data" hx-swap="innerHTML"></div>

<!-- Remplacer l'élément entier -->
<div hx-get="/data" hx-swap="outerHTML"></div>

<!-- Ajouter à la fin -->
<div hx-get="/data" hx-swap="beforeend"></div>

<!-- Ajouter au début -->
<div hx-get="/data" hx-swap="afterbegin"></div>

<!-- Insérer après l'élément -->
<div hx-get="/data" hx-swap="afterend"></div>

<!-- Insérer avant l'élément -->
<div hx-get="/data" hx-swap="beforebegin"></div>

<!-- Ne rien faire -->
<div hx-get="/data" hx-swap="none"></div>

<!-- Supprimer l'élément -->
<div hx-delete="/item/1" hx-swap="delete"></div>
```

### Déclencheurs
```html
<!-- Événement par défaut (click pour button, submit pour form) -->
<button hx-get="/data">Click</button>

<!-- Événement personnalisé -->
<input hx-get="/search" hx-trigger="keyup">

<!-- Avec délai (debounce) -->
<input hx-get="/search" hx-trigger="keyup changed delay:500ms">

<!-- Intersection (lazy loading) -->
<div hx-get="/more" hx-trigger="revealed"></div>

<!-- Au chargement -->
<div hx-get="/data" hx-trigger="load"></div>

<!-- Événements multiples -->
<div hx-get="/data" hx-trigger="click, keyup from:body"></div>
```

## Formulaires

### Formulaire simple
```html
<form hx-post="/submit" hx-target="#response">
    <input type="text" name="username">
    <input type="email" name="email">
    <button type="submit">Envoyer</button>
</form>
<div id="response"></div>
```

### Inclure des valeurs supplémentaires
```html
<button hx-post="/action" hx-vals='{"id": 123, "action": "approve"}'>
    Approuver
</button>

<!-- Valeurs dynamiques avec JavaScript -->
<button hx-post="/action" hx-vals='js:{timestamp: Date.now()}'>
    Action
</button>
```

### Envoyer avec un autre élément
```html
<input type="text" name="search" id="search-input">
<button hx-get="/search" hx-include="#search-input">Rechercher</button>
```

## Indicateurs de chargement

```html
<button hx-get="/slow-request">
    <span class="htmx-indicator">Chargement...</span>
    Charger
</button>

<style>
    .htmx-indicator { display: none; }
    .htmx-request .htmx-indicator { display: inline; }
    .htmx-request.htmx-indicator { display: inline; }
</style>
```

## Confirmation et validation

```html
<!-- Confirmation -->
<button hx-delete="/item/1" hx-confirm="Êtes-vous sûr ?">
    Supprimer
</button>

<!-- Validation côté client -->
<form hx-post="/submit">
    <input type="email" name="email" required>
    <button type="submit">Envoyer</button>
</form>
```

## Headers et Extensions

### Headers personnalisés
```html
<button hx-get="/data" hx-headers='{"X-Custom-Header": "value"}'>
    Avec header
</button>
```

### Réponses du serveur
```python
# Django view
from django.http import HttpResponse

def my_view(request):
    response = HttpResponse("<div>Nouveau contenu</div>")
    # Redirection côté client
    response['HX-Redirect'] = '/new-page'
    # Rafraîchir la page
    response['HX-Refresh'] = 'true'
    # Déclencher un événement
    response['HX-Trigger'] = 'itemAdded'
    return response
```

## Patterns courants

### Liste avec suppression
```html
<ul id="item-list">
    {% for item in items %}
    <li id="item-{{ item.id }}">
        {{ item.name }}
        <button hx-delete="/items/{{ item.id }}"
                hx-target="#item-{{ item.id }}"
                hx-swap="outerHTML"
                hx-confirm="Supprimer ?">
            X
        </button>
    </li>
    {% endfor %}
</ul>
```

### Recherche en temps réel
```html
<input type="search" name="q"
       hx-get="/search"
       hx-trigger="keyup changed delay:300ms"
       hx-target="#results"
       placeholder="Rechercher...">
<div id="results"></div>
```

### Pagination infinie
```html
<div id="items">
    {% for item in items %}
        <div class="item">{{ item.name }}</div>
    {% endfor %}
</div>
<div hx-get="/items?page={{ next_page }}"
     hx-trigger="revealed"
     hx-target="#items"
     hx-swap="beforeend">
    Chargement...
</div>
```

### Modal
```html
<button hx-get="/modal/content"
        hx-target="#modal-container"
        hx-swap="innerHTML">
    Ouvrir modal
</button>

<div id="modal-container"></div>
```

### Édition inline
```html
<div id="field-1">
    <span>Valeur actuelle</span>
    <button hx-get="/edit/1" hx-target="#field-1" hx-swap="outerHTML">
        Modifier
    </button>
</div>

<!-- Réponse du serveur pour /edit/1 -->
<form hx-put="/save/1" hx-target="this" hx-swap="outerHTML">
    <input type="text" name="value" value="Valeur actuelle">
    <button type="submit">Sauvegarder</button>
    <button hx-get="/cancel/1" hx-target="closest form" hx-swap="outerHTML">
        Annuler
    </button>
</form>
```

## Django + HTMX

### Détection de requête HTMX
```python
def my_view(request):
    if request.headers.get('HX-Request'):
        # Requête HTMX - retourner un fragment
        return render(request, 'partials/fragment.html', context)
    else:
        # Requête normale - retourner la page complète
        return render(request, 'full_page.html', context)
```

### django-htmx
```python
# settings.py
INSTALLED_APPS = [
    'django_htmx',
]

MIDDLEWARE = [
    'django_htmx.middleware.HtmxMiddleware',
]

# views.py
def my_view(request):
    if request.htmx:
        return render(request, 'partial.html')
    return render(request, 'full.html')
```
