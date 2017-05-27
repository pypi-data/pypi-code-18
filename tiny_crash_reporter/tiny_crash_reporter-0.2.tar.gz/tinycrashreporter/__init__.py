def crashReportExceptHook(exctype, value, tb):
                        try:
                                    print ("{0}: {1}".format(exctype.__name__, value))
                        except:
                                    raise Exception("Unexpected error in Tiny Crash Reporter.")
                        
