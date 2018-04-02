from django import template

register = template.Library()


@register.filter
def board_posts(board):
    posts = 0
    for thread in board.threads.all():
        posts += thread.posts.count()

    return posts


@register.simple_tag
def last_post_time(thread):
    last_post = thread.posts.all().order_by('created_date').last()

    return last_post.created_date.strftime('%d/%m/%y, %H:%M')
