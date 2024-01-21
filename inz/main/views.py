from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from .forms import *
import sys
sys.path.append('..')
from algorythms import MainInz
from algorythms.DecTable import DecTable
from algorythms.DecTree import DecTree
from .static import consts
import mimetypes
import os


all_tables = []
all_tables_and_trees = []
FILE_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(response, info: str|None=None):
    global all_tables
    form = SetParametersFormTables()
    form_load = UploadFileForm()
    if info:
        return render(response, 'main/index.html', {'form': form, 'form_load': form_load, 'info': info})
    else:
        return render(response, 'main/index.html', {'form': form, 'form_load': form_load, 'info': f'Suma wczytanych tablic: {len(all_tables)}'})

def get_tables(response):
    print(response.method)    
    form = SetParametersFormTables()
    form_load = UploadFileForm()
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
        except RecursionError:
            info = 'Błąd przy generowaniu - dobierz inne parametry tablic.'
            return render(response, 'main/index.html', {'info':info,'form': form, 'form_load': form_load})               
        except Exception as ex:
            print(ex)
            info = 'Błąd przy generowaniu.'
            return render(response, 'main/index.html', {info:info,'form': form,'form_load': form_load})              

    info = f'Tablice wygenerowane. Suma wczytanych tablic: {len(all_tables)}' if len(all_tables) else 'Nie wczytano tablic.'
    return render(response, 
        'main/index.html',
        {
            'info':info,
            'form': form,
            'form_load': form_load
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
    form_load = UploadFileForm()
    return render(response, 
        'main/index.html',
        {
            'info':f'Tablice zostały usunięte.',
            'form': form,
            'form_load': form_load
        })       

def save_tables(response):
    global all_tables
    global FILE_BASE_DIR

    filename = 'tables.csv'
    filepath = FILE_BASE_DIR + '/Files/' + filename   

    file_content = ''
    for table in all_tables:
        table_str = table.get_table_str(with_index=False)
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

def load_tables(request):
    global all_tables
    filename = 'tables_uploaded.csv'
    filepath = FILE_BASE_DIR + '/Files/' + filename   
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('file', None)
            if file:
                with open(filepath, "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)     
                with open(filepath, 'r') as f:
                    file_content = f.read()
                new_tables_csv =[]
                new_table = ''
                for line in file_content.split('\n'):
                    if any([sign.isalpha() for sign in line]):
                        # is header
                        new_tables_csv.append(new_table.strip()) if new_table else None
                        new_table = line + '\n'
                    else:
                        new_table += f'{line}\n'   
                new_tables_csv.append(new_table.strip())             
                for table in new_tables_csv:
                    dectable = DecTable.csv_table_to_dectable(table)
                    all_tables.append(dectable)
                return index(response=request, info=f"Tablice wczytane. Suma wczytanych tablic: {len(all_tables)}")
            else:
                return index(response=request, info="Wczytanie pliku nie powiodło się")
    else:
        return redirect('/')
    
def get_trees(response):
    global all_tables
    global all_tables_and_trees
    all_tables_and_trees = []
    if not len(all_tables):
        return render(response, 'main/index.html', 
               {'form': SetParametersFormTables(), 
                'form_load': UploadFileForm(), 
                'info': f'Nie wczytano tablic!'
                })
    for table in all_tables:
        all_tables_and_trees.append({table: DecTree(table)})
    return render(response, 'main/trees_home.html',{})
    
def save_trees(response):    
    file_content = ''
    global all_tables_and_trees
    for idx, bundle in enumerate(all_tables_and_trees):
        table, tree = list(bundle.items())[0]
        file_content += f'Tree {idx}\n'
        for rule in tree.rules:
            file_content += f'{rule}\n'
        global FILE_BASE_DIR

    filename = 'trees.txt'
    filepath = FILE_BASE_DIR + '/Files/' + filename   
    with open(filepath, 'w') as f:
        f.write(file_content)    
    # breakpoint()
    chunksize = 8192
    response = StreamingHttpResponse(
        FileWrapper(open(filepath, 'rb'), chunksize),
        content_type='text/plain'
    )
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = f'Attachment;filename={filename}'
    return response

def show_trees(response):
    filenames = ['1.jpg', '2.jpg', '3.jpg']
    return render(response, 'main/trees.html', {'trees': ['../inz/Files/' + filename for filename in filenames]})

def get_tree_list():
    global all_tables_and_trees
    trees = []
    for bundle in all_tables_and_trees:
        tree = list(bundle.values())[0]
        trees.append(tree)
    return trees

def a(response):
    global all_tables_and_trees
    max_nr_trees, rules_a = MainInz.algorythm_a(get_tree_list())
    parameters = {
        'rules': rules_a, 
        'max_nr': max_nr_trees, 
        'algorythm': 'A',
        'rules_count': len(rules_a),
        'avg_length': sum([rule.count('=')-1 for rule in rules_a]) / len(rules_a)
    }
    return render(response, 'main/rules.html', parameters)

def h(response):
    pass