from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from .forms import *
import sys
sys.path.append('..')
from algorythms import MainInz
from .static import consts
import mimetypes
import os


all_tables = []
FILE_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(response):
    # form = SetParametersForm()
    form = SetParametersFormTables()
    return render(response, 'main/index.html', {'form': form})

def get_tables(response):
    print(response.method)    
    if response.method == 'POST':
        tables_num = response.POST.get('tables_num')
        rows_num = response.POST.get('rows_num')
        attributes_num = response.POST.get('attributes_num')
        try:
            print('Generowanie tablic')
            global all_tables
            all_tables += MainInz.generate_n_tables(
                tables_num=int(tables_num),
                rows_num=int(rows_num),
                attributes_num=int(attributes_num)
            )
            print('Tablice wygenerowane.')
        except Exception as ex:
            print(f"Błąd przy generowaniu tablic: {ex}")

    form = SetParametersFormTables()
    return render(response, 
        'main/index.html',
        {
            'info':f'Tablice wygenerowane. Ilość wczytanych tablic: {len(all_tables)}',
            'form': form
        })   
        
def show_tables(response):
    ''' Prepare html table code '''
    tables_html = []
    global all_tables
    for table in all_tables:
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

def delete_tables(response):
    global all_tables
    all_tables = []
    form = SetParametersFormTables()
    return render(response, 
        'main/index.html',
        {
            'info':f'Tablice zostały usunięte.',
            'form': form
        })       

def save_tables(response):
    global all_tables
    global FILE_BASE_DIR

    filename = 'tables.csv'
    filepath = FILE_BASE_DIR + '/Files/' + filename   

    file_content = ''
    for table in all_tables:
        table_str = str(table)
        for row in table_str.split('\n'):
            file_content += ','.join(row.strip().split())
            file_content += ',\n'
    with open(filepath, 'w') as f:
        f.write(file_content)

    # breakpoint()
    chunksize = 8192
    response = StreamingHttpResponse(
        FileWrapper(open(filepath, 'rb'), chunksize),
        content_type='text/csv'
    )
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = f'Attachment;filename={filename}'
    return response

    return render(response, 
        'main/index.html',
        {
            'info':f'Tablice zostały zapisane.',
            # 'form': form
        })           
