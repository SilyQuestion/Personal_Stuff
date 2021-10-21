#!/home/sergio/anaconda3/bin/python
from dataclasses import dataclass
from itertools import groupby
import locale as lcl
lcl.setlocale(lcl.LC_ALL, '')
import fileinput

@dataclass
class Mine:
    num: int
    material: str
    production: str
    um_long: str # Unit of measure
    um_short: str
    active: bool
    # Print the production of all the mines and their status if they are closed
    def print_mine(self):
        if self.active:
            print(f'Miniera {self.num} = {self.production} {self.um_long}')
        else:
            print(f'Miniera {self.num} = CHIUSA')

@dataclass
class Total_Production:
    material: str
    tot_prod: float
    um: str
    # Print the total production for all the materials
    def print_prod(self):
        tmp_tot_prod = f'{self.tot_prod:.2f}'
        print(f'{self.material} = {conv_str(tmp_tot_prod)} {self.um}', end='\n')

@dataclass
class Net_Production:
    material: str
    net_prod: float
    um: str
    value: float
    # Print the net production for all the materials except gold
    def print_net_prod(self):
        if self.net_prod >= 0:
            print(f'{self.material} = +{conv_str(self.net_prod)} {self.um} ->'
                f' +{conv_str(self.value)} ducati')
        else:
            print(f'{self.material} = {conv_str(self.net_prod)} {self.um} ->' 
            f' {conv_str(self.value)} ducati')

# Initialize the mines, if the setup is changed this need to be edited
def init_mines(mines):
    mines.append(Mine(1, 'Oro', '0', 'ducati',  \
                'ducati', True))
    mines.append(Mine(2, 'Ferro', '0', 'chili di ferro', \
                'chili', True))
    mines.append(Mine(3, 'Pietra', '0', 'quintali di pietra', \
                'quintali', True))
    mines.append(Mine(4, 'Pietra', '0', 'quintali di pietra', \
                'quintali', True))
    mines.append(Mine(5, 'Ferro', '0', 'chili di ferro', \
                'chili', True))
    mines.append(Mine(6, 'Oro', '0', 'ducati', \
                'ducati', True))
    mines.append(Mine(7, 'Argilla', '0', 'blocchi di argilla', \
                'blocchi', False))

# Read the maintenance events from stdin
def read_mtn_events():
    l = []
    [l.append(s) for s in fileinput.input()]
    return l

# Calculate the total value for the materials
def calc_mtl_value(net_prod):
    tot = sum(p.value for p in net_prod)
    if  tot >= 0:
        print(f'Totale = +{conv_str(tot)} ducati , valore merci', end='\n\n')
    else:
        print(f'Totale = {conv_str(tot)} ducati , valore merci', end='\n\n')
    return tot

# Calculate the materials used for maintenance
def calc_mtl_usage(huge, um):
    tot_mtl = 0
    for line in huge:
        str = line.split(' ')
        try:
            index = str.index(um)
            tot_mtl += lcl.atof(str[index - 1])
        except:
            pass
    return tot_mtl


def by_material(p):
    return p.material

# Calculate the total production for every material
def sum_by_material(mines):
    grouped_prods = []
    for key, group in groupby(sorted(mines, key=by_material), by_material):
        total_prod = 0
        for g in group:
             total_prod += conv_float(g.production)
        if g.active:
            grouped_prods.append(Total_Production(key, total_prod, g.um_short))
    return grouped_prods 

# Calculate the net production of gold
def calc_net_gold(total_prod, salaries):
    net_gold = 0
    for m in total_prod:
        if m.material == 'Oro':
            net_gold = m.tot_prod - salaries
    return net_gold

# Calculate the net production of the other materials and their value
def calc_net_prod(total_prod, irons, IRON_PRICE, 
                stones, STONE_PRICE, CLAY_PRICE):
    net_prod = []
    for m in total_prod:
        if m.material == 'Ferro':
            t = m.tot_prod - irons
            v = t*IRON_PRICE
            net_prod.append(Net_Production('Ferro', t, 'chili', v))
        if m.material == 'Pietra':
            t = m.tot_prod - stones
            v = t*STONE_PRICE
            net_prod.append(Net_Production('Pietra', t, 'quintali', v))
        if m.material == 'Argilla':
            t = m.tot_prod
            v = t*CLAY_PRICE
            net_prod.append(Net_Production('Argilla', t, 'blocchi', v))
    return net_prod

# Print the total countervalue and the net production of gold
# Of course num and value will be different for each call
def print_tot(num, value):
    if num >= 0:
        print(f'{value} = +{conv_str(num)} ducati')
    else:
        print(f'{value} = {conv_str(num)} ducati')

# Convert a string to a floating point number
def conv_float(str):
    return float(str.replace(',','.'))

# Convert a floating point number to a string
def conv_str(num):
    n = f'{float(num):.2f}'
    return str(n).replace('.',',')

def main():
    mines = []
    init_mines(mines)

    print('Inserisci la produzione delle miniere:')
    for mine in mines:
        if mine.active:
            mine.production = input()

    print('Inserisci gli avvenimenti delle manutenzioni:')
    events = read_mtn_events()

    print('Inserisci il salario dei minatori:')
    salaries = conv_float((input()))

    print('Produzione:', end='\n\n')
    [mine.print_mine() for mine in mines]
    print(end='\n\n')

    print('Totale produzione:', end='\n\n')
    tot_prod = sum_by_material(mines)
    [ p.print_prod()  for p in tot_prod]
    print(end='\n\n')

    print('Spese e manutenzioni:', end='\n\n')
    stones = calc_mtl_usage(events, 'quintali')
    irons = calc_mtl_usage(events, 'chili')
    print(f'Pietra = {conv_str(stones)} quintali')
    print(f'Ferro = {conv_str(irons)} chili')
    print(f'Salario minatori = {conv_str(salaries)} ducati')
    print(end='\n\n')

    IRON_PRICE = 19
    STONE_PRICE = 14.50
    CLAY_PRICE = 4.00
    print('Produzione netta e controvalore in ducati per singola produzione:')
    print(f'( ferro {conv_str(IRON_PRICE)} dct -'\
            f' pietra {conv_str(STONE_PRICE)}' \
            f' dct - argilla {conv_str(CLAY_PRICE)} dct)',
            end ='\n\n')
    # Net production for all the materials
    net_prod = calc_net_prod(tot_prod, irons, IRON_PRICE, 
                            stones, STONE_PRICE, CLAY_PRICE)
    # Net production of gold
    net_gold = calc_net_gold(tot_prod, salaries)
    print_tot(net_gold, 'Oro')
    print(end='\n\n')
    # Net production for the other materials
    [m.print_net_prod() for m in net_prod]
    tot = calc_mtl_value(net_prod)
    value = 'Controvalore totale in ducati delle risorse minerarie prodotte'\
            ' al netto dei costi di manutenzione e spese'
    print_tot(net_gold + tot, value)

if __name__ == '__main__':
    main()