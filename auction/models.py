import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

from accounts.models import Account


# Create your models here.
class Book(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    top_bid_account_id = models.CharField(
        max_length=99999,
        null=True,
    )
    title = models.CharField(verbose_name='商品名', max_length=40)
    isbn_10 = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)],
    )
    isbn_13 = models.CharField(
        max_length=14,
        validators=[MinLengthValidator(14)]
    )
    price = models.IntegerField(
        verbose_name='価格',
        validators=[
            MaxValueValidator(9999999),
            MinValueValidator(0)
        ]
    )
    trade_date = models.DateTimeField('trade date')
    trade_place = models.CharField(
        verbose_name='受け渡し場所',
        max_length=20,
        validators=[MinLengthValidator(1)]
    )
    description = models.TextField(
        verbose_name='商品説明',
        blank=True,
        max_length=200,
        validators=[MinLengthValidator(0)]
    )
    pub_date = models.DateTimeField('date published')
    due_date = models.DateTimeField('due date')

    def __str__(self):
        return self.title


class Bid(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.IntegerField(
        verbose_name='付け値',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9999999)
        ]
    )
    bid_date = models.DateTimeField('bid date')


class History(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    browsed_date = models.DateTimeField('browsed date')


class Inquiry(models.Model):
    account = models.ForeignKey(Account, on_delete=False)
    detail = models.TextField(verbose_name='問い合わせ内容', max_length=1200)
    inq_date = models.DateTimeField('inquired date')


class Notification(models.Model):
    title = models.CharField(verbose_name='通知タイトル', max_length=20)
    description = models.TextField(verbose_name='通知内容', max_length=1200)
    date = models.DateTimeField('date', null=True, blank=True)
