# -*- coding: utf-8 -*-
"""
Category views
"""
from django.conf import settings
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views import generic

from braces.views import LoginRequiredMixin

from forum.models import Category, Thread

from forum.utils.views import SimpleListView

from forum.forms.category import CategoryForm
from forum.views.thread import ThreadQuerysetFiltersMixin

class CategoryIndexView(LoginRequiredMixin, SimpleListView):
    """
    Category list
    """
    template_name = 'forum/category_index.html'
    queryset = Category.objects.filter(visible=True).annotate(num_threads=Count('thread')).order_by('order', 'title')
    paginate_by = settings.FORUM_CATEGORY_INDEX_PAGINATE

class CategoryDetailsView(LoginRequiredMixin, ThreadQuerysetFiltersMixin, SimpleListView):
    """
    Category detail and its thread list
    """
    template_name = 'forum/category_details.html'
    paginate_by = settings.FORUM_CATEGORY_THREAD_PAGINATE
    
    def get_queryset(self, *args, **kwargs):
        self.category_instance = get_object_or_404(Category, slug=self.kwargs['slug'], visible=True)
        self.queryset = Thread.objects.filter(category=self.category_instance)
        return super(CategoryDetailsView, self).get_queryset(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(CategoryDetailsView, self).get_context_data(**kwargs)
        context.update({
            'category_instance': self.category_instance,
        })
        return context

class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Category create form view
    
    TODO: restrict for admins only
    """
    model = Category
    form_class = CategoryForm
    template_name = 'forum/category_form.html'
    permission_required = 'forum.add_category'
    raise_exception = True

    def get_success_url(self):
        return self.object.get_absolute_url()

class CategoryEditView(LoginRequiredMixin, generic.UpdateView):
    """
    Category edit form view
    
    TODO: restrict for admins only
    """
    model = Category
    form_class = CategoryForm
    template_name = 'forum/category_form.html'
    context_object_name = "category_instance"
    permission_required = 'forum.change_category'
    raise_exception = True

    def get_success_url(self):
        return self.object.get_absolute_url()
