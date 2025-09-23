from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
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
    def delete(user, comment_id):
        comment = Comment.objects.get(id=comment_id)
        post = comment.post
        if post.user != user or comment.user != user:
            PermissionDenied("Can't delete a comment you dont own")
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()

    @staticmethod
    def get_all(post_id):
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()  # pyright: ignore
