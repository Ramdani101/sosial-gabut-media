from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from home.models import Postingan, Suka, Komentar
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count
from friend.models import Friend
from django.db.models import Q
import json

def post(request, id):
    user_profile = get_object_or_404(User, id=id)
    user_posts = Postingan.objects.filter(user=user_profile).order_by('-created_at')

    friend_ids = Friend.objects.filter(
        Q(user=user_profile, status='accepted') | 
        Q(friend_username=user_profile, status='accepted')
    ).values_list('user__id', 'friend_username__id')
    
    friend_ids_flat = set()
    for u, f in friend_ids:
        friend_ids_flat.add(u)
        friend_ids_flat.add(f)
    friend_ids_flat.discard(user_profile.id)  # Jangan masukkan diri sendiri

    friends = User.objects.filter(id__in=friend_ids_flat)
    total_friends = friends.count()
    return render(
        request,
        "profileinfo/post.html",
        {
            "user_profile": user_profile,
            "user_posts": user_posts,
            "total_friends": total_friends,
        }
    )

def friend(request, id):
    user_profile = get_object_or_404(User, id=id)
    # Ambil semua user yang sudah berteman dua arah (accepted)
    friend_ids = Friend.objects.filter(
        Q(user=user_profile, status='accepted') | 
        Q(friend_username=user_profile, status='accepted')
    ).values_list('user__id', 'friend_username__id')

    friend_ids_flat = set()
    for u, f in friend_ids:
        friend_ids_flat.add(u)
        friend_ids_flat.add(f)
    friend_ids_flat.discard(user_profile.id)  # Jangan masukkan diri sendiri

    friends = User.objects.filter(id__in=friend_ids_flat)
    total_friends = friends.count()

    return render(request, "profileinfo/friend.html", {
        "user_profile": user_profile,
        "friends": friends,
        "total_friends": total_friends,
    })

def like_post(request, id):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        post = get_object_or_404(Postingan, id=id)
        like, created = Suka.objects.get_or_create(user_id=request.user.id, post_id=post)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        total_likes = Suka.objects.filter(post_id=post).count()
        return JsonResponse(
            {
                "status": "ok",
                "liked": liked,
                "total_likes": total_likes,
            }
        )
    return JsonResponse({"status": "error"}, status=400)


def share_post(request, id):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        post = get_object_or_404(Postingan, id=id)
        post.total_share += 1
        post.save()
        total_shares = post.total_share
        return JsonResponse(
            {
                "status": "ok",
                "total_shares": total_shares,
            }
        )
    return JsonResponse({"status": "error"}, status=400)

def get_post_comment(request, id):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        post = Postingan.objects.get(id=id)
        comments = Komentar.objects.filter(post_id=post)
        total_like = Suka.objects.filter(post_id=post).count()
        total_comments = comments.count()
        return JsonResponse(
            {
                "post": {
                    "konten": post.konten,
                    "total_share": post.total_share,
                    "pub_date": post.pub_date.strftime("%Y-%m-%d %H:%M"),
                    "total_like": total_like,
                    "total_comment": total_comments,
                },
                "comments": [
                    {
                        "komentar": comment.komentar,
                        "user_id": comment.user_id,
                        "pub_date": comment.pub_date.strftime("%Y-%m-%d %H:%M"),
                    }
                    for comment in comments
                ],
            }
        )
    return JsonResponse({"error": "Bad request"}, status=400)

def comment_post(request, id):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        body_unicode = request.body.decode('utf-8')   
        body_data = json.loads(body_unicode)            
        komentar = body_data.get('komentar') 
        post = get_object_or_404(Postingan, id=id)
        comment = Komentar.objects.create(user_id=1, post_id=post, komentar=komentar, pub_date=timezone.now())
        post.total_share += 1
        post.save()
        comment.save()
        commentsData = Komentar.objects.filter(post_id=post)

        return JsonResponse(
            {
                "comments": [
                    {
                        "komentar": comment.komentar,
                        "user_id": comment.user_id,
                        "pub_date": comment.pub_date.strftime("%Y-%m-%d %H:%M"),
                    }
                    for comment in commentsData
                ],
            }
        )
    return JsonResponse({"status": "error"}, status=400)