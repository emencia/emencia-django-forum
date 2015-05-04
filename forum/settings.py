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

# If True threadwatch checkbox is checked in thread create and post create forms
FORUM_DEFAULT_THREADWATCH_CHECKBOX = False

# Receiver function for signal when a new Post is created
FORUM_NEW_POST_SIGNAL = 'forum.signals.new_message_posted_receiver'

# Specific email sender address, if None. Use in the default new Post signal receiver
FORUM_EMAIL_SENDER = None

# Add new specific "rstview" parser settings for Forum app, if you have other apps 
# that define parser settings this can lead to overwrite problems . In this 
# case, just define all parser setting in 'RSTVIEW_PARSER_FILTER_SETTINGS' in 
# the same settings file.
# WARNING: This should be removed, it must not be a default settings coming from forum
#          Add it as a note in markup install doc
RSTVIEW_PARSER_FILTER_SETTINGS = {
    'forum':{
        'initial_header_level': 5,
        'file_insertion_enabled': False,
        'raw_enabled': False,
        'footnote_references': 'superscript',
        'doctitle_xform': False,
    },
}

#
# Optionnal text markup settings
#

# Field helper for text in forms
FORUM_TEXT_FIELD_HELPER_PATH = None # Default, just a CharField
#FORUM_TEXT_FIELD_HELPER_PATH = "forum.markup.get_text_field" # Use DjangoCodeMirror

# Validator helper for Post.text in forms
FORUM_TEXT_VALIDATOR_HELPER_PATH = None # Default, no markup validation
#FORUM_TEXT_VALIDATOR_HELPER_PATH = "forum.markup.clean_restructuredtext" # Validation for RST syntax (with Rstview)

# Text markup renderer
FORUM_TEXT_MARKUP_RENDER_TEMPLATE = None # Default, just a CharField
#FORUM_TEXT_MARKUP_RENDER_TEMPLATE = "forum/markup/_text_markup_render.html" # Use Rstview renderer

# Template to init some Javascript for text in forms
FORUM_TEXT_FIELD_JS_TEMPLATE = None # Default, no JS template
#FORUM_TEXT_FIELD_JS_TEMPLATE = "forum/markup/_text_field_djangocodemirror_js.html" # Use DjangoCodeMirror

# Template to display author infos in thread's post list
FORUM_AUTHOR_VCARD_TEMPLATE = None # Default, only display the author username
#FORUM_AUTHOR_VCARD_TEMPLATE = "forum/author/_vcard.html" # Use Gravatar
