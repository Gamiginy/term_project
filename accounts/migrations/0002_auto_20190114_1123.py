# Generated by Django 2.1.2 on 2019-01-14 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='secret_question',
            field=models.CharField(choices=[('FF', '好きな食べ物は？'), ('FD', '将来の夢は？'), ('PN', 'ペットの名前は？'), ('WG', '行きたい場所は？')], max_length=2, verbose_name='秘密の質問'),
        ),
    ]
