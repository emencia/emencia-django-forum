"""
Forum signals
"""
from django.conf import settings
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

def new_message_posted_receiver(sender, **kwargs):
    post_instance = kwargs['post_instance']
    threadwatchs = kwargs['threadwatchs']
    emails_datas = []
    
    subject = message = "New message #{0} has been posted on thread: {1}".format(post_instance.id, post_instance.thread)
    
    # Template context to build subject and content
    context = {
        'SITE': Site.objects.get_current(),
        'thread_instance': post_instance.thread,
        'post_instance': post_instance,
    }
    subject = ''.join(render_to_string('forum/threadwatch_email_subject.txt', context).splitlines())
    content = render_to_string('forum/threadwatch_email_content.txt', context)
    
    for item in threadwatchs:
        #print "*", item, "for", item.owner
        # (subject, message, from_email, recipient_list)
        emails_datas.append((
            subject,
            content,
            settings.FORUM_EMAIL_SENDER or settings.DEFAULT_FROM_EMAIL,
            [item.owner.email],
        ))
        
    send_mass_mail(tuple(emails_datas), fail_silently=settings.DEBUG)
