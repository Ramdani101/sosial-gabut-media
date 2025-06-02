from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Friend
from django.template import loader
from django.utils import timezone

def friend(request):
    return render(request, "friend/friends.html")

def friend_list(request, user_id):
    try:
        current_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    # Ambil semua user yang sudah berteman dua arah (baik sebagai pengirim atau penerima)
    friend_ids = Friend.objects.filter(
        Q(user=current_user, status='accepted') | 
        Q(friend_username=current_user, status='accepted')
    ).values_list('user__id', 'friend_username__id')

    # Flatten ke satu list id
    friend_ids_flat = set()
    for u, f in friend_ids:
        friend_ids_flat.add(u)
        friend_ids_flat.add(f)
    friend_ids_flat.discard(current_user.id)  # Jangan masukkan diri sendiri

    # Ambil permintaan pertemanan tertunda yang diterima oleh current_user
    pending_requests = Friend.objects.filter(friend_username=current_user, status='pending')
    pending_sender_ids = pending_requests.values_list('user__id', flat=True)
    pending_receiver_ids = Friend.objects.filter(user=current_user, status='pending').values_list('friend_username__id', flat=True)

    # Filter alluser: hanya user yang belum berteman/berkirim request
    alluser = User.objects.exclude(id=current_user.id)\
        .exclude(id__in=friend_ids_flat)\
        .exclude(id__in=pending_sender_ids)\
        .exclude(id__in=pending_receiver_ids)

    # Ambil teman yang sudah diterima (status='accepted') satu arah (untuk tampilan daftar teman)
    friends = Friend.objects.filter(
        Q(user=current_user, status='accepted') | 
        Q(friend_username=current_user, status='accepted')
    )

    # Tangani penambahan teman, penerimaan, atau penolakan permintaan
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_friend":
            friend_id = request.POST.get("friend_id")
            try:
                friend_user = User.objects.get(id=friend_id)
                if current_user == friend_user:
                    return HttpResponse("You cannot add yourself as a friend.", status=400)
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
