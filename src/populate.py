import random
import requests
from django.core.files.base import ContentFile
from django.db import transaction
from core.models import User, Credential, Post, Comment
from django.utils.text import slugify

NUM_USERS = 10  # Updated here
POSTS_PER_USER = 20
MAX_FOLLOWERS_PER_USER = 7
MAX_LIKES_PER_POST = 10
MAX_COMMENTS_PER_POST = 5


def DUMMY_POST_IMAGE_API(x):
    return f"https://picsum.photos/seed/{x}/600/400"


def download_image(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return ContentFile(r.content)
    except Exception as e:
        print(f"Failed to download image {url}: {e}")
        return None


def populate():
    with transaction.atomic():
        # Step 1: Create users without avatars
        user_objs = [
            User(
                email=f"user{i}@example.com", username=f"user{i}", bio=f"Bio of user{i}"
            )
            for i in range(NUM_USERS)
        ]
        User.objects.bulk_create(user_objs)

        # Refresh users from DB to get pks
        users = list(User.objects.all().order_by("id")[:NUM_USERS])
        print(f"Created {len(users)} users.")

        # Step 2: Set passwords and save avatars
        for i, user in enumerate(users):
            user.set_password(f"password{i}")
            user.save(update_fields=["password"])

            avatar_url = (
                f"https://randomuser.me/api/portraits/lego/{random.randint(0, 9)}.jpg"
            )
            avatar_content = download_image(avatar_url)
            if avatar_content:
                filename = f"{user.pk}/profile.jpg"
                if user.avatar:
                    user.avatar.delete(save=False)
                user.avatar.save(filename, avatar_content, save=True)
            print(f"user {i} avatar saved")

        # Step 3: Create follower relations
        for user in users:
            followers = random.sample(
                users, k=random.randint(0, MAX_FOLLOWERS_PER_USER)
            )
            for follower in followers:
                if follower != user:
                    user.followers.add(follower)
                    print(f"{follower.id} -> {user.pk}")

        print("Followers relationships created.")

        # Step 4: Create posts without images in bulk
        post_objs = []
        for user in users:
            for p in range(POSTS_PER_USER):
                seed = f"{user.pk}-{p}-{random.randint(0, 10000)}"
                caption = f"Post {p} by {user.username}"
                post_objs.append(Post(user=user, caption=caption))
        Post.objects.bulk_create(post_objs)

        # Get last created posts in correct order
        posts = list(Post.objects.order_by("-id")[: len(post_objs)])
        posts.reverse()
        print(f"Created {len(posts)} posts.")

        # Step 5: Download images and save to posts
        for post in posts:
            seed = f"{post.user.pk}-{post.pk}-{random.randint(0, 10000)}"
            image_url = DUMMY_POST_IMAGE_API(slugify(seed))
            image_content = download_image(image_url)
            if image_content:
                filename = f"{post.user.pk}/posts/{seed}.jpg"
                if post.image:
                    post.image.delete(save=False)
                post.image.save(filename, image_content, save=True)

        # Step 6: Add likes and create comments
        comment_objs = []
        for post in posts:
            likers = random.sample(users, k=random.randint(0, MAX_LIKES_PER_POST))
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

        # Bulk create all comments
        Comment.objects.bulk_create(comment_objs)
        print("Likes and comments created.")

    print("Database population complete!")
