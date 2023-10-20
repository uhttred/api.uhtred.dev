from django.conf import settings

from postmarker.core import PostmarkClient


client = PostmarkClient(
    server_token=settings.POSTMARK_SERVER_TOKEN,
    verbosity=3)


# client.emails.send_template_batch(u1, u2)


