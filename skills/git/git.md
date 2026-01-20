# Git

## Configuration

```bash
# Configuration globale
git config --global user.name "Votre Nom"
git config --global user.email "email@example.com"
git config --global init.defaultBranch main

# Configuration locale (par projet)
git config user.name "Nom Projet"
git config user.email "projet@example.com"
```

## Commandes de base

### Initialisation et clonage
```bash
git init
git clone https://github.com/user/repo.git
git clone --depth 1 https://github.com/user/repo.git  # Clone superficiel
```

### Status et historique
```bash
git status
git log --oneline
git log --graph --oneline --all
git diff
git diff --staged
git show <commit>
```

### Staging et commits
```bash
git add <file>
git add .
git add -p  # Ajout interactif par morceaux

git commit -m "Message"
git commit -am "Message"  # Add + commit (fichiers trackés)
git commit --amend  # Modifier le dernier commit
```

### Branches
```bash
git branch  # Liste des branches
git branch <name>  # Créer une branche
git checkout <branch>  # Changer de branche
git checkout -b <branch>  # Créer et changer
git switch <branch>  # Alternative moderne
git switch -c <branch>  # Créer et changer

git branch -d <branch>  # Supprimer (merge requis)
git branch -D <branch>  # Forcer la suppression
```

### Merge et rebase
```bash
# Merge
git merge <branch>
git merge --no-ff <branch>  # Force un commit de merge

# Rebase
git rebase <branch>
git rebase -i HEAD~3  # Rebase interactif des 3 derniers commits

# Résolution de conflits
git mergetool
git add <resolved-files>
git rebase --continue
git rebase --abort
```

### Remote
```bash
git remote -v
git remote add origin <url>
git remote remove origin

git fetch origin
git pull origin main
git push origin main
git push -u origin <branch>  # Push + set upstream
```

## Workflows courants

### Feature Branch
```bash
# 1. Créer une branche depuis main
git checkout main
git pull
git checkout -b feature/ma-feature

# 2. Travailler sur la feature
git add .
git commit -m "Implémente la feature"

# 3. Mettre à jour avec main
git fetch origin
git rebase origin/main

# 4. Push et créer PR
git push -u origin feature/ma-feature
```

### Hotfix
```bash
git checkout main
git pull
git checkout -b hotfix/fix-critical-bug
# ... fix ...
git commit -m "Fix critical bug"
git push -u origin hotfix/fix-critical-bug
```

## Annulation et correction

### Annuler des modifications
```bash
git checkout -- <file>  # Annuler les modifications non stagées
git restore <file>  # Alternative moderne

git reset HEAD <file>  # Unstage un fichier
git restore --staged <file>  # Alternative moderne
```

### Reset
```bash
git reset --soft HEAD~1  # Annule le commit, garde les changements stagés
git reset --mixed HEAD~1  # Annule le commit, garde les changements non stagés
git reset --hard HEAD~1  # Annule tout (dangereux)
```

### Revert
```bash
git revert <commit>  # Crée un nouveau commit qui annule les changements
```

### Stash
```bash
git stash  # Sauvegarder les modifications en cours
git stash list
git stash pop  # Récupérer et supprimer
git stash apply  # Récupérer sans supprimer
git stash drop  # Supprimer
```

## Cherry-pick

```bash
git cherry-pick <commit>  # Appliquer un commit spécifique
git cherry-pick <commit1> <commit2>  # Plusieurs commits
```

## Tags

```bash
git tag v1.0.0
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
git push origin --tags
```

## Recherche et debug

```bash
git log --grep="fix"  # Rechercher dans les messages
git log -S "function_name"  # Rechercher dans le code
git blame <file>  # Qui a modifié chaque ligne
git bisect start  # Trouver le commit qui a introduit un bug
```

## .gitignore

```gitignore
# Fichiers Python
__pycache__/
*.pyc
.env
venv/

# IDE
.idea/
.vscode/

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/
*.egg-info/
```

## Bonnes pratiques

### Messages de commit
```
type(scope): description courte

Corps détaillé si nécessaire.
Explique le pourquoi, pas le quoi.

Refs: #123
```

Types courants: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Règles
- Commits atomiques (une seule modification logique)
- Messages clairs et descriptifs
- Ne jamais commit de secrets ou credentials
- Rebase avant de merger pour un historique propre
- Utiliser des branches pour chaque feature/fix
