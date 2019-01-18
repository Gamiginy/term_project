# Generated by Django 2.1.2 on 2019-01-13 20:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_address', models.EmailField(max_length=23, verbose_name='メールアドレス')),
                ('rial_name', models.CharField(max_length=10, verbose_name='本名')),
                ('user_name', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(8)], verbose_name='ユーザ名')),
                ('password', models.CharField(max_length=16, validators=[django.core.validators.MinLengthValidator(8)], verbose_name='パスワード')),
                ('school_year', models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='学年')),
                ('school_grade', models.CharField(blank=True, choices=[('E', '工学部'), ('F', '未来科学部')], max_length=1, null=True, verbose_name='学部')),
                ('department', models.CharField(blank=True, choices=[('EJ', '電機電子工学科'), ('EH', '電子システム工学科'), ('ES', '応用科学科'), ('EK', '機会工学科'), ('EF', '先端機械工学科'), ('EC', '情報通信工学科'), ('FI', '情報メディア学科'), ('FE', '建築学科'), ('FR', 'ロボット・メカトロニクス学科')], max_length=2, null=True, verbose_name='学科')),
                ('secret_question', models.CharField(choices=[('Favorite food', '好きな食べ物は？'), ('Dream', '将来の夢は？'), ('Pet name', 'ペットの名前は？'), ('A place you want to go', '行きたい場所は？')], max_length=1, verbose_name='秘密の質問')),
                ('secret_question_answer', models.CharField(max_length=10, verbose_name='秘密の質問の答え')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999999)], verbose_name='付け値')),
                ('bid_date', models.DateTimeField(verbose_name='bid date')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='商品名')),
                ('isbn_10', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10)])),
                ('isbn_13', models.CharField(max_length=14, validators=[django.core.validators.MinLengthValidator(14)])),
                ('price', models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999999), django.core.validators.MinValueValidator(0)], verbose_name='価格')),
                ('trade_date', models.DateTimeField(verbose_name='trade date')),
                ('trade_place', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(1)], verbose_name='受け渡し場所')),
                ('description', models.TextField(blank=True, max_length=200, validators=[django.core.validators.MinLengthValidator(0)], verbose_name='商品説明')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('due_date', models.DateTimeField(verbose_name='due date')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.Account')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('browsed_date', models.DateTimeField(verbose_name='browsed date')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.Account')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField(max_length=1200, verbose_name='問い合わせ内容')),
                ('inq_date', models.DateTimeField(verbose_name='inquired date')),
                ('account', models.ForeignKey(on_delete=False, to='auction.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='通知タイトル')),
                ('description', models.TextField(max_length=1200, verbose_name='通知内容')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.Account')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auction.Book')),
            ],
        ),
        migrations.AddField(
            model_name='bid',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.Book'),
        ),
    ]
