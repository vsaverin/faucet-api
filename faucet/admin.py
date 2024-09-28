from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class AuthorAdmin(admin.ModelAdmin):
    pass
