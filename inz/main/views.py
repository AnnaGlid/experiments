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
parameters_a = None
parameters_h = None
trees_visualised = False
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
    global parameters_a
    global parameters_h
    global trees_visualised
    trees_visualised = False
    parameters_a = None
    parameters_h = None    
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
    global trees_visualised
    trees_visualised = False
    all_tables_and_trees = []
    if not len(all_tables):
        return render(response, 'main/index.html', 
               {'form': SetParametersFormTables(), 
                'form_load': UploadFileForm(), 
                'info': f'Nie wczytano tablic!'
                })
    for table in all_tables:
        all_tables_and_trees.append({table: DecTree(table)})
    return redirect('/trees-home/')

def trees_home(response):
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
    chunksize = 8192
    response = StreamingHttpResponse(
        FileWrapper(open(filepath, 'rb'), chunksize),
        content_type='text/plain'
    )
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = f'Attachment;filename={filename}'
    return response

def show_trees(response):
    global trees_visualised
    trees = get_tree_list()
    filenames = [f'{i+1}.png' for i in range(len(trees))]
    if not trees_visualised:        
        MainInz.save_trees_to_file(trees, 'main\\static\\imgs\\')        
        trees_visualised = True
    return render(response, 'main/trees.html', {'trees': filenames})

def get_tree_list():
    global all_tables_and_trees
    trees = []
    for bundle in all_tables_and_trees:
        tree = list(bundle.values())[0]
        trees.append(tree)
    return trees

def get_rules_html(rules_info: dict)-> str:
    html_code = '''
        <div class="subtitle">
            <p> Zbiór reguł </p>
        </div>    
        <table>
            <tr>
                <th> Reguła </th>
                <th> Długość reguły </th>
                <th> Wsparcie reguły </th>
            </tr>
    '''
    for rule_info in rules_info:
        rule = rule_info['rule']
        rule = f'{" ∧ ".join(rule.split()[:-1])} ⇒ {rule.split()[-1]}'
        length = rule_info['length']
        support = rule_info['support']
        html_code += f'''
            <tr>
                <td> {rule} </td>
                <td> {length} </td>
                <td> {support} </td>
            </tr>
        '''
    html_code += '</table>'
    return html_code

def prepare_algorythms_parameters(response, rules: list[str], tables_df: list, max_nr_trees: int)->dict:
    rules_info = []
    if not len(rules):
        return render(
            response,
            'main/trees_home.html',
            {'info': 'Wystąpił błąd'}
        )    
    for rule in rules:
        length = rule.count('=') - 1
        support = MainInz.calculate_support(tables=tables_df, rule=rule)
        rules_info.append({
            'rule': rule,
            'length': length,
            'support': support
        })
    parameters = {
        'rules_table': get_rules_html(rules_info), 
        'max_nr': max_nr_trees, 
        'rules_count': len(rules),
        'avg_length': round(sum([rule.count('=')-1 for rule in rules]) / len(rules), 2),
        'avg_support': round(sum([rule['support'] for rule in rules_info]) / len(rules_info), 2)
    }    
    return parameters

def a(response):
    global all_tables_and_trees
    global all_tables
    global parameters_a
    if parameters_a is None:
        tables = [dectable.table for dectable in all_tables]
        max_nr_trees, rules_a = MainInz.algorythm_a(get_tree_list())
        parameters_a = prepare_algorythms_parameters(response, rules_a, tables, max_nr_trees)
        parameters_a['algorythm'] = 'A'
    return render(response, 'main/rules.html', parameters_a)

def h(response):
    global all_tables_and_trees
    global all_tables
    global parameters_h
    if parameters_h is None:
        tables = [dectable.table for dectable in all_tables]
        max_nr_trees, rules_h = MainInz.heuristic1(get_tree_list())
        parameters_h = prepare_algorythms_parameters(response, rules_h, tables, max_nr_trees)
        parameters_h['algorythm'] = 'H'
    return render(response, 'main/rules.html', parameters_h)