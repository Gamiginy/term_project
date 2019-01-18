from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Account(AbstractUser):
    SCHOOL_GRADE_CHOICE = (
        ('E', '工学部'),
        ('F', '未来科学部')
    )

    DEPARTMENT_CHOICE = (
        ('EJ', '電機電子工学科'),
        ('EH', '電子システム工学科'),
        ('ES', '応用科学科'),
        ("EK", '機会工学科'),
        ('EF', '先端機械工学科'),
        ('EC', '情報通信工学科'),
        ('FI', '情報メディア学科'),
        ('FE', '建築学科'),
        ('FR', 'ロボット・メカトロニクス学科'),
    )

    SECRET_QUESTION_CHOICE = (
        ('FF', '好きな食べ物は？'),
        ('FD', '将来の夢は？'),
        ('PN', 'ペットの名前は？'),
        ('WG', '行きたい場所は？')
    )

    school_year = models.SmallIntegerField(
        verbose_name='学年',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    school_grade = models.CharField(
        verbose_name='学部',
        max_length=1,
        null=True,
        blank=True,
        choices=SCHOOL_GRADE_CHOICE,
    )
    department = models.CharField(
        verbose_name='学科',
        max_length=2,
        null=True,
        blank=True,
        choices=DEPARTMENT_CHOICE,
    )
    secret_question = models.CharField(
        verbose_name='秘密の質問',
        max_length=2,
        choices=SECRET_QUESTION_CHOICE,
    )
    secret_question_answer = models.CharField(
        verbose_name='秘密の質問の答え',
        max_length=10
    )