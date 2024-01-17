from django import forms
from .static.consts import Parameters

def normalize_choices(choices: list)-> list:
    return [(choices.index(choice), str(choice)) for choice in choices]


class SetParametersFormTables(forms.Form):
    tables_num = forms.IntegerField(
        max_value=100,
        min_value=5,
        required=True,
        initial=15,
        label = 'Liczba tablic'
    )

    attributes_num = forms.IntegerField(
        max_value=20,
        min_value=5,
        required=True,
        initial=7,
        label = 'Liczba atrybutów'
    )    

    rows_num = forms.IntegerField(
        max_value=80,
        min_value=5,
        required=True,
        initial=10,
        label = 'Ilość wierszy'
    )    

class UploadFileForm(forms.Form):
    file = forms.FileField(required=True, label='Plik')    