from django.shortcuts import render, redirect
from .forms import *
import sys
sys.path.append('..')
from algorythms import main_inz


# Create your views here.


def index(response):
    form = SetParametersForm()
    return render(response, 'main/index.html', {'form': form})

def get_values(response):
    if response.method != 'POST':
        return redirect(index)
    form = SetParametersForm(response.POST)

    