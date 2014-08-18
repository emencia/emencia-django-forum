"""
Forum signals
"""
def new_message_posted_receiver(sender, **kwargs):
    message = kwargs['post_instance']
    threadwatchs = kwargs['threadwatchs']
    
    print "New message #{0} has been posted on thread:".format(message.id), message.thread
    
    for item in threadwatchs:
        print "*", item, "for", item.owner
