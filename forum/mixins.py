"""
Common forum mixins
"""
from django.conf import settings
from django.db.models import Count
from django.shortcuts import render_to_response
from django.template import RequestContext, TemplateDoesNotExist

from guardian.conf import settings as guardian_settings
from guardian.mixins import PermissionRequiredMixin as PerObjectPermissionRequiredMixin

class ModeratorRequiredMixin(PerObjectPermissionRequiredMixin):
    """
    Mixin to check for moderator permission on category or thread (if not present for category)
    
    Inherit from ``guardian.mixins.PermissionRequiredMixin`` so you'll need to override the ``check_permissions`` method to add usage of ``ModeratorRequiredMixin.check_moderator_permissions`` or to remove the default ``PermissionRequiredMixin.check_permissions`` behavior.
    
    If you don't do this ``ModeratorRequiredMixin.check_moderator_permissions`` will not be used by default.
    """
    permission_required = ['forum.moderate_category', 'forum.moderate_thread']
    
    def check_moderator_permissions(self, request, category_instance, thread_instance):
        """
        Check if user have global or per object permission (on category 
        instance and on thread instance), finally return a 403 response if no 
        permissions has been finded.
        
        If a permission has been finded, return False, then the dispatcher 
        should so return the "normal" response from the view.
        """
        has_perms = self.has_moderator_permissions(request, category_instance, thread_instance)
        
        # Return a forbidden response if no permission has been finded
        if not has_perms:
            try:
                response = render_to_response(getattr(guardian_settings, 'TEMPLATE_403', '403.html'), {}, RequestContext(request))
                response.status_code = 403
                return response
            except TemplateDoesNotExist as e:
                if settings.DEBUG:
                    raise e
        
        return False
    
    def has_moderator_permissions(self, request, category_instance, thread_instance):
        """
        Find if user have global or per object permission firstly on category instance, 
        if not then on thread instance
        """
        perms = self.get_required_permissions(request)

        # global perms check (from "ModeratorRequiredMixin.permission_required")
        if any(request.user.has_perm(perm) for perm in perms):
            return "global"
        
        # Try Category per-object permission
        if any(request.user.has_perm(perm, category_instance) for perm in perms):
            return "per-object.category"
            
        # Try Thread per-object permission
        if any(request.user.has_perm(perm, thread_instance) for perm in perms):
            return "per-object.thread"
        
        # no permission at all has been finded
        return False


class ThreadQuerysetFiltersMixin(object):
    """
    Just a mixin to add common Thread list filters (not for detail views)
    """
    def get_queryset(self, *args, **kwargs):
        q = super(ThreadQuerysetFiltersMixin, self).get_queryset(*args, **kwargs)
        return q.filter(category__visible=True, visible=True).annotate(num_posts=Count('post')).select_related().order_by('-sticky', '-modified')
