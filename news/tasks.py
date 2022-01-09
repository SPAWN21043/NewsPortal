from datetime import datetime, timedelta
import logging
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from celery import shared_task
from collections import defaultdict
from news.models import Post
from django.utils import timezone


logger = logging.getLogger(__name__)


@shared_task
def send_post_mail(name_post, post_id, post_preview, to_mail):
    '''if isinstance(to_mail, str):
        post_mail = [to_mail, ]
    else:
        post_mail = to_mail'''

    subject = 'В категориях, на которые вы подписаны появилась новая статья:'
    text_content = f'Появилась новая статья: {name_post}\n' \
                   f'Ссылка на новость: http://127.0.0.1:8000/news/{post_id}\n' \
                   f'Краткое содержание: {post_preview}'
    email_send = settings.EMAIL_FROM
    html_save = render_to_string('send_post.html', {'subject': subject, 'heading': name_post, 'preview': post_preview, 'post_id': post_id})

    '''send_mail(subject, text_content, email_send, post_mail)'''

    msg = EmailMultiAlternatives(subject, text_content, email_send, to=to_mail)

    msg.attach_alternative(html_save, "text/html")
    msg.send()


@shared_task
def mail_monday():

    last_week_post_qs = Post.objects.filter(date_create__gte=datetime.now(tz=timezone.utc) - timedelta(days=7))

    posts_for_user = defaultdict(set)  # user -> posts

    for post in last_week_post_qs:
        for category in post.categ.all():
            for user in category.subscr_user.all():
                posts_for_user[user].add(post)

    # непосредственно рассылка
    for user, posts in posts_for_user.items():
        email_list = user.email
        posts = posts

    if isinstance(email_list, str):
        subscribers_list = [email_list, ]
    else:
        subscribers_list = email_list

    email_from = settings.EMAIL_FROM  # в settings должно быть заполнено
    subject = 'В категориях, на которые вы подписаны появились новые статьи'
    text_message = 'В категориях, на которые вы подписаны появились новые статьи'

    # рендерим в строку шаблон письма и передаём туда переменные, которые в нём используем
    render_html_template = render_to_string('send_posts_list.html', {'posts': posts, 'subject': subject})

        # формируем письмо
    msg = EmailMultiAlternatives(subject, text_message, email_from, list(subscribers_list))
        # прикрепляем хтмл-шаблон
    msg.attach_alternative(render_html_template, 'text/html')
        # отправляем
    msg.send()

