from itertools import combinations
from datetime import date

PEOPLE_ABBRS = ['Li', 'Mi', 'Pa', 'Sa', 'Se', 'St']
#LINDA, MICHELLE, PANDU, SAM, SEAN, STACY = range(6)
PEOPLE_NAMES = ['Linda', 'Michelle', 'Pandu', 'Sam', 'Sean', 'Stacy']

def main():
    lines = input_until_blank()
    transactions = read_lines(lines)

    output = 'Everything added up\n'
    amounts_owed = add_transactions(transactions)
    output += str_amounts_owed_readable(amounts_owed)

    amounts_owed = simplify(amounts_owed, False)
    output += '\nWith things canceled out\n'
    output += str_amounts_owed_readable(amounts_owed)

    output += '\nTabbed\n'
    output += str_amounts_owed_tabbed(amounts_owed)

    output += '\nData\n'
    for t in transactions:
        output += str(t) + '\n'
    outfile = 'out-{0}.txt'.format(date.today().isoformat())
    with open(outfile, 'w') as f:
        f.write(output)

def simplify(amounts_owed, verbose):
    for a, b in combinations(PEOPLE_NAMES, 2):
        if amounts_owed[a][b] < 0.0001 or amounts_owed[b][a] < 0.0001:
            continue
        elif amounts_owed[a][b] < amounts_owed[b][a]:
            if verbose:
                print(b, 'owes more than', a)
            amounts_owed[b][a] = amounts_owed[b][a] - amounts_owed[a][b]
            amounts_owed[a][b] = 0
        else:
            if verbose:
                print(a, 'owes more than or equal to', b)
            amounts_owed[a][b] = amounts_owed[a][b] - amounts_owed[b][a]
            amounts_owed[b][a] = 0
        #input('wait')
        if verbose:
            print_amounts_owed_readable(amounts_owed)
    return amounts_owed

def add_transactions(transactions):
    # amounts_owed[x][y] is how much x owes y

    amounts_owed = {x: {y: 0 for y in PEOPLE_NAMES} for x in PEOPLE_NAMES}
    for t in transactions:
        for debtor, included in zip(PEOPLE_NAMES, t.debtors):
            if included:
                amounts_owed[debtor][t.owedto] += t.amount
    return amounts_owed

COL_WIDTH = 7
def str_amounts_owed_readable(amounts_owed):
    s = ' '*10 + ''.join(p.ljust(COL_WIDTH) for p in PEOPLE_ABBRS)
    s += 'ASSETS'.ljust(COL_WIDTH)
    s += 'LIAB'.ljust(COL_WIDTH)
    s += 'NET'.ljust(COL_WIDTH)
    for debtor in PEOPLE_NAMES:
        s += '\n' + debtor.ljust(10)
        for owedto in PEOPLE_NAMES:
            s += '{0:.2f}'.format(amounts_owed[debtor][owedto]).ljust(COL_WIDTH)
        s += '{0:.2f}'.format(assets(amounts_owed, debtor)).ljust(COL_WIDTH)
        s += '{0:.2f}'.format(liabilities(amounts_owed, debtor)).ljust(COL_WIDTH)
        s += '{0:.2f}'.format(assets(amounts_owed, debtor) - liabilities(amounts_owed, debtor)).ljust(COL_WIDTH)
    s += '\n'
    return s

def print_amounts_owed_readable(amounts_owed):
    print(str_amounts_owed_readable(amounts_owed))

def str_amounts_owed_tabbed(amounts_owed):
    s = ''
    for debtor in PEOPLE_NAMES:
        for owedto in PEOPLE_NAMES:
            s += '{0:.2f}\t'.format(amounts_owed[debtor][owedto])
        s += '\n'
    return s

def liabilities(amounts_owed, person):
    amount = 0
    for debt in amounts_owed[person].values():
        amount += debt
    return amount

def assets(amounts_owed, person):
    amount = 0
    for debts in amounts_owed.values():
        amount += debts[person]
    return amount

class Transaction:
    def __init__(self, date, owedto, debtors, amount, reason):
        self.date = date
        self.owedto = owedto
        self.debtors = debtors # List of True and False
        self.amount = amount
        self.reason = reason

    @property
    def debtors_str(self):
        s = ''
        for person, included in zip(PEOPLE_ABBRS, self.debtors):
            if included:
                s += person
            else:
                s += '--'
        return s

    def __repr__(self):
        date = self.date
        owedto = self.owedto.ljust(9)
        debtors = self.debtors_str
        amount = '{0:.2f}'.format(self.amount).ljust(5)
        reason = self.reason
        return '{0}  {1}  {2}  {3}  {4}'.format(date, owedto, debtors, amount, reason)

def input_until_blank():
    line = input('? ')
    lines = []
    while line:
        if not line.startswith('#ignore'):
            lines.append(line)
        line = input('? ')
    return lines

def read_lines(lines):
    transactions = []
    for line in lines:
        info = line.split('\t')
        date, owedto, L, M, P, Sa, Se, St, amount, reason = info
        debtors = [L, M, P, Sa, Se, St]
        debtors = [x == 'x' for x in debtors]
        amount = float(amount)
        transactions.append(Transaction(date, owedto, debtors, amount, reason))
    return transactions

main()
