# -*- coding: utf-8 -*-
"""
Vues des messages de fils
"""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views import generic

from braces.views import LoginRequiredMixin

from forum.mixins import ModeratorCheckMixin, ModeratorRequiredMixin

from forum.models import Category, Post

from forum.forms.post import PostEditForm, PostDeleteForm


class PostRedirectView(LoginRequiredMixin, generic.RedirectView):
    """
    View to find and redirect to the exact page where is the Post
    """
    permanent = False

    def get_redirect_url(self, **kwargs):
        post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return post_instance.get_absolute_url()
    

#class PostEditView(ModeratorRequiredMixin, generic.UpdateView):
class PostEditView(LoginRequiredMixin, ModeratorCheckMixin, generic.UpdateView):
    """
    Message edit view
    
    Restricted to message owner and moderators
    """
    model = Post
    form_class = PostEditForm
    template_name = 'forum/post/form.html'
    context_object_name = "post_instance"
    
    def get_object(self, *args, **kwargs):
        """
        Should memoize the object to avoid multiple query if get_object is used many times in the view
        """
        self.category_instance = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return get_object_or_404(Post, thread__id=self.kwargs['thread_id'], thread__category=self.category_instance, pk=self.kwargs['post_id'])

    def check_permissions(self, request):
        self.object = self.get_object()
        
        # Owner can edit its posts if FORUM_OWNER_MESSAGE_CAN_EDIT setting is True
        if settings.FORUM_OWNER_MESSAGE_CAN_EDIT and self.object.author == request.user:
            return False
            
        return self.check_moderator_permissions(request)
        
    def get_context_data(self, **kwargs):
        context = super(PostEditView, self).get_context_data(**kwargs)
        context.update({
            'FORUM_TEXT_FIELD_JS_TEMPLATE': settings.FORUM_TEXT_FIELD_JS_TEMPLATE,
            'FORUM_TEXT_MARKUP_RENDER_TEMPLATE': settings.FORUM_TEXT_MARKUP_RENDER_TEMPLATE,
            'category_instance': self.category_instance,
            'thread_instance': self.object.thread,
        })
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()
    
    def get(self, *args, **kwargs):
        self.check_permissions(self.request)
        return super(PostEditView, self).get(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        self.check_permissions(self.request)
        return super(PostEditView, self).post(*args, **kwargs)

#class PostDeleteView(ModeratorRequiredMixin, generic.UpdateView):
class PostDeleteView(LoginRequiredMixin, ModeratorRequiredMixin, generic.UpdateView):
    """
    Message delete view, without any confirm
    
    Restricted to moderators only
    """
    model = Post
    form_class = PostDeleteForm
    template_name = 'forum/post/delete_form.html'
    
    def get_object(self, *args, **kwargs):
        self.category_instance = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return get_object_or_404(Post, thread__id=self.kwargs['thread_id'], thread__category=self.category_instance, pk=self.kwargs['post_id'])
        
    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        context.update({
            'FORUM_TEXT_FIELD_JS_TEMPLATE': settings.FORUM_TEXT_FIELD_JS_TEMPLATE,
            'FORUM_TEXT_MARKUP_RENDER_TEMPLATE': settings.FORUM_TEXT_MARKUP_RENDER_TEMPLATE,
            'category_instance': self.category_instance,
            'thread_instance': self.object.thread,
            'post_instance': self.object,
        })
        return context

    def get_success_url(self):
        return reverse('forum:thread-details', args=(self.category_instance.slug, self.object.id))
