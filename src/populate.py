import random
import requests
import logging
from django.core.files.base import ContentFile
from django.db import transaction
from core.models import User, Post, Comment
from django.utils.text import slugify

NUM_USERS = 10
POSTS_PER_USER = 20
MAX_FOLLOWERS_PER_USER = 7
MAX_LIKES_PER_POST = 10
MAX_COMMENTS_PER_POST = 5
IMAGE_RETRIES = 3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def DUMMY_POST_IMAGE_API(x):
    return f"https://picsum.photos/seed/{x}/600/400"


def USER_AVATAR_API():
    return f"https://randomuser.me/api/portraits/lego/{random.randint(0, 9)}.jpg"


def download_image(url):
    for attempt in range(IMAGE_RETRIES):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return ContentFile(r.content)
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
    return None


def populate():
    with transaction.atomic():
        # Step 1: Create users
        user_objs = [
            User(
                email=f"user{i}@example.com", username=f"user{i}", bio=f"Bio of user{i}"
            )
            for i in range(NUM_USERS)
        ]
        User.objects.bulk_create(user_objs)
        users = list(User.objects.all().order_by("id")[:NUM_USERS])
        logger.info(f"Created {len(users)} users.")

        # Step 2: Set passwords and save avatars
        for i, user in enumerate(users):
            user.set_password(f"password{i}")
            user.save(update_fields=["password"])

            avatar_url = USER_AVATAR_API()
            avatar_content = download_image(avatar_url)
            if avatar_content:
                filename = f"{user.pk}/profile.jpg"
                if user.avatar:
                    user.avatar.delete(save=False)
                user.avatar.save(filename, avatar_content, save=True)
            logger.info(f"user {i} avatar saved")

        # Step 3: Create follower relationships
        for user in users:
            k = random.randint(0, min(MAX_FOLLOWERS_PER_USER, len(users)))
            followers = random.sample(users, k=k)
            for follower in followers:
                if follower != user:
                    user.followers.add(follower)
                    logger.info(f"{follower.pk} -> {user.pk}")
        logger.info("Followers relationships created.")

        # Step 4: Create posts
        post_objs = []
        for user in users:
            for p in range(POSTS_PER_USER):
                caption = f"Post {p} by {user.username}"
                post_objs.append(Post(user=user, caption=caption))
        Post.objects.bulk_create(post_objs)
        posts = list(Post.objects.order_by("-id")[: len(post_objs)])
        posts.reverse()
        logger.info(f"Created {len(posts)} posts.")

        # Step 5: Download and save post images
        for post in posts:
            seed = f"{post.user.pk}-{post.pk}-{random.randint(0, 10000)}"
            image_url = DUMMY_POST_IMAGE_API(slugify(seed))
            image_content = download_image(image_url)
            if image_content:
                filename = f"{post.user.pk}/posts/{seed}.jpg"
                if post.image:
                    post.image.delete(save=False)
                post.image.save(filename, image_content, save=True)

        logger.info("Post images saved.")

        # Step 6: Likes and comments
        comment_objs = []
        for post in posts:
            likers = random.sample(
                users, k=random.randint(0, min(MAX_LIKES_PER_POST, len(users)))
            )
            post.liked_by.add(*likers)
            post.likes_count = post.liked_by.count()

            for _ in range(random.randint(0, MAX_COMMENTS_PER_POST)):
                commenter = random.choice(users)
                comment_objs.append(
                    Comment(
                        user=commenter,
                        post=post,
                        text=f"This is a comment by {commenter.username} on post {post.pk}",
                    )
                )

            post.comments_count = post.comments.count()
            post.save(update_fields=["likes_count", "comments_count"])

        Comment.objects.bulk_create(comment_objs)
        logger.info("Likes and comments created.")

    logger.info("Database population complete!")
