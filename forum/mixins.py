"""
Common forum mixins
"""
from django.conf import settings
from django.db.models import Count
from django.shortcuts import render_to_response
from django.template import RequestContext, TemplateDoesNotExist
from django.core.exceptions import PermissionDenied

from braces.views import PermissionRequiredMixin, MultiplePermissionsRequiredMixin

class ModeratorCheckMixin(object):
    """
    Mixin to include checking for moderator permission on category or thread
    """
    permission_required = ['forum.moderate_category', 'forum.moderate_thread']
    
    def check_moderator_permissions(self, request):
        """
        Check if user have global or per object permission (on category 
        instance and on thread instance), finally return a 403 response if no 
        permissions has been finded.
        
        If a permission has been finded, return False, then the dispatcher 
        should so return the "normal" response from the view.
        """
        has_perms = self.has_moderator_permissions(request)
        
        # Return a forbidden response if no permission has been finded
        if not has_perms:
            raise PermissionDenied
        
        return False
    
    def has_moderator_permissions(self, request):
        """
        Find if user have global or per object permission firstly on category instance, 
        if not then on thread instance
        """
        return any(request.user.has_perm(perm) for perm in self.permission_required)


class ModeratorRequiredMixin(MultiplePermissionsRequiredMixin):
    """
    """
    permissions = {
        "any": ('forum.moderate_category', 'forum.moderate_thread')
    }


class ThreadQuerysetFiltersMixin(object):
    """
    Just a mixin to add common Thread list filters (not for detail views)
    """
    def get_queryset(self, *args, **kwargs):
        q = super(ThreadQuerysetFiltersMixin, self).get_queryset(*args, **kwargs)
        return q.filter(category__visible=True, visible=True).annotate(num_posts=Count('post')).select_related().order_by('-sticky', '-modified')
