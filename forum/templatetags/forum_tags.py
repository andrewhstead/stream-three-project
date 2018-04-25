from django import template

register = template.Library()


# Count the number of posts in a given board on the forum.
@register.filter
def board_posts(board):
    posts = 0
    for thread in board.threads.all():
        posts += thread.posts.count()

    return posts
