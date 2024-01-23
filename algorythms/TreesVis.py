import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from random import randint

class TreeVis:
    RADIUS = 2
    LIMITS_OFFSET_X = 2
    LIMITS_OFFSET_Y = 2
    INCH = 16 # units

    def __init__(self, rules: str|list[str], decision_sign: str):
        if isinstance(rules, str):
            rules = rules.split('\n')
        self.rules = self.prepare_rules(rules)
        self.elements = []
        self.patches = []
        self.labels = []
        self.x_min = None
        self.y_min = None
        self.x_max = None
        self.y_max = None
        self.decision_sign = decision_sign
        self.max_depth = max([len(rule) for rule in self.rules])

    def prepare_rules(self, rules):
        result = []
        for rule in rules:
            pairs = rule.strip().split()
            result.append([pair.split('=') for pair in pairs])
        return result

    def __set_limits(self, x:int, y:int):
        if self.x_min is None or self.x_min > x:
            self.x_min = x
        if self.x_max is None or self.x_max < x:
            self.x_max = x
        if self.y_min is None or self.y_min > y:
            self.y_min = y
        if self.y_max is None or self.y_max < y:
            self.y_max = y

    def draw_cricle(self, x: int, y:int, label: str|None=None, scale_radius:int=1, depth_scale:bool=False):
        if depth_scale:
            scale_radius = self.max_depth // 3
        self.patches.append(plt.Circle((x, y), self.RADIUS*scale_radius, fill=False))
        if label:
            self.labels.append({
                'x':x, 'y':y, 
                'text':label,
            })
        self.__set_limits(x,y)
        
    def count_edge_x_length(self, current_depth:int)-> int:
        ''' Counts length of edge on x axis. Root's depth is equal to 0.
            Maximum depth of tree is counted with leaves.
            Node degree is counted as: maximum_depth - current_depth.'''
        # degree = self.max_depth - current_depth
        # if degree == 0:
        #     return self.RADIUS
        # if degree == 1:
        #     return self.RADIUS * 2
        # prev = self.RADIUS * 2        

        degree = self.max_depth - current_depth - 1 
        if degree == 0:
            return 0
        if degree == 1:
            return self.RADIUS
        if degree == 2:
            return self.RADIUS + 2
        prev = self.RADIUS + 2   
        for i in range(2, degree):
            length = 2*prev + 2*self.RADIUS
            prev = length
        if current_depth < 3:
            print(prev)
        return prev
        

    def draw_arrow(self, x: int, y: int, right: bool, depth: int,
                   label: str|None=None) -> tuple[int, int]:
        ''' Draws arrow from point x, y and returns coordinates for next node
            depth is depth of the node that the arrow is going FROM '''
        factor = 1 if right else -1
        
        x_start = x + self.RADIUS * factor
        y_start = y-self.RADIUS

        #region dependent on depth        
        calculated_length = self.count_edge_x_length(depth)
        x_len = calculated_length * factor      
        x_label = x + (calculated_length + self.RADIUS)*factor
        next_x = x + (calculated_length + self.RADIUS*2)*factor
        #endregion

        y_factor = (calculated_length // 10) + 1 + depth
        # y_len = -3 if not right else -3 
        # y_label = y-2 if not right else y-2
        # next_y = y-5 if not right else y-5
        y_len = -y_factor
        y_label = y-(y_factor//2)
        next_y = y - y_factor - 2

        plt.arrow(x_start, y_start, x_len, y_len, length_includes_head=True, head_width=0.3, head_length=0.4)
        if label is not None:
            self.labels.append({
                'x':x_label, 
                'y':y_label, 
                'text':label,
            })            
        self.__set_limits(next_x, next_y )           
        return (next_x, next_y)


    def draw(self, show:bool=False, save:bool=False, path:str|None=None):
        ax = plt.subplot()
        for patch in self.patches:
            ax.add_patch(patch)
        for label in self.labels:
            ax.text(label['x'], label['y'], label['text'], horizontalalignment='center', 
                    verticalalignment='center', fontsize=8, color='red')
        plt.xlim([self.x_min - self.LIMITS_OFFSET_X, self.x_max + self.LIMITS_OFFSET_X])
        plt.ylim([self.y_min - self.LIMITS_OFFSET_Y, self.y_max + self.LIMITS_OFFSET_Y])
        plt.subplots_adjust(
            left=0,
            bottom=0,
            right=1,
            top=1
        )
        ax.axis('off')        
        figure = plt.gcf() # get current figure
        x_size = abs(self.x_min) + abs(self.x_max)
        y_size = abs(self.y_min) + abs(self.y_max)
        x_size = self.INCH if x_size < self.INCH else x_size
        y_size = self.INCH if y_size < self.INCH else y_size
        figure.set_size_inches(x_size//self.INCH, y_size // self.INCH)
        # figure.set_size_inches(x_size,y_size)     
        # ax = plt.gca()
        # ax.set_aspect('equal', adjustable='box')
        ax.axes.set_aspect('equal')
        if show:
            plt.show()
        if save:
            # plt.savefig(path, dpi=150, bbox_inches='tight')  
            plt.savefig(path)
        plt.close()


    def construct_tree(self):
        ''' Binary tree - egdes equal to 1 are going right, equal to 0 are going left'''
        if not self.rules:
            print('Empty rules set!')
            return 
        stack = []
        # create first complete path
        for idx, pair in enumerate(self.rules[0]):
            atr, val = pair[0], int(pair[1])
            if idx == 0:
                x, y = 0, 0  
            else:
                x, y = next_coords[0], next_coords[1]
            if atr == self.decision_sign:
                self.draw_cricle(x, y, f'{atr}={val}')   
            else: 
                self.draw_cricle(x, y, atr)
                stack.append({'x':x, 'y':y, 'atr': atr, 'val': val})
                next_coords = self.draw_arrow(x, y, right=bool(val), label=val, depth=idx)            

        for rule in self.rules[1:]:
            reversed_rule = rule.copy()
            reversed_rule.reverse()
            start_pair_idx = 0
            break_stack = False
            while len(stack):
                stack_element = stack.pop()
                for idx, pair in enumerate(reversed_rule):
                    atr, val = pair[0], int(pair[1])
                    if atr == self.decision_sign:
                        continue                
                    if stack_element['atr'] != atr:
                        continue
                    else:
                        start_pair_idx = idx      # count idx from the end
                        break_stack = True
                        break
                if break_stack:
                    break
            x, y = stack_element['x'], stack_element['y']
            depth = rule.index([atr, str(val)])
            next_coords = self.draw_arrow(x, y, right=val, label=val, depth=depth)
            for pair in rule[-start_pair_idx:]:         
                atr, val = pair[0], pair[1]
                x, y = next_coords[0], next_coords[1]        
                if atr == self.decision_sign:
                    self.draw_cricle(x, y, f'{atr}={val}')   
                else: 
                    self.draw_cricle(x, y, atr)
                    stack.append({'x':x, 'y':y, 'atr': atr, 'val': val})
                    depth = rule.index(pair)
                    next_coords = self.draw_arrow(x, y, right=bool(val), label=val, depth=depth)                                                     
        
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
# vis = TreeVis(rules, decision_sign='d')
# vis.construct_tree()
# vis.draw(show=True)
# d=1
# vis.draw_cricle(0,0, 'f31')
# next_node = vis.draw_arrow(0,0, True, '1')
# vis.draw_cricle(next_node[0], next_node[1], 'f21')
# next_nodes = vis.draw_arrow(next_node[0], next_node[1], False, '0')
# next_node = vis.draw_arrow(next_node[0], next_node[1], True, '1')
# vis.draw_cricle(next_nodes[0], next_nodes[1], 'f21')
# vis.draw(show=True)

# circle1 = plt.Circle((0, 0), 0.2, color='r')
# circle2 = plt.Circle((0.5, 0.5), 0.2, color='blue')
# circle3 = plt.Circle((1, 1), 0.2, color='g', clip_on=False)

# fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
# (or if you have an existing figure)
# fig = plt.gcf()
# ax = fig.gca()

# ax.add_patch(circle1)
# ax.add_patch(circle2)
# ax.add_patch(circle3)