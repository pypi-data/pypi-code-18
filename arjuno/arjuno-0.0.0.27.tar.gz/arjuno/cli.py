import sys
from optparse import OptionParser
from libs import check_serial

def optional_arg(arg_default):
    def func(option,opt_str,value,parser):
        if parser.rargs and not parser.rargs[0].startswith('-'):
            val=parser.rargs[0]
            parser.rargs.pop(0)
        else:
            val=arg_default
        setattr(parser.values,option.dest,val)
    return func

def example():
    return "v0.1"

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-v","--version",dest="version",help="display version",action='callback',callback=optional_arg('empty'))
    parser.add_option("-c","--check",dest="check_serial",help="check serial available",action='callback',callback=optional_arg('empty'))
    parser.add_option("-r","--read",dest="read_serial",help="read string to serial device",action='callback',callback=optional_arg('empty'))
    parser.add_option("-w","--write",dest="write_serial",help="write string to serial device",action='callback',callback=optional_arg('empty'))


    (options, args) = parser.parse_args(sys.argv)
    if options.version:
        print example()
    elif options.check_serial:
        print check_serial.serial_ports()
    elif options.read_serial and option.write_serial:
        print "asd"
    
