from django import template

register = template.Library()


@register.filter
def board_posts(board):
    posts = 0
    for thread in board.threads.all():
        posts += thread.posts.count()

    return posts