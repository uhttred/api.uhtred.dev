from urllib.parse import urlencode

from django.db import models
from django.utils.translation import get_language

from uhtred.core.configs import conf
from uhtred.core.postmark import client

from uhtred.insight.serializers import InsightDetail
from uhtred.insight.models import Insight
from .models import Email


EMAIL_FROM = 'Uhtred M <noreply@uhtred.dev>'


def send_newsletter_confirmation_email(email: Email) -> None:

    template = conf.postmark_email_template.email_confirmation
    language = email.preferred_language or get_language()[:2] or ''
    template_id = template.get(language, template['en'])

    model = {
        'name_or_email': email.name or email.email,
        'email_confirmation_link': '{appUrl}/{language}?{query_params}'.format(
            appUrl=conf.app_base_url,
            language='pt/' if language == 'pt' else '',
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


def send_newsletter_article_published(insight: Insight) -> None:

    active_language = get_language()[:2]
    template = conf.postmark_email_template.insight_published

    queryset: models.QuerySet[Email] = Email.objects.all_by_topics(
        topics=insight.topics.all())

    messages = []
    insight_data = InsightDetail(
        insight,
        fields=[
            'title',
            'pt_title',
            'pt_description',
            'description'
        ]
    ).data

    utm_source = 'uhtred_newsletter_insight_%d' % insight.id

    for email in queryset.all():

        language = email.preferred_language or active_language

        messages.append({
            'TemplateId': template.get(language, template['en']),
            'From': 'Uhtred M <newsletter@uhtred.dev>',
            'To': email.email,
            'Tag': 'Insight Published',
            'TemplateModel': {
                'name_or_email': email.name or email.email,
                'insight': insight_data,
                'insight_link': '{appUrl}/{language}insights/{slug}?{query_params}'.format(
                    appUrl=conf.app_base_url,
                    language='pt/' if language == 'pt' else '',
                    slug=insight.slug,
                    query_params=urlencode({
                        'utm_source': utm_source,
                        'utm_medium': 'email',
                        'utm_campaign': 'insight_published'
                    })
                ),
                'email_unsubscribe_link': '{apiUrl}/notify/emails/{uid}/unsubscribe?{query_params}'.format(
                    apiUrl=conf.api_base_url,
                    uid=email.uid,
                    query_params=urlencode({
                        'email': email.email,
                    })
                ),
                'email_preferences_link': '{appUrl}/{language}?{query_params}'.format(
                    appUrl=conf.app_base_url,
                    language='pt/' if language == 'pt' else '',
                    query_params=urlencode({
                        'newsletter-preferences': 'yes',
                        'email': email.email,
                        'sign': email.uid
                    })
                )
            }
        })

    if messages:
        client.emails.send_template_batch(
            *messages)
