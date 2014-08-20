"""
Default Forum settings to import/define in your project settings
"""

# Categories pagination in 'Category index' (=forum index) view
FORUM_CATEGORY_INDEX_PAGINATE = 6
# Threads pagination in 'Last threads' view
FORUM_LAST_THREAD_PAGINATE = 15
# Threads pagination in 'Category detail' view
FORUM_CATEGORY_THREAD_PAGINATE = 15
# Messages pagination in 'Thread detail' view
FORUM_THREAD_DETAIL_PAGINATE = 10

# If True message owner can edit its text, else only admin/moderate
FORUM_OWNER_MESSAGE_CAN_EDIT = True

FORUM_NEW_POST_SIGNAL = 'forum.signals.new_message_posted_receiver'

# Specific email sender address, if None 
FORUM_EMAIL_SENDER = None

# Add new specific "rstview" parser settings for Forum app, if you have other apps 
# that define parser settings this can lead to overwrite problems . In this 
# case, just defined all parser setting in the same 
# 'RSTVIEW_PARSER_FILTER_SETTINGS' in your project settings
RSTVIEW_PARSER_FILTER_SETTINGS = {
    'forum_message':{
        'initial_header_level': 5,
        'file_insertion_enabled': False,
        'raw_enabled': False,
        'footnote_references': 'superscript',
        'doctitle_xform': False,
    },
}
