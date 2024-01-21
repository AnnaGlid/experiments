from matplotlib import pyplot as plt
import numpy as np
from matplotlib.patches import Circle

class TreeVis:
    RADIUS = 1
    LIMITS_OFFSET = 3

    def __init__(self, rules: str|list[str]):
        if isinstance(rules, str):
            rules = rules.split('\n')
        self.rules = rules
        self.elements = []
        self.patches = []
        self.labels = []
        self.x_min = None
        self.y_min = None
        self.x_max = None
        self.y_max = None


    def __set_limits(self, x:int, y:int):
        if self.x_min is None or self.x_min > x:
            self.x_min = x
        if self.x_max is None or self.x_max < x:
            self.x_max = x
        if self.y_min is None or self.y_min > y:
            self.y_min = y
        if self.y_max is None or self.y_max < y:
            self.y_max = y

    def draw_cricle(self, x: int, y:int, label: str|None=None):
        self.patches.append(plt.Circle((0, 0), self.RADIUS, fill=False))
        if label:
            self.labels.append({
                'x':x, 'y':y, 
                'text':label,
            })
        self.__set_limits(x,y)
        
    def draw_arrow(self, x: int, y: int, right: bool, label: str|None=None) -> tuple[int, int]:
        ''' Draws arrow and returns coordinates for next node'''
        if right:
            plt.arrow(x+1, y-1, 2, -3, length_includes_head=True, head_width=0.3, head_length=0.4)
            if label:
                self.labels.append({
                    'x':x+2, 
                    'y':y-2, 
                    'text':label,
                })            
            next_x, next_y = x+3, y-5
            self.__set_limits(next_x, next_y )
        else:
            plt.arrow(x-1, y-1, -2, -3, length_includes_head=True)   
            if label:
                self.labels.append({
                    'x':x-2, 
                    'y':y-2, 
                    'text':label,
                })                  
            next_x, next_y = x-3, y-5
            self.__set_limits(next_x, next_y)              
        return (next_x, next_y)

    def draw(self, show:bool=False):
        ax = plt.subplot()
        for patch in self.patches:
            ax.add_patch(patch)
        for label in self.labels:
            ax.text(label['x'], label['y'], label['text'], horizontalalignment='center', verticalalignment='center')
        plt.xlim([self.x_min - self.LIMITS_OFFSET, self.x_max + self.LIMITS_OFFSET])
        plt.ylim([self.y_min - self.LIMITS_OFFSET, self.y_max + self.LIMITS_OFFSET])
        if show:
            plt.show()

    
rules = [
    'f5=1 f1=1 f7=1 f3=1 d=1',
    'f5=1 f1=1 f7=1 f3=0 d=0',
    'f5=1 f1=1 f7=0 d=1',
    'f5=1 f1=0 d=1',
    'f5=0 f6=1 d=1',
    'f5=0 f6=0 f7=1 f2=1 d=1',
    'f5=0 f6=0 f7=1 f2=0 d=0',
    'f5=0 f6=0 f7=0 f1=1 d=0',
    'f5=0 f6=0 f7=0 f1=0 d=1'
]
vis = TreeVis(rules)
vis.draw_cricle(0,0, 'f31')
next_node = vis.draw_arrow(0,0, True, '1')
# vis.draw_cricle(next_node[0], next_node[1], 'f21')
vis.draw(show=True)

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

plt.show()