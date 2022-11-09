import csv
import io

from recipes.models import Ingredient

DIC = {
    Ingredient: 'data/ingredients.csv',
}


# set this value to True, in case you need
# to clean db before injecting data:
ERASE_ALL = True


def get_fields(row):
    row['name'] = Ingredient.objects.get(pk=row['name'])
    return row


def run():
    for key in DIC:
        if ERASE_ALL:
            key.objects.all().delete()
            print(
                f'All existing records for table {key.__name__} were erased.'
            )

        with io.open((DIC[key]), encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            data = []
            for row in reader:
                try:
                    temp_row = dict(zip(header, row))
                    row_fixed = get_fields(temp_row)
                    data.append(row_fixed)
                except Exception as e:
                    print(f'Failed with error: {e}')

            successful = 0
            failed = 0
            for row in data:
                try:
                    _, s = key.objects.get_or_create(**row)
                    if s:
                        successful += 1
                except Exception as e:
                    print(f'Failed with error: {e}')
                    failed += 1

            print(
                f'Successfully created ojects type {key.__name__}:'
                f'{successful}, failed: {failed}.'
            )
