# -*- coding: utf-8 -*-
"""
Map des modèles de données dans l'administration de Django
"""
from django.contrib import admin
from models import *

from guardian.admin import GuardedModelAdmin

class CategoryAdmin(GuardedModelAdmin):
    pass

class ThreadAdmin(GuardedModelAdmin):
    def save_model(self, request, obj, form, change):
        """
        Surclasse la méthode de sauvegarde de l'admin du modèle pour y 
        rajouter automatiquement l'auteur qui créé l'objet
        """
        instance = form.save(commit=False)
        if not(instance.created):
            instance.author = request.user
        instance.save()
        form.save_m2m()

        return instance

class PostAdmin(GuardedModelAdmin):
    def save_model(self, request, obj, form, change):
        """
        Surclasse la méthode de sauvegarde de l'admin du modèle pour y 
        rajouter automatiquement l'auteur qui créé l'objet
        """
        instance = form.save(commit=False)
        if not(instance.created):
            instance.author = request.user
        instance.save()
        form.save_m2m()

        return instance

admin.site.register(Category, CategoryAdmin)
admin.site.register(ThreadWatch)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
