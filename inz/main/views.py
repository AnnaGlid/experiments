from django.shortcuts import render, redirect
from .forms import *
import sys
sys.path.append('..')
from algorythms import MainInz
from .static import consts

# Create your views here.


def index(response):
    form = SetParametersForm()
    return render(response, 'main/index.html', {'form': form})

def get_tables(response):
    print(response.method)    
    if response.method != 'POST':
        return redirect(index)
    m_index = response.POST.get('m_parameters')
    n_index = response.POST.get('n_parameters')    
    try:
        print('Generowanie tablic')
        tables = MainInz.generate_tables(
            m_values=consts.Parameters.m[int(m_index)],
            n_values=consts.Parameters.n[int(n_index)],
            iters=int(response.POST.get('iters_parameter'))
        )
        print('Tablice wygenerowane.')
    except Exception as ex:
        print(f"Błąd przy generowaniu tablic: {ex}")

    # breakpoint()
        
    ''' Prepare html table code '''
    tables_html = []
    for table in tables:
        html_code = f'''
        <div class="label">
            <p>Liczba atrybutów: {len(table.attributes_subset)}</p>
            <p>Liczba wierszy: {table.rows_number}</p>
        </div>
        '''
        html_code +='<table>'
        table_str = str(table)
        print(table_str)
        print('\n')
        rows = table_str.split('\n')
        for idx, row in enumerate(rows):
            row = row.strip()
            tag = 'th' if idx == 0 else 'td'
            html_code += f'<tr>'
            cells = row.split() if idx == 0 else row.split()[1:]
            for cell in cells:
                html_code += f'<{tag}>{cell.strip()}</{tag}>'
            html_code += '</tr>'
        html_code += '</table>'
        tables_html.append(html_code)
                            
    return render(response, 
        'main/tables.html',
        {'tables':tables_html})


    