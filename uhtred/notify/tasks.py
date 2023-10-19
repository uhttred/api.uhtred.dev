from urllib.parse import urlencode

from django.utils.translation import get_language

from uhtred.core.configs import conf
from uhtred.core.postmark import client

from .models import Email


EMAIL_FROM = 'Uhtred M <noreply@uhtred.dev>'


def send_newsletter_confirmation_email(email: Email) -> None:

    # pt_template_id = 33542968
    # en_template_id = 33543094

    template = {'pt': 33542968, 'en': 33543094}
    language = email.preferred_language or get_language()[:2] or ''
    template_id = template.get(language, template['en'])

    model = {
        'name_or_email': email.name or email.email,
        'email_confirmation_link': '{appUrl}/{language}?{query_params}'.format(
            appUrl=conf.app_base_url,
            language=language,
            query_params=urlencode({
                'newsletter-preferences': 'yes',
                'email-confirmation': 'yes',
                'email': email.email,
                'sign': email.uid
            })
        )
    }

    client.emails.send_with_template(
        TemplateId=template_id,
        To=email.email,
        From=EMAIL_FROM,
        Tag='Newsletter Confirmation',
        TemplateModel=model
    )
