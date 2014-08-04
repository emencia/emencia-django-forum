# -*- coding: utf-8 -*-
"""
Vues d'index général
"""
from forum.views.category import CategoryIndexView

"""
Page d'index, utilise la vue d'index des catégories
"""
class IndexView(CategoryIndexView): pass
