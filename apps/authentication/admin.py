from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "tipo", "activo", "fecha_creacion")
    search_fields = ("username", "email", "nombre_completo")
    list_filter = ("tipo", "activo")



