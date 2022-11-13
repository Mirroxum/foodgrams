# Generated by Django 2.2.16 on 2022-11-13 03:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='favorite',
            field=models.ManyToManyField(related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Избранные рецепты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='_recipe_ingredients_+', through='recipes.AmountIngredient', to='recipes.Ingredient', verbose_name='Ингридиенты для рецепта'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='_recipe_tags_+', to='recipes.Tag', verbose_name='Теги'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_for_ingredient'),
        ),
        migrations.AddField(
            model_name='amountingredient',
            name='ingredients',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recipes.Ingredient', verbose_name='Связанные ингредиенты'),
        ),
        migrations.AddField(
            model_name='amountingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recipes.Recipe', verbose_name='В каких рецептах'),
        ),
        migrations.AddConstraint(
            model_name='recipe',
            constraint=models.UniqueConstraint(fields=('name', 'author'), name='unique_for_author'),
        ),
        migrations.AddConstraint(
            model_name='amountingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredients'), name='%(app_label)s_%(class)s ingredient alredy added\n'),
        ),
    ]
