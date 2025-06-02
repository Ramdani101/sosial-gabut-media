from django.contrib import admin
from django.contrib.auth.models import User
from .models import Friend
from django.utils import timezone

class FriendInLine(admin.StackedInline):
    model = Friend
    fk_name = 'user'  # Menentukan bahwa field 'user' adalah ForeignKey yang terkait
    fields = ['friend_username', 'status', 'accepted_at']
    readonly_fields = ['created_at']
    extra = 1  # Menampilkan 1 form kosong untuk menambahkan teman

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            # Batasi pilihan friend_username untuk mengecualikan pengguna saat ini
            formset.form.base_fields['friend_username'].queryset = User.objects.exclude(id=obj.id)
        return formset

    def save_model(self, request, obj, form, change):
        # Jika status 'accepted', isi accepted_at jika belum diisi
        if obj.status == 'accepted' and not obj.accepted_at:
            obj.accepted_at = timezone.now()
        # Jika status bukan 'accepted', kosongkan accepted_at
        elif obj.status != 'accepted':
            obj.accepted_at = None
        super().save_model(request, obj, form, change)

class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'email', 'password']
    inlines = [FriendInLine]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Friend)