import graphviz
import os
os.environ["PATH"] += os.pathsep + r'D:\Program Files\Graphviz\bin'


class TreeVis:

    def __init__(self, rules: str|list[str], decision_sign: str, name: str, folder_path: str):
        if isinstance(rules, str):
            rules = rules.split('\n')
        self.rules = rules
        self.decision_sign = decision_sign
        self.figure = graphviz.Digraph(name, filename=name)
        self.figure.attr(rankdir='TB', size='12')
        self.figure.attr('node', shape='circle')        
        self.edges = list()
        self.name = name
        self.folder_path = folder_path

    def draw(self): 
        self.figure.render(format='png', filename=f'{self.folder_path}{self.name}')        

    def construct_tree(self):    
        if not self.rules:
            print('Empty rules set!')
            return 
        for r_idx, rule in enumerate(self.rules):
            path = ''
            pairs = rule.split()
            for i in range(len(pairs)-1):
                atr, val = pairs[i].split('=')
                path += atr
                n_atr, n_val = pairs[i+1].split('=')
                start_node = path
                path += f'={val}'
                end_node = path + n_atr
                self.figure.node(name=start_node, label=atr)
                if n_atr == self.decision_sign:
                    end_node = f'{end_node}-{n_val}'
                    self.figure.node(name=end_node, label=pairs[i+1])
                else:
                    self.figure.node(name=end_node, label=n_atr)
                if not ((start_node, end_node)) in self.edges:
                    self.figure.edge(start_node, end_node, label=val)
                    self.edges.append((start_node, end_node))

                    
# rules = [
#     'f5=1 f1=1 f7=1 f3=1 d=1',
#     'f5=1 f1=1 f7=1 f3=0 d=0',
#     'f5=1 f1=1 f7=0 d=1',
#     'f5=1 f1=0 d=1',
#     'f5=0 f6=1 d=1',
#     'f5=0 f6=0 f7=1 f2=1 d=1',
#     'f5=0 f6=0 f7=1 f2=0 d=0',
#     'f5=0 f6=0 f7=0 f1=1 d=0',
#     'f5=0 f6=0 f7=0 f1=0 d=1'
# ]

# vis = TreeVis(rules, decision_sign='d', name='test')
# vis.construct_tree_gr()
# vis.draw_gr()