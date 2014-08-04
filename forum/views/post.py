# -*- coding: utf-8 -*-
"""
Vues des messages de fils
"""
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views import generic

from braces.views import LoginRequiredMixin

from forum.utils.views import DirectDeleteView

from forum.models import Category, Post

from forum.forms.post import PostEditForm

class PostEditView(LoginRequiredMixin, generic.UpdateView):
    """
    Édition d'un message
    
    TODO: restrict for admins only (and message owner)
    """
    model = Post
    form_class = PostEditForm
    template_name = 'forum/post_form.html'
    context_object_name = "post_instance"
    permission_required = 'forum.change_post'
    raise_exception = True
    
    def get_object(self, *args, **kwargs):
        self.category_instance = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return get_object_or_404(Post, thread__id=self.kwargs['thread_id'], thread__category=self.category_instance, pk=self.kwargs['post_id'])
        
    def get_context_data(self, **kwargs):
        context = super(PostEditView, self).get_context_data(**kwargs)
        context.update({
            'category_instance': self.category_instance,
            'thread_instance': self.object.thread,
        })
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()

class PostDeleteView(LoginRequiredMixin, DirectDeleteView):
    """
    Supprimer un message directement sans confirmation
    
    TODO: restrict for admins only
    """
    model = Post
    permission_required = 'forum.delete_post'
    raise_exception = True
    
    def get_object(self, *args, **kwargs):
        self.category_instance = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return get_object_or_404(Post, thread__id=self.kwargs['thread_id'], thread__category=self.category_instance, pk=self.kwargs['post_id'])

    def get_success_url(self):
        return reverse('forum-thread-details', args=(self.category_instance.slug, self.object.thread_id))
