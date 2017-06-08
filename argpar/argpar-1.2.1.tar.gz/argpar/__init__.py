from sys import exit

def list2str(l):
	ret = ""
	for i in l:
		ret = ret + i
	return ret

def opt_get(opt, args):
	opt = "-" + opt
	val = args[args.index(opt) + 1]
	args.remove(opt)
	args.remove(val)
	return val, args

def opt_get_od(opt, args, defaultvalue):
	try:
		return opt_get(opt, args)
	except ValueError:
		return defaultvalue, args

def opts_get(opts, args):
	ret = {}
	for opt in opts:
		ret[opt], args = opt_get(opt, args)
	return ret, args

def opts_get_od(opts, args):
	ret = {}
	for opt in list(opts.keys()):
		ret[opt], args = opt_get_od(opt, args, opts[opt])
	return ret, args

def flag_get(flag, args):
	flag = "-" + flag
	if flag in args:
		args.remove(flag)
		return True, args
	else:
		return False, args

def flags_get(flags, args):
	ret = {}
	for flag in flags:
		ret[flag], args = flag_get(flag, args)
	return ret, args

def posarg_get(args):
	ret = args[1:][-1]
	args.remove(ret)
	return ret, args

def posarg_get_od(args, defaultvalue):
	try:
		return posarg_get(args)
	except IndexError:
		return defaultvalue, args

def parse_args(opts, args, flags=[], posarg={}):
	ret = {}
	ret, args = opts_get_od(opts, args)
	r, args = flags_get(flags, args)
	ret.update(r)
	try:
		ret[list(posarg.keys())[0]], args = posarg_get_od(args, list(posarg.values())[0])
	except IndexError:
		pass
	return ret

def help_get(opts, args, flags, posarg):
	if posarg:
		posarg = list(posarg.keys())[0].upper()
	else:
		posarg = ""
	return "Usage: {} -{}{} {}".format(args[0].split("/")[-1], list2str(opts.keys()), list2str(flags), posarg)

def help_print(opts, args, flags, posarg):
	print(help_get(opts, args, flags, posarg))
	exit(0)

def parse(opts, args, flags=[], posarg={}):
	if flag_get("h", args)[0]:
		help_print(opts, args, flags, posarg)

	return parse_args(opts, args, flags, posarg)