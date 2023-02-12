import json

from django.core.management.base import BaseCommand
from api.models import Ingredient


class Command(BaseCommand):
    help = 'import ingredient'

    def handle(self, *args, **options):
        with open(
                'backend/foodgram/data/ingredients.json',
                'r',
                encoding='utf-8'
                ) as file:
            data = json.load(file)
            for element in data:
                models = Ingredient(
                    name=element['name'],
                    measurement_unit=element['measurement_unit'],
                )
                models.save()
        print('ингредиенты импортированны')
