# -*- coding: utf-8 -*-
"""
Category views
"""
from django.conf import settings
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views import generic

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from forum.models import Category, Thread

from forum.utils.views import SimpleListView

from forum.forms.category import CategoryForm
from forum.mixins import ThreadQuerysetFiltersMixin

class CategoryIndexView(LoginRequiredMixin, SimpleListView):
    """
    Category list view
    """
    template_name = 'forum/category/index.html'
    queryset = Category.objects.filter(visible=True).annotate(num_threads=Count('thread')).order_by('order', 'title')
    paginate_by = settings.FORUM_CATEGORY_INDEX_PAGINATE
    
    def get_context_data(self, **kwargs):
        context = super(CategoryIndexView, self).get_context_data(**kwargs)
        context.update({
            'FORUM_TEXT_FIELD_JS_TEMPLATE': settings.FORUM_TEXT_FIELD_JS_TEMPLATE,
            'FORUM_TEXT_MARKUP_RENDER_TEMPLATE': settings.FORUM_TEXT_MARKUP_RENDER_TEMPLATE,
        })
        return context


class CategoryDetailsView(LoginRequiredMixin, ThreadQuerysetFiltersMixin, SimpleListView):
    """
    Category detail view with its thread list
    """
    template_name = 'forum/category/details.html'
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


class CategoryCreateView(PermissionRequiredMixin, generic.CreateView):
    """
    Category create form view
    
    Restricted to user with ``forum.add_category`` global permission
    """
    model = Category
    form_class = CategoryForm
    template_name = 'forum/category/form.html'
    permission_required = 'forum.add_category'
    raise_exception = True

    def get_success_url(self):
        return self.object.get_absolute_url()
    
    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context.update({
            'FORUM_TEXT_FIELD_JS_TEMPLATE': settings.FORUM_TEXT_FIELD_JS_TEMPLATE,
            'FORUM_TEXT_MARKUP_RENDER_TEMPLATE': settings.FORUM_TEXT_MARKUP_RENDER_TEMPLATE,
        })
        return context

class CategoryEditView(PermissionRequiredMixin, generic.UpdateView):
    """
    Category edit form view
    
    Restricted to category moderators only
    """
    model = Category
    form_class = CategoryForm
    template_name = 'forum/category/form.html'
    context_object_name = "category_instance"
    permission_required = 'forum.moderate_category'
    raise_exception = True

    def get_success_url(self):
        return self.object.get_absolute_url()
    
    def get_context_data(self, **kwargs):
        context = super(CategoryEditView, self).get_context_data(**kwargs)
        context.update({
            'FORUM_TEXT_FIELD_JS_TEMPLATE': settings.FORUM_TEXT_FIELD_JS_TEMPLATE,
            'FORUM_TEXT_MARKUP_RENDER_TEMPLATE': settings.FORUM_TEXT_MARKUP_RENDER_TEMPLATE,
        })
        return context
