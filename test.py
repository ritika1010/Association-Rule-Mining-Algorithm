import itertools
import sys
from collections import defaultdict

def read_dataset(filename):
    transactions = []
    with open(filename, 'r') as file:
        next(file)  # Skip header
        for line in file:
            line = line.strip().split(',')
            transaction = line[:4]  # Extracting the relevant columns for items
            transactions.append(transaction)
    return transactions

# def apriori_gen(L_prev, k):
#     if k == 2:
#         C2 = []
#         for i in range(len(L_prev)):
#             for j in range(i+1, len(L_prev)):
#                 C2.append([L_prev[i], L_prev[j]])
#         return C2
#     else:
#         # Implement generation of candidate itemsets for k > 2
#         pass
def apriori_gen(L_prev, k):
    if k == 2:
        C2 = []
        for i in range(len(L_prev)):
            for j in range(i+1, len(L_prev)):
                C2.append([L_prev[i], L_prev[j]])
        return C2
    else:
        Ck = []
        for i in range(len(L_prev)):
            for j in range(i+1, len(L_prev)):
                # Check if the first k-2 items are the same
                if L_prev[i][:-1] == L_prev[j][:-1]:
                    # Join step: merge the two itemsets
                    new_itemset = list(set(L_prev[i]).union(set(L_prev[j])))
                    new_itemset.sort()  # Sorting for consistency
                    # Pruning step: check if all subsets of length k-1 are in L_prev
                    if all([subset in L_prev for subset in itertools.combinations(new_itemset, k-1)]):
                        Ck.append(new_itemset)
        return Ck


def calculate_support(transaction_list, itemset):
    count = 0
    for transaction in transaction_list:
        if set(itemset).issubset(set(transaction)):
            count += 1
    return count / len(transaction_list)

def main():
    data_file = sys.argv[1]
    min_sup = float(sys.argv[2])
    min_conf = float(sys.argv[3])

    transactions = read_dataset(data_file)
    total_transactions = len(transactions)

    # First pass to count item occurrences
    item_counts = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_counts[item] += 1

    # Extract large 1-item sets
    L1 = [item for item, count in item_counts.items() if count / total_transactions >= min_sup]

    L = [L1]
    k = 2

    while len(L[k-2]) > 0:
        Ck = apriori_gen(L[k-2], k)
        Lk = []

        for itemset in Ck:
            support = calculate_support(transactions, itemset)
            if support >= min_sup:
                Lk.append((itemset, support))
        
        L.append(Lk)
        k += 1

    # Output frequent itemsets
    print("==Frequent itemsets (min_sup={}%)==".format(min_sup * 100))
    for level in L:
        for itemset in level:
            print("{}\t supp: {:.2f}%".format(itemset, support * 100))

    
    # Generate association rules
    associations = []
    for level in L[1:]:
        for itemset, _ in level:
            for i in range(1, len(itemset)):
                for subset in itertools.combinations(itemset, i):
                    remaining = [item for item in itemset if item not in subset]
                    confidence = calculate_support(transactions, itemset) / calculate_support(transactions, list(subset))
                    if confidence >= min_conf:
                        associations.append((subset, remaining, confidence))

    # Output high-confidence association rules
    print("\n==High-confidence association rules (min_conf={}%)==".format(min_conf * 100))
    for lhs, rhs, conf in associations:
        print("{} ==> {} \t conf: {:.2f}%".format(lhs, rhs, conf * 100))

if __name__ == "__main__":
    main()
