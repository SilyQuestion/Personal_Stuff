#!/home/sergio/anaconda3/bin/python
from dataclasses import dataclass
from itertools import groupby
import fileinput
from datetime import date, datetime
import locale
locale.setlocale(locale.LC_ALL, "")


@dataclass
class Mine:
    num: int
    material: str
    production: float
    um_long: str # Unit of measure
    um_short: str
    active: bool
    # Print the production of all the mines and their status if they're closed
    def print_mine(self):
        if self.active:
            print(f'Miniera {self.num} ='\
                    f' {f_to_str(self.production)} {self.um_long}')
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
        print(f'{self.material} = {f_to_str(tmp_tot_prod)} {self.um}')

@dataclass
class Net_Production:
    material: str
    net_prod: float
    um: str
    value: float
    # Print the net production for all the materials except gold
    def get_color_sign(self, color, sign):
        print_tags('color=black', end='')
        print(f'{self.material} = ', end='')
        print_tags('/color', end='')

        print_tags(f'color={color}', end='')
        print(f'{sign}{f_to_str(self.net_prod)} {self.um}', end='')
        print_tags('/color', end='')

        print_tags('color=black', end='')
        print(f' -> {sign}{f_to_str(self.value)} ducati')
        print_tags('/color', end='')

    def print_net_prod(self):
        if self.net_prod >= 0:
            self.get_color_sign('green', '+')
        else:
            self.get_color_sign('red', '')

# Initialize the mines, if the setup is changed this need to be edited
def init_mines():
    mines = []
    mines.append(Mine(1, 'Oro', 0, 'ducati', \
                'ducati', True))
    mines.append(Mine(2, 'Ferro', 0, 'chili di ferro', \
                'chili', True))
    mines.append(Mine(3, 'Pietra', 0, 'quintali di pietra', \
                'quintali', True))
    mines.append(Mine(4, 'Pietra', 0, 'quintali di pietra', \
                'quintali', True))
    mines.append(Mine(5, 'Ferro', 0, 'chili di ferro', \
                'chili', True))
    mines.append(Mine(6, 'Oro', 0, 'ducati', \
                'ducati', True))
    mines.append(Mine(7, 'Argilla', 0, 'blocchi di argilla', \
                'blocchi', False))
    return mines

def input_mines(mines):
    for mine in mines:
        if mine.active:
            mine.production = str_to_f(input())

def rm_inactv_mines(mines):
    for mine in mines:
        if mine.active is False:
            mines.remove(mine)

# Read the maintenance events from stdin
def read_mtn_events():
    l = []
    [l.append(s) for s in fileinput.input()]
    return l

# Calculate the value for the materials
def calc_mtl_value(net_prod):
    return sum(m.value for m in net_prod)

# Print the total value for the materials
def print_mtl_value(tot):
    print_tags('color=black', end='')
    if  tot >= 0:
        print(f'Totale = +{f_to_str(tot)} ducati , valore merci\n')
    else:
        print(f'Totale = {f_to_str(tot)} ducati , valore merci\n')
    print_tags('/color')

# Calculate the materials used for maintenance
def calc_mtl_usage(events, um):
    tot_mtl = 0
    for line in events:
        str = line.split(' ')
        try:
            tot_mtl += float(str[str.index(um) - 1])
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
            total_prod += g.production
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

def print_tot(num, caption):
    if num >= 0:
        print_tags('color=black', end='')
        print(f'{caption} = ', end='')
        print_tags('b', end='')
        print(f'+{f_to_str(num)} ducati')
        print_tags('/b', '/color')
    else:
        print_tags('color=black', end='')
        print(f'{caption = }', end='')
        print_tags('b', end='')
        print(f'{f_to_str(num)} ducati')
        print_tags('/b', '/color')

def print_gold(num, caption):
    if num >= 0:
        print_tags('color=black', end='')
        print(f'{caption} = ', end='')
        print_tags('/color', 'color=green', end='')
        print(f'+{f_to_str(num)} ducati')
        print_tags('/color')
    else:
        print_tags('color=black', end='')
        print(f'{caption} = ', end='')
        print_tags('/color', 'color=red', end='')
        print(f'{f_to_str(num)} ducati')
        print_tags('/color')

# Convert a string to a floating point number
def str_to_f(str):
    return float(str.replace(',','.'))

# Convert a floating point number to a string
def f_to_str(num):
    n = f'{float(num):.2f}'
    return str(n).replace('.',',')

def current_date():
    rk_year = 552 # Difference in years between our time and RK
    now = datetime.today()
    dt = now.replace(year=now.year - rk_year)
    tm = now.time()
    reset = now.replace(hour=3, minute=59, second=59, microsecond=0).time()
    if(tm < reset):
        dt = dt.replace(day=dt.day - 2)
        return dt.strftime(f'%d %B %Y')
    else:
        dt = dt.replace(day=dt.day - 1)
        return dt.strftime(f'%d %B %Y')

def print_tags(*args, end='\n'):
    for a in args:
        print(f'[{a}]', end='')
    print(end=end)

def print_heading():
    print_tags('center')
    florence_logo = 'https://i.imgur.com/L7wsril.png'
    print(f'[img]{florence_logo}[/img]')
    print('[b][color=darkred]')
    print('[size=18]Palazzo Vecchio[/size]')
    print('Ufficio del Ministro delle Miniere e delle Grandi Opere\n')
    
    print('[size=18]Resoconto delle miniere')
    print(f'{current_date()}[/size][/b][/color]')
    print_tags('/center', end='\n\n\n')

def print_data(events, salaries):
    print('[center][b][color=black]Dati minerari[/color][/b][/center]')
    print_tags('spoiler')
    print('\nInserire dati minerari qui\n')
    print_tags('/spoiler')
    print('[center][color=black][b]Dati manutenzioni[/b][/color][/center]')
    print_tags('spoiler')
    formatted_events = ''.join(events)
    print(f'{formatted_events}')
    print_tags('/spoiler')
    print('[center][color=black][b]Salari[/b][/color][/center]')
    print_tags('spoiler', end='')
    print(f'Salario minatori: {salaries} ducati')
    print_tags('/spoiler')

def main():
    mines = init_mines()

    print('Inserisci la produzione delle miniere:')
    input_mines(mines)

    print('Inserisci gli avvenimenti delle manutenzioni:')
    events = read_mtn_events()

    print('Inserisci il salario dei minatori:')
    salaries = str_to_f((input()))

    # The post start here
    print_tags('rp')

    print_heading()
    print_data(events, salaries)

    print_tags('color=green', 'b')
    print('PRODUZIONE:', end='')
    print_tags('/b', '/color')
    print_tags('color=black')
    [mine.print_mine() for mine in mines]
    print_tags('/color')

    rm_inactv_mines(mines)

    print_tags('color=black', 'b', end='')
    print('Totale produzione:', end='')
    print_tags('/color', '/b')
    
    print_tags('color=black')
    tot_prod = sum_by_material(mines)
    [p.print_prod()  for p in tot_prod]
    print_tags('/color')

    print_tags('color=red', 'b', end='')
    print('SPESE E MANUTENZIONI:', end ='')
    print_tags('/color', '/b')
    
    print_tags('color=black')
    stones = calc_mtl_usage(events, 'quintali')
    irons = calc_mtl_usage(events, 'chili')
    print(f'Pietra = {f_to_str(stones)} quintali')
    print(f'Ferro = {f_to_str(irons)} chili')
    print(f'Salario minatori = {f_to_str(salaries)} ducati')
    print_tags('/color')
    print(end='\n\n\n')

    IRON_PRICE = 19
    STONE_PRICE = 14.50
    CLAY_PRICE = 4.00
    print_tags('color=black', 'b', end='')
    print('Produzione netta e controvalore in ducati per singola produzione',
            end='')
    print_tags('/b')
    print(f'( ferro {f_to_str(IRON_PRICE)} dct -'\
            f' pietra {f_to_str(STONE_PRICE)}' \
            f' dct - argilla {f_to_str(CLAY_PRICE)} dct)')
    print_tags('/color')

    # Net production for all the materials
    net_prod = calc_net_prod(tot_prod, irons, IRON_PRICE, 
                            stones, STONE_PRICE, CLAY_PRICE)
    # Net production of gold
    net_gold = calc_net_gold(tot_prod, salaries)
    print_gold(net_gold, 'Oro',)

    # Net production for the other materials
    [m.print_net_prod() for m in net_prod]
    
    # Value for the other materials
    tot = calc_mtl_value(net_prod)
    print_mtl_value(tot)

    caption = 'Controvalore totale in ducati delle risorse minerarie'\
                ' prodotte al netto dei costi di manutenzione e spese'
    print_tot(net_gold + tot, caption)

    print_tags('center', 'color=black')
    print('Il Ministro delle Miniere e delle Grandi Opere\n')
    sign_link = 'https://i.imgur.com/AIPMgz8.png'
    print(f'[img]{sign_link}[/img]')
    seal_link = 'https://i.ibb.co/LY5mhSH/mdm.png'
    print(f'[img]{seal_link}[/img]')
    print_tags('/center', '/color')
    print_tags('/rp')

if __name__ == '__main__':
    main()