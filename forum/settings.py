"""
Default Forum settings to import/define in your project settings
"""

# Categories pagination in 'Category index' (=forum index) view
FORUM_CATEGORY_INDEX_PAGINATE = 6
# Threads pagination in 'Last threads' view
FORUM_LAST_THREAD_PAGINATE = 15
# Threads pagination in 'Category detail' view
FORUM_CATEGORY_THREAD_PAGINATE = 20
# Messages pagination in 'Thread detail' view
# TODO: Actually to None because pagination cause troubles with Post.get_absolute_url
FORUM_THREAD_DETAIL_PAGINATE = None
