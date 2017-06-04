def power(values):
    for value in values:
        print 'powering %s' % value
        yield value

def adder(values):
    for value in values:
        print 'adding to %s'%value 
        if value % 2 == 0:
            yield value + 3
        else:
            yield value + 2

elements = [1,4,7,9,12,19]
res = adder(power(elements))

res.next()


# example 2

def getPower():
    print 'Please enter a number between 0 and 100'
    response = None 
    while True:
        response = (yield)

        if response is not None:
            if not isinstance(response, int):
                print "\t Please enter the number not character"

            elif response < 0:
                print "\t Please enter positive number"

            elif response > 100:
                print "\t Please enter the number smaller than 100"
            else:
                print '\t Result is %s'%response*response

        else:
            print '\t\t idle with no response...'
            



gen = getPower()

gen.next()
print '................'
gen.send(-10)

print '................'
gen.send(101)

print '................'
gen.send(50)