from django.contrib import admin
from .models import Book, Bid, History, Notification

# Register your models here.
admin.site.register(Book)
admin.site.register(Bid)
admin.site.register(History)
admin.site.register(Notification)
