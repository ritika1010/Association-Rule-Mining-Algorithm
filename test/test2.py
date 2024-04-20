import itertools
import string
import sys
import sqlite3  # Import sqlite3 module
from collections import defaultdict
from tables import *
from operator import itemgetter

# python3 main.py INTEGRATED-DATASET.csv 0.01 0.5

def create_tables():
    conn = sqlite3.connect("candidates.db")    # connecting to the database
    crsr = conn.cursor()    # cursor

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
    if(k == 2):
        for i, item in enumerate((L_prev)):
            # SQL command to insert the data in the table
            crsr.execute("""INSERT INTO L1(item1) 
                        VALUES (?);""", (item,))
            conn.commit()
        # execute the command to fetch all the data from the table L1
        crsr.execute("INSERT INTO C2(item1, item2)\
                    SELECT A.item1, B.item1\
                    FROM L1 AS A, L1 AS B\
                    WHERE A.item1 < B.item1")

        # Pruning step: not needed here because we pass L_prev = L1.copy()
        # in the first run. L_prev contains single items that have min_support

        # After pruning
        crsr.execute("SELECT item1, item2 FROM C2")
        C2 = crsr.fetchall()  
        return C2
    elif(k == 3):
        for i, item in enumerate(L_prev):
            crsr.execute("""INSERT INTO L2(item1, item2) 
                        VALUES (?,?);""", (item[0],item[1]))
            conn.commit()
        crsr.execute("INSERT INTO C3(item1, item2, item3)\
                    SELECT A.item1, A.item2, B.item2\
                    FROM L2 AS A, L2 AS B\
                    WHERE A.item1 = B.item1 AND\
                    A.item2 < B.item2")

        # Pruning step
        crsr.execute("SELECT item1, item2, item3 FROM C3")
        C3 = crsr.fetchall()
        for i, c in enumerate(C3):
            for s in itertools.combinations(c, 2):
                if(s not in L_prev):
                    crsr.execute("""DELETE FROM C3 WHERE item1=(?) AND item2=(?) AND item3=(?);""",(c[0],c[1],c[2]))
        # After pruning
        crsr.execute("SELECT item1, item2, item3 FROM C3")
        C3 = crsr.fetchall()
        return C3
    elif(k == 4):
        for i, item in enumerate(L_prev):
            crsr.execute("""INSERT INTO L3(item1, item2, item3) 
                        VALUES (?,?,?);""", (item[0],item[1],item[2]))
            conn.commit()
        crsr.execute("INSERT INTO C4(item1, item2, item3, item4)\
                SELECT A.item1, A.item2, A.item3, B.item3\
                FROM L3 AS A, L3 AS B\
                WHERE A.item1 = B.item1 AND\
                A.item2 = B.item2 AND\
                A.item3 < B.item3")

        # Pruning step
        crsr.execute("SELECT item1, item2, item3, item4 FROM C4")
        C4 = crsr.fetchall()
        for i, c in enumerate(C4):
            # print(i, c)
            for s in itertools.combinations(c, 3):
                if(s not in L_prev):
                    # print(s)
                    crsr.execute("""DELETE FROM C4 WHERE item1=(?) AND item2=(?) AND item3=(?) AND item4=(?);""",(c[0],c[1],c[2],c[3]))
        crsr.execute("SELECT item1, item2, item3, item4 FROM C4")
        C4 = crsr.fetchall()
        return C4
    else:
        return {}

def main():
    crsr, conn = create_tables()

    data = sys.argv[1] 
    min_sup = float(sys.argv[2])
    min_conf = float(sys.argv[3])
    transaction = []

    # itemsets = set()
    dataset_rows = 0
    total_rows = 0

    csvreader = open(data, 'r')
    for i, row in enumerate(csvreader):

        # skip the header with column names
        if(i == 0):
            continue

        row = row.strip().rstrip(",")
        row = row.lower()

        row_split = list(row.split(','))

        transaction.append(row_split)
        
        dataset_rows += 1
        total_rows += int(row_split[4])
    
    ### First pass: counts item occurrences to determine the large 1-items

    first_pass = defaultdict(int)
    L = [set()]  # keep track of all items sets of all sizes
    L1 = set()   # Large item sets of exactly 1-elements

    # Count num times each item appears in dataset
    for i, trans in enumerate(transaction):
        for item in trans[0:4]:
            first_pass[item] += int(trans[4])  # summing count values for each individual item in a particular row
    
    # Calculate support, populate L1 with 1-items with > min_supp
    L_temp = {}
    for item in first_pass:
        support = first_pass[item] / total_rows
        if(support >= min_sup):
            L_temp[item] = support
            L1.add(item)

    L.append(L_temp)

    ### A priori algorithm

    k = 2
    L_prev = L1.copy()  # Set of large k-1 itemsets
    C_t = set()
    while len(L_prev) > 0:
        next_pass = defaultdict(int)

        C_k = apriori_gen(L_prev, k, crsr, conn) # Set of candidate k itemsets (potentially large)
        L_prev = set()

        # Count num times each item appears in dataset
        for i, trans in enumerate(transaction):
            for item in C_k:
                if(set(item).issubset(set(trans))):
                    next_pass[item] += int(trans[4])

        # Calculate support, populate L2 in L with 2-items with > min_supp
        L_temp = {}
        for item in next_pass:
            support = next_pass[item] / total_rows
            if(support >= min_sup):
                L_temp[item] = support
                L_prev.add(item)

        L.append(L_temp)
        k += 1

    ## Get associations
    associations = set()
    for k in range(2, len(L)):
        for c in L[k]:
            # K == 4
            if(k == 4):
                # print('>>>', c, '\tsupp: ', L[4][c])
                for s in itertools.combinations(c, 3):
                    # (LHS U RHS)/(LHS)
                    if(L[4][c]/L[3][s] >= min_conf):
                        # print(s, '---->', tuple(set(c) - set(s)), '\t conf: ', L[4][c]/L[3][s], '\t supp: ', L[4][c])
                        associations.add((s,tuple(set(c) - set(s)), L[4][c]/L[3][s], L[4][c]))
            elif(k == 3):
                for s in itertools.combinations(c, 2):
                    # (LHS U RHS)/(LHS)
                    if(L[3][c]/L[2][s] >= min_conf):
                        # print(s, '---->', tuple(set(c) - set(s)), '\t conf: ', L[3][c]/L[2][s], '\t supp: ', L[3][c])
                        associations.add((s, tuple(set(c) - set(s)), L[3][c]/L[2][s], L[3][c]))
            elif(k == 2):
                # (LHS U RHS)/(LHS)
                if(L[2][c]/L[1][c[0]] >= min_conf):
                    # print(tuple((c[0],)), '---->', tuple((c[1],)), '\t conf: ', L[2][c]/L[1][c[0]], '\t supp: ', L[2][c])
                    associations.add((tuple((c[0],)), tuple((c[1],)), L[2][c]/L[1][c[0]], L[2][c]))
                if(L[2][c]/L[1][c[1]] >= min_conf):
                    # print(tuple((c[1],)), '---->', tuple((c[0],)), '\t conf: ', L[2][c]/L[1][c[1]], '\t supp: ', L[2][c])
                    associations.add((tuple((c[1],)), tuple((c[0],)), L[2][c]/L[1][c[1]], L[2][c]))

    # Create output file

    f = open("output.txt", "w")
    f.write(("==Frequent itemsets (min_sup={}%)==\n").format(min_sup * 100))
    
    itemsets = []

    # For each possible itemset size, append the individual row with conf
    for i in range(2, len(L)):
        for itset in L[i]:
            itemsets.append((itset, L[i][itset]))

    # Sort the itemsets by support
    itemsets.sort(key = itemgetter(1), reverse=True)
    
    # Output all itemsets in order
    for itset in itemsets:
        f.write(str(itset[0]) + '\t supp: ' + str(round(itset[1] * 100, 2)) + '%\n')

    f.write('\n\n\n')

    # Sort associations in decreasing order of confidence
    associations = list(associations)
    associations.sort(key = itemgetter(2), reverse=True)

    f.write(("==High-confidence association rules (min_conf={}%)==\n").format(min_conf * 100))
    for asc in list(associations):
        # print(asc)
        f.write(str(asc[0]) + ' ===> ' + str(asc[1]) + '\t conf: ' + str(round(asc[2] * 100, 2)) + '% \t supp: ' + str(round(asc[3] * 100,2)) + '%\n')

if __name__=="__main__":
    main()
