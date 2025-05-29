from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Friend
from django.template import loader
from django.utils import timezone

def friend(request):
    return render(request, "friend/friends.html")

def friend_list(request, user_id):
    try:
        current_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    # Ambil teman yang sudah diterima (status='accepted')
    friends = Friend.objects.filter(user=current_user, status='accepted')

    # Ambil permintaan pertemanan tertunda yang diterima oleh current_user
    pending_requests = Friend.objects.filter(friend_username=current_user, status='pending')

    # Ambil semua pengguna yang belum mengirim permintaan, bukan teman, dan belum dikirimi permintaan oleh current_user
    friend_ids = friends.values_list('friend_username__id', flat=True)  # ID teman yang sudah diterima
    pending_sender_ids = pending_requests.values_list('user__id', flat=True)  # ID pengirim permintaan tertunda
    pending_receiver_ids = Friend.objects.filter(user=current_user, status='pending').values_list('friend_username__id', flat=True)  # ID yang sudah dikirimi permintaan
    alluser = User.objects.exclude(id=user_id).exclude(id__in=friend_ids).exclude(id__in=pending_sender_ids).exclude(id__in=pending_receiver_ids)

    # Tangani penambahan teman, penerimaan, atau penolakan permintaan
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_friend":
            friend_id = request.POST.get("friend_id")
            try:
                friend_user = User.objects.get(id=friend_id)
                Friend.objects.get_or_create(
                    user=current_user,
                    friend_username=friend_user,
                    defaults={'status': 'pending'}
                )
            except User.DoesNotExist:
                return HttpResponse("Selected user not found", status=404)
        elif action == "accept_request":
            request_id = request.POST.get("request_id")
            try:
                friend_request = Friend.objects.get(id=request_id, friend_username=current_user, status='pending')
                friend_request.status = 'accepted'
                friend_request.accepted_at = timezone.now()
                friend_request.save()
            except Friend.DoesNotExist:
                return HttpResponse("Friend request not found", status=404)
        elif action == "reject_request":
            request_id = request.POST.get("request_id")
            try:
                friend_request = Friend.objects.get(id=request_id, friend_username=current_user, status='pending')
                friend_request.status = 'rejected'
                friend_request.accepted_at = None
                friend_request.save()
            except Friend.DoesNotExist:
                return HttpResponse("Friend request not found", status=404)
        return redirect('friend:friend_list', user_id=user_id)

    template = loader.get_template("friend/friend_lists.html")
    context = {
        'friends': friends,
        'pending_requests': pending_requests,
        'alluser': alluser,
        'current_user': current_user,
    }
    return HttpResponse(template.render(context, request))
