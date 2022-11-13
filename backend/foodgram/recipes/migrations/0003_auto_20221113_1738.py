# Generated by Django 2.2.16 on 2022-11-13 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20221113_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountingredient',
            name='ingredients',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='recipes.Ingredient', verbose_name='Связанные ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(to='recipes.AmountIngredient'),
        ),
    ]
