from typing import Optional

from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.db import transaction
from core.models import Post


class PostService:
    @staticmethod
    def get_likes_count(obj):
        return obj.liked_by.count()

    @staticmethod
    def create_or_update(user, image_name: str, image_content: bytes, caption: str):
        ext = image_name.split(".")[-1].lower()
        with transaction.atomic():
            post, created = Post.objects.update_or_create(user=user, caption=caption)
            if not created:
                post.image.delete(save=False)
            file_name = f"{post.pk}.{ext}"
            post.image.save(file_name, ContentFile(image_content), save=True)
        return post

    @staticmethod
    def delete(user, post_id: int):
        post = Post.objects.get(pk=post_id)
        if post.user != user:
            raise PermissionDenied("Cannot delete someone elses post")
        post.delete()

    @staticmethod
    def edit(
        post_id: int,
        image_name: Optional[str] = None,
        image_content: Optional[bytes] = None,
        caption: Optional[str] = None,
    ):
        post = Post.objects.get(pk=post_id)
        if caption:
            post.caption = caption
        if image_name and image_content:
            ext = image_name.split(".")[-1].lower()
            file_name = f"{post.pk}.{ext}"
            post.image.delete(save=False)
            post.image.save(file_name, ContentFile(image_content), save=True)
        post.save()
