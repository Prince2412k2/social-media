from django.core.exceptions import PermissionDenied
from core.models import Comment, Post


class CommentService:
    @staticmethod
    def create_or_update(user, post_id, text):
        post = Post.objects.get(pk=post_id)
        comment, created = Comment.objects.get_or_create(
            user=user,
            post=post,
            text=text,
        )
        return comment

    @staticmethod
    def delete(user, post_id, comment_id):
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.get(id=comment_id)
        if post.user != user or comment.user != user:
            PermissionDenied("Can't delete a comment you dont own")
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
