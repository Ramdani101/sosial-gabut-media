from django.shortcuts import render, get_object_or_404, redirect
from .models import Postingan, Suka, Komentar
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count
import json

def index(request):
    if request.method == "POST":
        konten = request.POST.get("konten")
        user_id = 1
        if konten and user_id:
            Postingan.objects.create(
                konten=konten, user_id=user_id, pub_date=timezone.now()
            )
            return redirect("home:index")
    postingan = Postingan.objects.annotate(jumlah_komentar=Count('comments')).order_by("-pub_date")
    liked_post_id = Suka.objects.filter(user_id=1).values_list("post_id", flat=True)
    return render(
        request,
        "home/index.html",
        {"postingan": postingan, "liked_post_id": liked_post_id},
    )


def like_post(request, id):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        post = get_object_or_404(Postingan, id=id)
        like, created = Suka.objects.get_or_create(user_id=1, post_id=post)

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