import itertools
import string
import sys
import sqlite3
from collections import defaultdict
import sqlite3  # Import sqlite3 module
from tables import *
from operator import itemgetter

# Define table creation statements
table_L1 = """CREATE TABLE IF NOT EXISTS L1(
            item1 TEXT);"""

table_L2 = """CREATE TABLE IF NOT EXISTS L2(
            item1 TEXT,
            item2 TEXT);"""

table_L3 = """CREATE TABLE IF NOT EXISTS L3(
            item1 TEXT,
            item2 TEXT,
            item3 TEXT);"""

table_C2 = """CREATE TABLE IF NOT EXISTS C2(
            item1 TEXT,
            item2 TEXT);"""

table_C3 = """CREATE TABLE IF NOT EXISTS C3(
            item1 TEXT,
            item2 TEXT,
            item3 TEXT);"""

table_C4 = """CREATE TABLE IF NOT EXISTS C4(
            item1 TEXT,
            item2 TEXT,
            item3 TEXT,
            item4 TEXT);"""

def create_tables():
    conn = sqlite3.connect("candidates.db")
    crsr = conn.cursor()

    print("Connected to the database")

    crsr.execute("DROP TABLE if Exists L1")
    crsr.execute("DROP TABLE if Exists L2")
    crsr.execute("DROP TABLE if Exists L3")
    crsr.execute("DROP TABLE if Exists C2")
    crsr.execute("DROP TABLE if Exists C3")
    crsr.execute("DROP TABLE if Exists C4")

    crsr.execute(table_L1)
    crsr.execute(table_L2)
    crsr.execute(table_L3)

    crsr.execute(table_C2)
    crsr.execute(table_C3)
    crsr.execute(table_C4)

    conn.commit()

    return crsr, conn

def apriori_gen(L_prev, k, crsr, conn):
    if k == 2:
        for i, item in enumerate((L_prev)):
            crsr.execute("""INSERT INTO L1(item1) 
                        VALUES (?);""", (item,))
            conn.commit()

        crsr.execute("INSERT INTO C2(item1, item2)\
                    SELECT A.item1, B.item1\
                    FROM L1 AS A, L1 AS B\
                    WHERE A.item1 < B.item1")

        crsr.execute("SELECT item1, item2 FROM C2")
        C2 = crsr.fetchall()  
        return C2 if C2 else []

def main():
    crsr, conn = create_tables()

    data = sys.argv[1] 
    min_sup = float(sys.argv[2])
    min_conf = float(sys.argv[3])
    transaction = []

    dataset_rows = 0
    total_rows = 0

    csvreader = open(data, 'r')
    for i, row in enumerate(csvreader):
        if i == 0:
            continue

        row = row.strip().rstrip(",")
        row = row.lower()
        row_split = list(row.split(','))

        # Skip rows that don't have the expected number of elements
        if len(row_split) != 7:
            continue

        try:
            # Extract numerical values and sum them
            deaths = int(row_split[4])
            total_rows += deaths
        except ValueError:
            # If the value cannot be converted to an integer, skip this row
            continue
        
        transaction.append(row_split)
        dataset_rows += 1
    
    first_pass = defaultdict(int)
    L = [set()]
    L1 = set()

    for i, trans in enumerate(transaction):
        for item in trans[0:4]:
            first_pass[item] += int(trans[4])
    
    L_temp = {}
    for item in first_pass:
        support = first_pass[item] / total_rows
        if support >= min_sup:
            L_temp[item] = support
            L1.add(item)

    L.append(L_temp)

    k = 2
    L_prev = L1.copy()
    C_t = set()
    while len(L_prev) > 0:
        next_pass = defaultdict(int)
        C_k = apriori_gen(L_prev, k, crsr, conn)
        L_prev = set()

        for i, trans in enumerate(transaction):
            if C_k is None:
                continue
            for item in C_k:
                if set(item).issubset(set(trans)):
                    next_pass[item] += int(trans[4])

        L_temp = {}
        for item in next_pass:
            support = next_pass[item] / total_rows
            if support >= min_sup:
                L_temp[item] = support
                L_prev.add(item)

        L.append(L_temp)
        k += 1

    associations = set()

    for k in range(2, len(L)):
        for c in L[k]:
            for s in itertools.combinations(c, k-1):
                if k == 4:
                    if L[4][c]/L[3][s] >= min_conf:
                        associations.add((s, tuple(set(c) - set(s)), L[4][c]/L[3][s], L[4][c]))
                elif k == 3:
                    if L[3][c]/L[2][s] >= min_conf:
                        associations.add((s, tuple(set(c) - set(s)), L[3][c]/L[2][s], L[3][c]))
                elif k == 2:
                    if L[2][c]/L[1][c[0]] >= min_conf:
                        associations.add((tuple((c[0],)), tuple((c[1],)), L[2][c]/L[1][c[0]], L[2][c]))
                    if L[2][c]/L[1][c[1]] >= min_conf:
                        associations.add((tuple((c[1],)), tuple((c[0],)), L[2][c]/L[1][c[1]], L[2][c]))

    f = open("example-run.txt", "w")
    f.write(("==Frequent itemsets (min_sup={}%)==\n").format(min_sup * 100))
    
    itemsets = []

    for i in range(2, len(L)):
        for itset in L[i]:
            itemsets.append((itset, L[i][itset]))

    itemsets.sort(key = itemgetter(1), reverse=True)
    
    for itset in itemsets:
        f.write(str(itset[0]) + '\t supp: ' + str(round(itset[1] * 100, 2)) + '%\n')

    f.write('\n\n\n')

    associations = list(associations)
    associations.sort(key = itemgetter(2), reverse=True)

    f.write(("==High-confidence association rules (min_conf={}%)==\n").format(min_conf * 100))
    for asc in list(associations):
        f.write(str(asc[0]) + ' ===> ' + str(asc[1]) + '\t conf: ' + str(round(asc[2] * 100, 2)) + '% \t supp: ' + str(round(asc[3] * 100,2)) + '%\n')

if __name__=="__main__":
    main()
