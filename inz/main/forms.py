from django import forms
from .static.consts import Parameters

def normalize_choices(choices: list)-> list:
    return [(choices.index(choice), str(choice)) for choice in choices]


class SetParametersForm(forms.Form):
    """ Gets all parameters value (m, n, iters)"""  
    m_parameters = forms.ChoiceField(
        choices=normalize_choices(Parameters.m),
        required=False,
        label="Pula atrybutów tablicy decyzyjnej"
    )
    # m_parameters_custom = forms.CharField(
    #     min_length=1,
    #     max_length=100,
    #     required=False,
    #     label="Inna pula atrybutów tablicy decyzyjnej"
    # )
    n_parameters = forms.ChoiceField(
        choices=normalize_choices(Parameters.n),
        required=False,
        label="Ilość agentów"
    )
    # n_parameters_custom = forms.CharField(
    #     min_length=1,
    #     max_length=100,
    #     required=False,
    #     label="Inna ilość agentów"
    # )    
    iters_parameter = forms.IntegerField(
        max_value=50,
        min_value=1,
        required=True,
        initial=5,
        label = 'Ilość zbiorów drzew decyzyjnych'
    )

    # file_path = forms.FilePathField(
    #     path=PATHS.trees_folder,
    #     allow_folders=False,
    #     allow_files=True,
    #     required=True,
    #     label="Wybierz plik"
    # )

    file_path = forms.CharField(
        max_length=200,
        min_length=1,
        strip=True,
        required=True,
        label="Wpisz ścieżkę pliku do zapisu"
    )