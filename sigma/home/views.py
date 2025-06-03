from django.shortcuts import render, get_object_or_404, redirect
from .models import Postingan, Suka, Komentar
from friend.models import Friend
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models import Q
import json

def index(request):
    if request.method == "POST":
        konten = request.POST.get("konten")
        user = request.user
        if konten and user.is_authenticated:
            Postingan.objects.create(
                user=user,
                uploader_name=user.username,
                uploader_image=user.profile.image.url,
                konten=konten,
                pub_date=timezone.now()
            )
            return redirect("home:index")
    postingan = Postingan.objects.annotate(jumlah_komentar=Count('comments')).order_by("-pub_date")
    liked_post_id = Suka.objects.filter(user_id=request.user.id).values_list("post_id", flat=True) if request.user.is_authenticated else []
    if request.user.is_authenticated:
        # Ambil semua user yang sudah berteman accepted dua arah
        friend_ids = Friend.objects.filter(
            Q(user=request.user, status='accepted') | 
            Q(friend_username=request.user, status='accepted')
        ).values_list('user__id', 'friend_username__id')

        friend_ids_flat = set()
        for u, f in friend_ids:
            friend_ids_flat.add(u)
            friend_ids_flat.add(f)
        friend_ids_flat.discard(request.user.id)  # Jangan masukkan diri sendiri

        friends = User.objects.filter(id__in=friend_ids_flat)
    else:
        friends = User.objects.none()

    return render(
        request,
        "home/index.html",
        {"postingan": postingan, "liked_post_id": liked_post_id, "friends": friends},
    )


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
                    "username": post.user.username,
                    "profile_image": post.user.profile.image.url,
                },
                "comments": [
                    {
                        "komentar": comment.komentar,
                        "user_id": comment.user.id,
                        "pub_date": comment.pub_date.strftime("%Y-%m-%d %H:%M"),
                        "username": comment.user.username,
                        "profile_image": comment.user.profile.image.url,
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
        comment = Komentar.objects.create(user=request.user, post_id=post, komentar=komentar, pub_date=timezone.now())
        post.total_share += 1
        post.save()
        comment.save()
        commentsData = Komentar.objects.filter(post_id=post)

        return JsonResponse(
            {
                "comments": [
                    {
                        "komentar": comment.komentar,
                        "user_id": comment.user.id,
                        "username": comment.user.username,
                        "profile_image": comment.user.profile.image.url,
                        "pub_date": comment.pub_date.strftime("%Y-%m-%d %H:%M"),
                    }
                    for comment in commentsData
                ],
            }
        )
    return JsonResponse({"status": "error"}, status=400)