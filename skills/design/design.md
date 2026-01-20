# Velzon Design System - SaaS Dashboard (Tailwind CSS)

Ce skill décrit le design system inspiré de Velzon pour créer des interfaces SaaS modernes avec Tailwind CSS.

## Vue d'ensemble

Design épuré, moderne et data-driven. Privilégie la lisibilité, la hiérarchie visuelle et l'efficacité dans la présentation des données.

## Palette de couleurs

### Configuration Tailwind
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff2f7',
          100: '#d4dae8',
          200: '#a9b5d1',
          300: '#7e90ba',
          400: '#536ba3',
          500: '#405189', // Principal
          600: '#33416e',
          700: '#263152',
          800: '#1a2037',
          900: '#0d101b',
        },
        secondary: {
          500: '#3577f1', // Bleu vif
        },
        success: {
          50: '#e6f7f4',
          500: '#0ab39c', // Vert teal
          600: '#099885',
        },
        warning: {
          50: '#fef7e9',
          500: '#f7b84b', // Orange/Jaune
          600: '#d9a03d',
        },
        danger: {
          50: '#fdeeed',
          500: '#f06548', // Rouge/Orange
          600: '#cc563d',
        },
        info: {
          500: '#299cdb', // Bleu clair
        },
        // Neutres
        slate: {
          50: '#f3f3f9',   // Fond de page
          100: '#e9ebec',  // Bordures
          400: '#878a99',  // Texte muted
          600: '#495057',  // Texte principal
          800: '#212529',  // Fond card dark
          900: '#1a1d21',  // Fond page dark
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'xxs': '0.625rem',  // 10px
        'xs': '0.75rem',    // 12px
        'sm': '0.8125rem',  // 13px - Corps
        'base': '0.875rem', // 14px
        'lg': '1rem',       // 16px
        'xl': '1.25rem',    // 20px
        '2xl': '1.5rem',    // 24px
      },
    },
  },
}
```

## Typographie

```html
<!-- Titre de page -->
<h1 class="text-2xl font-semibold text-slate-600 dark:text-slate-100">Projects</h1>

<!-- Titre de card -->
<h5 class="text-base font-semibold text-slate-600 dark:text-slate-100">Team Members</h5>

<!-- Label uppercase -->
<span class="text-xs font-medium uppercase tracking-wide text-slate-400">Sort By</span>

<!-- Corps de texte -->
<p class="text-sm text-slate-600 dark:text-slate-300">Description text</p>

<!-- Texte muted -->
<span class="text-xs text-slate-400">09:10 am</span>
```

## Structure de layout

### Layout principal
```html
<div class="min-h-screen bg-slate-50 dark:bg-slate-900">
  <!-- Header -->
  <header class="fixed top-0 left-0 right-0 h-16 bg-white dark:bg-slate-800 border-b border-slate-100 dark:border-slate-700 z-50">
    <div class="flex items-center justify-between h-full px-4">
      <!-- Logo -->
      <div class="flex items-center gap-4">
        <img src="logo.svg" alt="Logo" class="h-8">
        <!-- Search -->
        <div class="relative hidden md:block">
          <input type="text" placeholder="Search..."
            class="w-64 pl-10 pr-4 py-2 text-sm bg-slate-50 dark:bg-slate-700 border-0 rounded-lg focus:ring-2 focus:ring-primary-500">
          <i class="ri-search-line absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"></i>
        </div>
      </div>
      <!-- Actions -->
      <div class="flex items-center gap-3">
        <button class="relative p-2 text-slate-500 hover:text-slate-600">
          <i class="ri-notification-3-line text-xl"></i>
          <span class="absolute top-1 right-1 w-2 h-2 bg-danger-500 rounded-full"></span>
        </button>
        <!-- User menu -->
        <div class="flex items-center gap-2">
          <img src="avatar.jpg" class="w-8 h-8 rounded-full">
          <span class="text-sm font-medium text-slate-600 dark:text-slate-200">Anna Adame</span>
        </div>
      </div>
    </div>
  </header>

  <!-- Sidebar -->
  <aside class="fixed top-16 left-0 w-64 h-[calc(100vh-4rem)] bg-white dark:bg-slate-800 border-r border-slate-100 dark:border-slate-700 overflow-y-auto">
    <nav class="p-4">
      <!-- Menu items -->
    </nav>
  </aside>

  <!-- Main content -->
  <main class="ml-64 pt-16 p-6">
    <!-- Page content -->
  </main>
</div>
```

### Sidebar menu item
```html
<!-- Item actif -->
<a href="#" class="flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-primary-500 bg-primary-50 dark:bg-primary-500/10 rounded-lg">
  <i class="ri-dashboard-line text-lg"></i>
  <span>Dashboard</span>
</a>

<!-- Item normal -->
<a href="#" class="flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 rounded-lg">
  <i class="ri-folder-line text-lg"></i>
  <span>Projects</span>
  <span class="ml-auto text-xs bg-danger-500 text-white px-1.5 py-0.5 rounded">5</span>
</a>

<!-- Section title -->
<p class="px-4 py-2 text-xs font-semibold uppercase tracking-wider text-slate-400">Apps</p>
```

## Composants

### Card
```html
<div class="bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-100 dark:border-slate-700">
  <!-- Header -->
  <div class="flex items-center justify-between px-4 py-3 border-b border-slate-100 dark:border-slate-700">
    <h5 class="text-base font-semibold text-slate-600 dark:text-slate-100">Team Members</h5>
    <div class="flex items-center gap-2">
      <!-- Dropdown trigger -->
      <button class="text-xs text-slate-500 hover:text-slate-600">
        Sort By: <span class="text-slate-600 font-medium">Last 30 Days</span>
        <i class="ri-arrow-down-s-line"></i>
      </button>
    </div>
  </div>
  <!-- Body -->
  <div class="p-4">
    <!-- Content -->
  </div>
</div>
```

### Badges de statut
```html
<!-- Success (Completed) -->
<span class="inline-flex items-center px-2 py-1 text-xs font-medium rounded bg-success-50 text-success-600 dark:bg-success-500/10 dark:text-success-500">
  Completed
</span>

<!-- Warning (In Progress) -->
<span class="inline-flex items-center px-2 py-1 text-xs font-medium rounded bg-warning-50 text-warning-600 dark:bg-warning-500/10 dark:text-warning-500">
  In Progress
</span>

<!-- Danger (Pending) -->
<span class="inline-flex items-center px-2 py-1 text-xs font-medium rounded bg-danger-50 text-danger-600 dark:bg-danger-500/10 dark:text-danger-500">
  Pending
</span>

<!-- Info (New) -->
<span class="inline-flex items-center px-2 py-1 text-xs font-medium rounded bg-info-500/10 text-info-500">
  +3 New
</span>
```

### Progress bars
```html
<div class="flex items-center gap-3">
  <div class="flex-1 h-1.5 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden">
    <div class="h-full bg-primary-500 rounded-full" style="width: 64%"></div>
  </div>
  <span class="text-xs text-slate-400 w-8">64%</span>
</div>

<!-- Progress coloré selon valeur -->
<div class="h-1.5 bg-slate-100 rounded-full overflow-hidden">
  <div class="h-full bg-success-500 rounded-full" style="width: 77%"></div>
</div>
```

### Avatars
```html
<!-- Tailles -->
<img src="avatar.jpg" class="w-6 h-6 rounded-full">   <!-- xs: 24px -->
<img src="avatar.jpg" class="w-8 h-8 rounded-full">   <!-- sm: 32px -->
<img src="avatar.jpg" class="w-10 h-10 rounded-full"> <!-- md: 40px -->
<img src="avatar.jpg" class="w-12 h-12 rounded-full"> <!-- lg: 48px -->

<!-- Avatar avec statut online -->
<div class="relative">
  <img src="avatar.jpg" class="w-10 h-10 rounded-full">
  <span class="absolute bottom-0 right-0 w-3 h-3 bg-success-500 border-2 border-white dark:border-slate-800 rounded-full"></span>
</div>

<!-- Groupe d'avatars -->
<div class="flex -space-x-2">
  <img src="avatar1.jpg" class="w-8 h-8 rounded-full ring-2 ring-white dark:ring-slate-800">
  <img src="avatar2.jpg" class="w-8 h-8 rounded-full ring-2 ring-white dark:ring-slate-800">
  <img src="avatar3.jpg" class="w-8 h-8 rounded-full ring-2 ring-white dark:ring-slate-800">
  <span class="flex items-center justify-center w-8 h-8 text-xs font-medium text-primary-600 bg-primary-100 rounded-full ring-2 ring-white dark:ring-slate-800">
    +3
  </span>
</div>
```

### Table (Team Members)
```html
<table class="w-full">
  <thead>
    <tr class="text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
      <th class="pb-3">Member</th>
      <th class="pb-3">Hours</th>
      <th class="pb-3">Tasks</th>
      <th class="pb-3">Status</th>
    </tr>
  </thead>
  <tbody class="divide-y divide-slate-100 dark:divide-slate-700">
    <tr>
      <td class="py-3">
        <div class="flex items-center gap-3">
          <img src="avatar.jpg" class="w-8 h-8 rounded-full">
          <div>
            <p class="text-sm font-medium text-slate-600 dark:text-slate-200">Donald Risher</p>
            <p class="text-xs text-slate-400">Product Manager</p>
          </div>
        </div>
      </td>
      <td class="py-3 text-sm text-slate-600 dark:text-slate-300">110h : 150h</td>
      <td class="py-3 text-sm text-slate-600 dark:text-slate-300">258</td>
      <td class="py-3">
        <div class="w-24 h-1.5 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden">
          <div class="h-full bg-success-500 rounded-full" style="width: 73%"></div>
        </div>
      </td>
    </tr>
  </tbody>
</table>
```

### Boutons
```html
<!-- Primary -->
<button class="px-4 py-2 text-sm font-medium text-white bg-primary-500 hover:bg-primary-600 rounded-lg transition-colors">
  Action
</button>

<!-- Primary soft -->
<button class="px-4 py-2 text-sm font-medium text-primary-600 bg-primary-50 hover:bg-primary-100 dark:bg-primary-500/10 dark:hover:bg-primary-500/20 rounded-lg transition-colors">
  Action
</button>

<!-- Success avec icône -->
<button class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-success-500 hover:bg-success-600 rounded-lg transition-colors">
  <i class="ri-send-plane-fill"></i>
  Send
</button>

<!-- Icon button -->
<button class="p-2 text-slate-500 hover:text-slate-600 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors">
  <i class="ri-settings-4-line text-lg"></i>
</button>

<!-- Outline -->
<button class="px-4 py-2 text-sm font-medium text-primary-500 border border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-500/10 rounded-lg transition-colors">
  Action
</button>
```

### Dropdown
```html
<div class="relative" x-data="{ open: false }">
  <button @click="open = !open" class="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-600">
    <span>Sort By:</span>
    <span class="font-medium text-slate-600">Last 30 Days</span>
    <i class="ri-arrow-down-s-line"></i>
  </button>
  <div x-show="open" @click.away="open = false"
    class="absolute right-0 mt-2 w-48 bg-white dark:bg-slate-800 rounded-lg shadow-lg border border-slate-100 dark:border-slate-700 py-1 z-10">
    <a href="#" class="block px-4 py-2 text-sm text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700">Today</a>
    <a href="#" class="block px-4 py-2 text-sm text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700">Last 7 Days</a>
    <a href="#" class="block px-4 py-2 text-sm text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700">Last 30 Days</a>
    <a href="#" class="block px-4 py-2 text-sm text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700">All Time</a>
  </div>
</div>
```

### Chat widget
```html
<div class="flex flex-col h-80">
  <!-- Messages -->
  <div class="flex-1 overflow-y-auto space-y-4 p-4">
    <!-- Message reçu -->
    <div class="flex gap-3">
      <img src="avatar.jpg" class="w-8 h-8 rounded-full flex-shrink-0">
      <div>
        <div class="bg-slate-100 dark:bg-slate-700 rounded-lg rounded-tl-none px-3 py-2 max-w-xs">
          <p class="text-sm text-slate-600 dark:text-slate-200">Yeah everything is fine. Our next meeting tomorrow at 10.00 AM</p>
        </div>
        <span class="text-xs text-slate-400 mt-1">09:10 am</span>
      </div>
    </div>

    <!-- Message envoyé -->
    <div class="flex justify-end">
      <div class="text-right">
        <div class="bg-primary-500 rounded-lg rounded-tr-none px-3 py-2 max-w-xs">
          <p class="text-sm text-white">Wow that's great</p>
        </div>
        <span class="text-xs text-slate-400 mt-1">
          <i class="ri-check-double-line text-success-500"></i> 09:12 am
        </span>
      </div>
    </div>
  </div>

  <!-- Input -->
  <div class="border-t border-slate-100 dark:border-slate-700 p-4">
    <div class="flex gap-2">
      <input type="text" placeholder="Enter Message..."
        class="flex-1 px-4 py-2 text-sm bg-slate-50 dark:bg-slate-700 border-0 rounded-lg focus:ring-2 focus:ring-primary-500">
      <button class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-success-500 hover:bg-success-600 rounded-lg">
        Send <i class="ri-send-plane-fill"></i>
      </button>
    </div>
  </div>
</div>
```

### Widget statistique
```html
<div class="bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-100 dark:border-slate-700 p-4">
  <div class="flex items-center justify-between">
    <div>
      <p class="text-xs font-medium uppercase tracking-wide text-slate-400 mb-1">Total Projects</p>
      <h4 class="text-2xl font-semibold text-slate-600 dark:text-slate-100">258</h4>
    </div>
    <span class="inline-flex items-center px-2 py-1 text-xs font-medium rounded bg-success-50 text-success-600">
      <i class="ri-arrow-up-line mr-1"></i>+16.24%
    </span>
  </div>
</div>
```

### Projects Status (Donut legend)
```html
<div class="space-y-3">
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 bg-success-500 rounded-full"></span>
      <span class="text-sm text-slate-600 dark:text-slate-300">Completed</span>
    </div>
    <span class="text-sm text-slate-600 dark:text-slate-300">125 Projects</span>
    <span class="text-sm font-medium text-success-500">15870hrs</span>
  </div>
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 bg-primary-500 rounded-full"></span>
      <span class="text-sm text-slate-600 dark:text-slate-300">In Progress</span>
    </div>
    <span class="text-sm text-slate-600 dark:text-slate-300">42 Projects</span>
    <span class="text-sm font-medium text-primary-500">243hrs</span>
  </div>
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 bg-warning-500 rounded-full"></span>
      <span class="text-sm text-slate-600 dark:text-slate-300">Yet to Start</span>
    </div>
    <span class="text-sm text-slate-600 dark:text-slate-300">58 Projects</span>
    <span class="text-sm font-medium text-warning-500">-2050hrs</span>
  </div>
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 bg-danger-500 rounded-full"></span>
      <span class="text-sm text-slate-600 dark:text-slate-300">Cancelled</span>
    </div>
    <span class="text-sm text-slate-600 dark:text-slate-300">89 Projects</span>
    <span class="text-sm font-medium text-danger-500">-900hrs</span>
  </div>
</div>
```

### Pagination
```html
<div class="flex items-center justify-between">
  <p class="text-sm text-slate-400">Showing 5 of 25 Results</p>
  <div class="flex items-center gap-1">
    <button class="p-2 text-slate-400 hover:text-slate-600 disabled:opacity-50" disabled>
      <i class="ri-arrow-left-s-line"></i>
    </button>
    <button class="w-8 h-8 text-sm text-slate-600 hover:bg-slate-100 dark:hover:bg-slate-700 rounded">1</button>
    <button class="w-8 h-8 text-sm text-white bg-primary-500 rounded">2</button>
    <button class="w-8 h-8 text-sm text-slate-600 hover:bg-slate-100 dark:hover:bg-slate-700 rounded">3</button>
    <button class="p-2 text-slate-400 hover:text-slate-600">
      <i class="ri-arrow-right-s-line"></i>
    </button>
  </div>
</div>
```

### Checklist / Todo
```html
<div class="space-y-3">
  <label class="flex items-center gap-3 cursor-pointer">
    <input type="checkbox" class="w-4 h-4 text-primary-500 border-slate-300 rounded focus:ring-primary-500">
    <span class="text-sm text-slate-600 dark:text-slate-300">E-commerce Landing Page</span>
    <span class="ml-auto text-xs text-slate-400">10 Dec 2021</span>
    <span class="px-2 py-0.5 text-xs font-medium rounded bg-danger-50 text-danger-600">Pending</span>
  </label>
  <label class="flex items-center gap-3 cursor-pointer">
    <input type="checkbox" checked class="w-4 h-4 text-primary-500 border-slate-300 rounded focus:ring-primary-500">
    <span class="text-sm text-slate-400 line-through">UI/UX Design</span>
    <span class="ml-auto text-xs text-slate-400">22 Dec 2021</span>
    <span class="px-2 py-0.5 text-xs font-medium rounded bg-success-50 text-success-600">Done</span>
  </label>
</div>
```

## Icônes

Utiliser **Remix Icon** (https://remixicon.com/)

```html
<link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">

<!-- Exemples -->
<i class="ri-dashboard-line"></i>      <!-- Dashboard -->
<i class="ri-user-line"></i>           <!-- User -->
<i class="ri-settings-4-line"></i>     <!-- Settings -->
<i class="ri-notification-3-line"></i> <!-- Notifications -->
<i class="ri-search-line"></i>         <!-- Search -->
<i class="ri-more-2-fill"></i>         <!-- More actions -->
<i class="ri-check-double-line"></i>   <!-- Double check (lu) -->
<i class="ri-send-plane-fill"></i>     <!-- Send -->
<i class="ri-arrow-up-line"></i>       <!-- Trend up -->
<i class="ri-arrow-down-line"></i>     <!-- Trend down -->
<i class="ri-folder-line"></i>         <!-- Folder -->
<i class="ri-calendar-line"></i>       <!-- Calendar -->
```

## Grille et espacements

```html
<!-- Row de widgets (4 colonnes sur xl, 2 sur md, 1 sur mobile) -->
<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
  <!-- Widgets -->
</div>

<!-- Layout principal + sidebar -->
<div class="grid grid-cols-1 xl:grid-cols-3 gap-4">
  <div class="xl:col-span-2"><!-- Contenu principal --></div>
  <div><!-- Sidebar widgets --></div>
</div>

<!-- Layout 3 colonnes égales -->
<div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
  <div><!-- Widget 1 --></div>
  <div><!-- Widget 2 --></div>
  <div><!-- Widget 3 --></div>
</div>
```

## Dark mode

Utiliser la stratégie `class` de Tailwind:

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  // ...
}
```

```html
<!-- Toggle dark mode -->
<html class="dark">
  <!-- Le dark mode s'applique -->
</html>
```

## Dépendances recommandées

- **Tailwind CSS 3.4+**
- **Remix Icon** - Icônes
- **Alpine.js** - Interactivité (dropdowns, modals)
- **ApexCharts** - Graphiques
- **Flatpickr** - Date picker

## Patterns UX récurrents

1. **Header de carte**: Titre à gauche, actions/dropdown à droite
2. **Listes avec avatars**: Photo + nom + rôle alignés avec `flex items-center gap-3`
3. **Statuts visuels**: Badges avec fond subtil (`bg-{color}-50 text-{color}-600`)
4. **Filtres temporels**: Dropdown discret "Last 30 Days"
5. **Notifications badge**: Point rouge absolu sur icônes
6. **Load More**: Lien texte `text-primary-500 hover:underline`
7. **Breadcrumb**: Séparateur `/` avec `text-slate-400`

## Notes d'implémentation Django

```python
# Intégration avec django-tailwind ou manuel avec npm

# Structure templates
templates/
├── base.html              # Layout avec Tailwind
├── components/
│   ├── card.html          # {% include "components/card.html" %}
│   ├── badge.html
│   └── avatar.html
└── dashboard/
    └── index.html
```

```html
<!-- base.html -->
{% load static %}
<!DOCTYPE html>
<html lang="fr" class="{% if request.session.dark_mode %}dark{% endif %}">
<head>
  <link href="{% static 'css/tailwind.css' %}" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
</head>
<body class="bg-slate-50 dark:bg-slate-900 text-slate-600 dark:text-slate-300">
  {% block content %}{% endblock %}
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</body>
</html>
```
