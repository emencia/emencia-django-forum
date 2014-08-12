from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy

site.update({
    'forum:index': ugettext_lazy("Forum"),
    'forum:category-details': ugettext_lazy('<small class="subhead">Category</small> {{ category_instance.title }}'),
    'forum:category-create': ugettext_lazy('New category'),
    'forum:category-edit': ugettext_lazy('<small class="subhead">{{ category_instance.title }}</small> Edit'),
    'forum:thread-recent': ugettext_lazy('Recent threads'),
    'forum:thread-details': ugettext_lazy('<small class="subhead">{{ category_instance.title }}</small> {{ thread_instance.subject }}'),
    'forum:thread-create': ugettext_lazy('<small class="subhead">{{ category_instance.title }}</small> New thread'),
    'forum:thread-edit': ugettext_lazy('<small class="subhead">{{ thread_instance.subject }}</small> Thread edit'),
    'forum:post-edit': ugettext_lazy('<small class="subhead">{{ thread_instance.subject }}</small> Edit message #{{ post_instance.id }}'),
})