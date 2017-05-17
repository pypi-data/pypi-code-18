


from stepist.flow import step, Hub


@step(None)
def step3(a):
    print("step3")
    return {'c': 'd', 'a': a}


@step(None)
def step2(a):
    print("step2")
    return {'a': 'b'}


@step(Hub(step2, step3))
def step1(a):
    return dict(a=a)



print(step1(a='b'))
