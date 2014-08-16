# -*- coding: utf-8 -*-
"""
Vues des messages de fils
"""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views import generic

from guardian.mixins import PermissionRequiredMixin

from braces.views import LoginRequiredMixin

from forum.mixins import ModeratorRequiredMixin

from forum.models import Category, Post

from forum.forms.post import PostEditForm, PostDeleteForm

class PostEditView(LoginRequiredMixin, ModeratorRequiredMixin, generic.UpdateView):
    """
    Message edit view
    
    Restricted to message owner and moderators
    """
    model = Post
    form_class = PostEditForm
    template_name = 'forum/post_form.html'
    context_object_name = "post_instance"
    
    def get_object(self, *args, **kwargs):
        self.category_instance = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return get_object_or_404(Post, thread__id=self.kwargs['thread_id'], thread__category=self.category_instance, pk=self.kwargs['post_id'])

    def check_permissions(self, request):
        self.object = self.get_object()
        
        # Owner can edit its post is FORUM_OWNER_MESSAGE_CAN_EDIT settings is enabled
        if settings.FORUM_OWNER_MESSAGE_CAN_EDIT and self.object.author == request.user:
            return False
            
        return self.check_moderator_permissions(request, self.category_instance, self.object.thread)
        
    def get_context_data(self, **kwargs):
        context = super(PostEditView, self).get_context_data(**kwargs)
        context.update({
            'category_instance': self.category_instance,
            'thread_instance': self.object.thread,
        })
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()

class PostDeleteView(LoginRequiredMixin, ModeratorRequiredMixin, generic.UpdateView):
    """
    Message 'direct to delete' view, without any confirm
    """
    model = Post
    form_class = PostDeleteForm
    template_name = 'forum/post_delete_form.html'
    
    def get_object(self, *args, **kwargs):
        self.category_instance = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return get_object_or_404(Post, thread__id=self.kwargs['thread_id'], thread__category=self.category_instance, pk=self.kwargs['post_id'])

    def check_permissions(self, request):
        self.object = self.get_object()
        
        return self.check_moderator_permissions(request, self.category_instance, self.object.thread)
        
    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        context.update({
            'category_instance': self.category_instance,
            'thread_instance': self.object.thread,
            'post_instance': self.object,
        })
        return context

    def get_success_url(self):
        return reverse('forum:thread-details', args=(self.category_instance.slug, self.object.id))
