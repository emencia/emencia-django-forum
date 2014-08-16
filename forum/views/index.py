# -*- coding: utf-8 -*-
from forum.views.category import CategoryIndexView

"""
Forum index is actually using the Category index view
"""
class IndexView(CategoryIndexView): pass
