# Generated by Django 4.1 on 2022-10-15 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0003_alter_post_category_alter_post_owner_alter_post_tag"),
    ]

    operations = [
        migrations.RemoveField(model_name="post", name="tag",),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(to="blog.tag", verbose_name="标签"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="作者",
            ),
        ),
    ]
