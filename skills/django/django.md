# Django

## Structure de projet

```
project/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    └── myapp/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── models.py
        ├── views.py
        ├── urls.py
        ├── forms.py
        ├── templates/
        └── tests/
```

## Modèles

### Définition
```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title
```

### Relations
- `ForeignKey`: Relation many-to-one
- `ManyToManyField`: Relation many-to-many
- `OneToOneField`: Relation one-to-one

### QuerySet
```python
# Filtrage
Article.objects.filter(author=user)
Article.objects.exclude(status='draft')

# Agrégation
from django.db.models import Count, Avg
Article.objects.aggregate(total=Count('id'))

# Annotations
Article.objects.annotate(comment_count=Count('comments'))

# Select related (optimisation)
Article.objects.select_related('author')
Article.objects.prefetch_related('tags')
```

## Vues

### Function-Based Views
```python
from django.shortcuts import render, get_object_or_404

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})
```

### Class-Based Views
```python
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'content']
    success_url = reverse_lazy('article_list')
```

## URLs

```python
from django.urls import path, include

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('api/', include('api.urls')),
]
```

## Formulaires

```python
from django import forms

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError("Le titre est trop court")
        return title
```

## Middleware

```python
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code avant la vue
        response = self.get_response(request)
        # Code après la vue
        return response
```

## Signaux

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Article)
def article_saved(sender, instance, created, **kwargs):
    if created:
        # Logique pour nouvel article
        pass
```

## Commandes de gestion

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py shell
python manage.py test
```

## Bonnes pratiques
- Utiliser des apps Django modulaires
- Séparer les settings par environnement
- Utiliser les managers personnalisés pour les requêtes complexes
- Toujours utiliser `select_related` et `prefetch_related` pour optimiser
- Valider les données dans les formulaires, pas dans les vues
