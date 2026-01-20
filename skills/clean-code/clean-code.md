# Clean Code

## Principes fondamentaux

### Nommage
- Utiliser des noms explicites et descriptifs pour les variables, fonctions et classes
- Éviter les abréviations obscures
- Les noms doivent révéler l'intention du code
- Utiliser des noms prononçables et recherchables

### Fonctions
- Une fonction = une seule responsabilité (Single Responsibility Principle)
- Garder les fonctions courtes (idéalement < 20 lignes)
- Limiter le nombre de paramètres (max 3-4)
- Éviter les effets de bord
- Préférer les fonctions pures quand possible

### Commentaires
- Le code doit être auto-documenté
- Les commentaires expliquent le "pourquoi", pas le "quoi"
- Supprimer le code commenté
- Éviter les commentaires redondants

### Formatage
- Indentation cohérente
- Lignes de longueur raisonnable (80-120 caractères)
- Grouper le code logiquement
- Séparer les concepts par des lignes vides

### DRY (Don't Repeat Yourself)
- Extraire le code dupliqué en fonctions réutilisables
- Centraliser la logique métier
- Utiliser l'héritage ou la composition pour partager le comportement

### KISS (Keep It Simple, Stupid)
- Privilégier la simplicité à la complexité
- Éviter l'over-engineering
- Ne pas anticiper des besoins futurs hypothétiques

### YAGNI (You Aren't Gonna Need It)
- Ne pas implémenter de fonctionnalités "au cas où"
- Se concentrer sur les besoins actuels

## Exemples

### Mauvais nommage
```python
# Mauvais
def calc(x, y):
    return x * y * 0.2

# Bon
def calculate_tax(price, quantity):
    TAX_RATE = 0.2
    return price * quantity * TAX_RATE
```

### Fonction avec trop de responsabilités
```python
# Mauvais
def process_user(data):
    # Valide, sauvegarde, envoie email, génère rapport...
    pass

# Bon
def validate_user(data):
    pass

def save_user(user):
    pass

def send_welcome_email(user):
    pass
```

## Règles de refactoring
- Extraire les méthodes longues
- Renommer pour clarifier l'intention
- Supprimer le code mort
- Simplifier les conditions complexes
- Remplacer les magic numbers par des constantes nommées
