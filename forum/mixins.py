"""
Common forum mixins
"""
from django.db.models import Count
from django.http import HttpResponseForbidden

from guardian.mixins import PermissionRequiredMixin

class ModeratorRequiredMixin(PermissionRequiredMixin):
    """
    Mixin to check for moderator permission on category or thread (if not present for category)
    
    TODO: Use 'RENDER_403' behavior and not anymore HttpResponseForbidden
    """
    permission_required = ['forum.moderate_category', 'forum.moderate_thread']
    
    def check_moderator_permissions(self, request, category_instance, thread_instance):
        """
        Check if user have global or per object permission firstly on category instance, 
        if not then on thread instance
        """
        perms = self.get_required_permissions(request)

        # Category level
        has_category_permissions = False
        # global perms check first (if accept_global_perms)
        has_category_permissions = any(request.user.has_perm(perm) for perm in perms)
        # if still no permission granted, try obj perms
        if not has_category_permissions:
            has_category_permissions = any(request.user.has_perm(perm, category_instance) for perm in perms)
            
        # Thread level if category didn't match
        if not has_category_permissions:
            has_thread_permissions = False
            # global perms check first (if accept_global_perms)
            has_thread_permissions = any(request.user.has_perm(perm) for perm in perms)
            # if still no permission granted, try obj perms
            if not has_thread_permissions:
                has_thread_permissions = any(request.user.has_perm(perm, thread_instance) for perm in perms)
        
        # Raise a forbidden response if still no permission at all
        if not has_category_permissions and not has_thread_permissions:
            return HttpResponseForbidden()
        
        return False


class ThreadQuerysetFiltersMixin(object):
    """
    Just a mixin to add common Thread list filters (not for detail views)
    """
    def get_queryset(self, *args, **kwargs):
        q = super(ThreadQuerysetFiltersMixin, self).get_queryset(*args, **kwargs)
        return q.filter(category__visible=True, visible=True).annotate(num_posts=Count('post')).select_related().order_by('-sticky', '-modified')
