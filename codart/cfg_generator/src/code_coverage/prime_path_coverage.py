import networkx as nx
import math
from collections import defaultdict
from .path_finder import prime_paths


def check(l1, l2):
    # return True if list2 is sublist of list1 but order of l2 is same in l1.
    index_list = [i for i, v in enumerate(l1) if v == l2[0]]
    for ii in index_list:
        l1_slice = l1[ii:ii + len(l2)]
        if l1_slice == l2:
            return True
    else:
        return False


def checkSubset(list1, list2):
    # return True if list2 is sublist of list1.
    exist = True
    for i in list2:
        if i not in list1:
            exist = False
    return exist


def overlap(a, b):
    # return continiusly overlap of two list
    flag = False
    for i in range(len(b), 0, -1):
        if a[-i:] == b[0:i]:
            flag = True
            result = i
    if flag is True:
        return a[:] + b[result:]
    else:
        return []


def path_request(test_path, primes):
    # map each test path with test requirement
    tr_tp = defaultdict(list)
    tp_tr = defaultdict(list)
    for i in test_path:
        for j in primes:
            if check(i, j) is True:
                tp_tr[str(i)].append(j)
                tr_tp[str(j)].append(i)
    return tp_tr


def prime_path(g, first, last):
    # return prime path of graph
    primes = prime_paths(g, first, last)
    return primes


def compute_P(g, first):
    # first algorithm use BFS to create small set of path's
    P = list()
    ll = nx.bfs_tree(g, first)
    for i in nx.nodes(g):
        ss = nx.all_simple_paths(ll, first, i)
        for j in list(ss):
            P.append(j)
    return P


def compute_TP(g, P, first, last):
    """
    The heuristic algorithm for generating a small
    set of test paths
    """
    # if the last node of pi ∈ F then
    TP = list()
    new_P = P
    for path in P:
        if first == path[0] and last == path[-1]:
            TP.append(path)
            if path not in TP:
                new_P.remove(path)

    # if pi includes fj  chop the sub-path pij from the beginning tothe position where fj is in pi
    neww_p = new_P
    for path in new_P:
        if first == path[0] and last in path:
            path[:path.index(last)]
            neww_p.remove(path)
            if path not in TP:
                TP.append(path)

    # the last node of not pi ∈ F
    for path in neww_p:
        if first == path[0]:
            aa = list()
            paths = nx.single_source_shortest_path(g, path[-1])
            destination_node = last
            if destination_node in paths:
                aa = paths[destination_node]
            if path + aa[1:] not in TP:
                TP.append(path + aa[1:])
    return TP


def super_request(g, first, last):
    # use set coverage greedy algorithm to find minimum super test requirement list.
    tp_tr = defaultdict(list)
    super_req = list()

    # put the super-test requirement sk of tri and trj intoa set S where k>0
    S = list()
    tr = prime_path(g, first, last)
    for i in range(0, len(tr)):
        for j in range(0, len(tr)):
            if i != j:
                a = overlap(tr[i], tr[j])
                if a != [] and a not in S:
                    S.append(a)

    # compute the cost-effectiveness of g
    test_req = tr + S
    new = tr.copy()
    covered = list()
    while new != []:
        cost_efftectivness = {}
        tp_tr = path_request(test_req, new)
        for key, val in tp_tr.items():
            effectiveness = 0
            for j in val:
                if j not in covered:
                    effectiveness += 1
            cost = len(eval(key))
            div = cost / effectiveness
            cost_efftectivness[key] = div
        # find gi with the minimum cost-effectiveness and extend the super-test requirement Π with g
        min_list = list()
        minn = math.inf
        for num, i in enumerate(list(cost_efftectivness.values())):
            if i < minn:
                minn = i
                min_list = list()
                min_list.append(num)
            elif i == minn:
                min_list.append(num)
        minimum = math.inf
        for i in min_list:
            if len(eval(list(tp_tr.keys())[i])) < minimum:
                minimum = len(eval(list(tp_tr.keys())[i]))
                min_index = i
        super_req += eval(list(tp_tr.keys())[min_index])
        for i in tp_tr[list(tp_tr.keys())[min_index]]:
            if i not in covered:
                covered.append(i)
            if i in new:
                new.remove(i)
    return super_req


def spliting_super(g, super_req, TP, first, last):
    # cut the super requrement list to exe cution path's.
    TR = prime_path(g, first, last)
    edgg = list()
    edg = nx.edges(g)
    ans_tp = list()
    ans_tr = list()
    go_to_brute = list()
    for i in edg:
        edgg.append(list(i))
    end_res = list()
    a = 0
    while a < len(super_req) - 1:
        p = []
        a += 1
        p.append(super_req[a - 1])
        while a < len(super_req) and [super_req[a - 1], super_req[a]] in edgg:
            p.append(super_req[a])
            a += 1
        end_res.append(p)
    complete_tp_tr = path_request(end_res, TR)
    for i in end_res:
        if i[0] == first and i[-1] == last:
            ans_tp.append(i)
            ans_tr.append(complete_tp_tr[str(i)])
        else:
            go_to_brute.append(i)

    ctp = brute_force(TP, go_to_brute, first, last)
    last_tp, last_tr = minimize(ctp, TR)
    result_tp = last_tp + ans_tp
    result_tr = last_tr + ans_tr
    return result_tp, result_tr


def brute_force(TP, TR, first, last):
    # you can find method definition and functionality in article.

    # each test requirement tri ∈ T R that is not covered by T P
    not_covered = list()
    res = list()
    for tr in TR:
        for tp in TP:
            if check(tp, tr) is False:
                if tr not in not_covered:
                    not_covered.append(tr)
    for path in not_covered:
        new_path = []
        new_path = path.copy()
        while new_path[0] != first or new_path[-1] != last:
            for tp in TP:
                if new_path[0] != first and new_path[0] in tp:
                    new_path = tp[:tp.index(new_path[0])] + new_path[:]
                elif new_path[-1] != last and new_path[-1] in tp:
                    new_path = new_path[:] + tp[tp.index(new_path[-1]) + 1:]
        if new_path not in res:
            res.append(new_path)
    return res


def minimizing(CTP, TR):
    # delete redundant path
    tp_tr = path_request(CTP, TR)
    new = list()
    for i in tp_tr.values():
        for j in i:
            if j not in new:
                new.append(j)

    dele = list()
    for p1, r1 in tp_tr.items():
        for p2, r2 in tp_tr.items():
            if p1 != p2:
                if checkSubset(list(r1), list(r2)) is True:
                    if p2 not in dele and (p1 not in dele and len(r2) != len(r1)):
                        dele.append(p2)
    for i in dele:
        del tp_tr[i]

    new = list()
    for i in tp_tr.values():
        for j in i:
            if j not in new:
                new.append(j)
    return list(tp_tr.keys())


def minimize(CTP, TR):
    # other algorithm for delete redundant path
    result_tr = list()
    result_tp = list()
    tp_tr = path_request(CTP, TR)
    for p1, r1 in tp_tr.copy().items():
        duplicate = []
        for p2, r2 in tp_tr.copy().items():
            if p1 != p2:
                for k in r1:
                    if k in r2 and k not in duplicate:
                        duplicate.append(k)
        flag = True
        for o in duplicate:
            if o in r1:
                pass
            else:
                flag = False
        if flag is True and len(duplicate) == len(r1):
            del tp_tr[p1]

    for i in tp_tr.keys():
        result_tp.append(eval(i))

    for j in tp_tr.values():
        result_tr.append(j)

    return result_tp, result_tr


def prime_path_coverage_superset(g, first, last):
    # firs method for prime path coverage.
    P = compute_P(g, first)
    TP = compute_TP(g, P, first, last)
    super_req = super_request(g, first, last)
    end_tp, end_tr = spliting_super(g, super_req, TP, first, last)
    return end_tp, end_tr


def prime_path_coverage_bruteforce(g, first, last):
    # second method for prime path coverage.

    TR = prime_path(g, first, last)
    P = compute_P(g, first)
    TP = compute_TP(g, P, first, last)
    ctp = brute_force(TP, TR, first, last)
    end_tp, end_tr = minimize(ctp, TR)
    return end_tp, end_tr
