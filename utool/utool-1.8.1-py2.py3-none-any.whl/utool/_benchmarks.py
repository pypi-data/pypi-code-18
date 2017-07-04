
def unique_flag_benchmarks():
    import random
    import utool as ut
    import ubelt as ub
    import plottool as pt

    def random_items(n, m):
        rng = random.Random(0)
        return [rng.randint(0, n) for _ in range(m)]

    m = 1000

    def method1(items):
        seen = set()
        def unseen(item):
            if item in seen:
                return False
            seen.add(item)
            return True
        flag_list = [unseen(item) for item in items]
        return flag_list

    def method2(items):
        return ut.index_to_boolmask([items.index(x) for x in set(items)], len(items))

    def method3(items):
        return ut.index_to_boolmask(dict(zip(reversed(items), reversed(range(len(items))))).values(), len(items))

    ub.Timerit.DEFAULT_VERBOSE = False

    ut.qtensure()
    exps = [0, .25, .5, .75, 1, 2]
    pnum_ = pt.make_pnum_nextgen(nSubplots=len(exps))
    current = ut.flag_unique_items

    for count, exp in ut.ProgIter(list(enumerate(exps, start=1))):
        ydatas = ut.ddict(list)
        xdata = []
        for m in ut.ProgIter(list(range(0, 10000, 100)), freq=1):
            xdata.append(m)
            num = 10
            n = int(m ** exp)
            items = random_items(n=n, m=m)
            ydatas['method1'].append(ub.Timerit(num).call(method1, items))
            ydatas['method2'].append(ub.Timerit(num).call(method2, items))
            ydatas['method3'].append(ub.Timerit(num).call(method3, items))
            ydatas['current'].append(ub.Timerit(num).call(current, items))

            # assert method1(items) == method3(items)
            # assert method1(items) == current(items)

        pt.multi_plot(
            xdata, list(ydatas.values()), label_list=list(ydatas.keys()),
            ylabel='time', title=str(exp), fnum=1, pnum=pnum_())


def unique_items_benchmarks():
    import random
    import utool as ut
    import ubelt as ub
    import plottool as pt

    def random_items(n, m):
        rng = random.Random(0)
        return [rng.randint(0, n) for _ in range(m)]

    m = 1000

    def method1(items):
        seen = set()
        def unseen(item):
            if item not in seen:
                seen.add(item)
                return True
            return False
        return [item for item in items if unseen(item)]

    def method4_(items):
        seen = set()
        for item in items:
            if item not in seen:
                seen.add(item)
                yield item

    def method4(items):
        return list(method4_(items))

    def method5_(items):
        unseen = set(items)
        for item in items:
            if item in unseen:
                unseen.remove(item)
                yield item

    def method5(items):
        return list(method4_(items))

    def method2(items):
        len_ = len(items)
        unique_indices = dict(zip(reversed(items), reversed(range(len_))))
        return [items[idx] for idx in sorted(unique_indices.values())]

    ub.Timerit.DEFAULT_VERBOSE = False

    ut.qtensure()
    exps = [0, .5, .75, 1.5]
    pnum_ = pt.make_pnum_nextgen(nSubplots=len(exps))

    methods = {
        # 'method1': method1,
        'method2': method2,
        'ub.unique': ub.unique,
        'method4': method4,
        'method5': method5,
    }

    methods_similar = {
        'set': set
    }

    for count, exp in ut.ProgIter(list(enumerate(exps, start=1))):
        ydatas = ut.ddict(list)
        xdata = []
        for m in ut.ProgIter(list(range(0, 50000, 5000)), freq=1):
            xdata.append(m)
            num = 10
            n = int(m ** exp)
            items = random_items(n=n, m=m)
            for (key1, func1), (key2, func2) in ut.itertwo(methods.items()):
                assert func1(items) == func2(items), '{} {}'.format(key1, key2)

            for key, func in methods.items():
                ydatas[key].append(ub.Timerit(num).call(func, items))

            for key, func in methods_similar.items():
                ydatas[key].append(ub.Timerit(num).call(func, items))

        pt.multi_plot(
            xdata, list(ydatas.values()), label_list=list(ydatas.keys()),
            ylabel='time', title=str(exp), fnum=1, pnum=pnum_())
