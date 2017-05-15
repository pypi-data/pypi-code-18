import urllib
import datetime
import threading
import time
import os
import tempfile

def downloadBinaryFromSymbolsServer( filename, date_time=None, file_size=None, dbg_id=None, custom_symbols_server=None ):
    if not dbg_id:
        if isinstance(date_time, str):
            # Minuts Hours DayOfTheMonth Month Year
            date_time = int(time.mktime(time.strptime(date_time, '%M %H %d %m %Y')))
        elif not isinstance(date_time, (int, long)):
            date_time = int(time.mktime(date_time))
        elif not data_time:
            raise Exception("Missing information")
        dbg_id = '%X%X' % (date_time, file_size)

    if None != custom_symbols_server:
        symbols_server = custom_symbols_server
    else:
        symbols_server = os.environ.get('_NT_SYMBOL_PATH', "http://msdl.microsoft.com/download/symbols/")
    for server in symbols_server.split(';'):
        cacheDir = None
        if "*" in server:
            _, cacheDir, server = tuple(server.split('*'))
        if not server.startswith('http'):
            continue

        cacheFileName = None
        if cacheDir:
            cacheFileName = os.path.join(cacheDir, filename, dbg_id, filename)
            if os.path.isfile(cacheFileName):
                return cacheFileName

        url = server
        if url[-1] != "/":
            url += "/"
        url += filename
        url += "/"
        url += dbg_id
        url += "/"

        for filenameToDownload in [filename, filename[:-1] + '_']:
            class MSURLOpener(urllib.FancyURLopener):
                verison = "Microsoft-Symbol-Server/6.2.9200.16384"
            msurlOpener = MSURLOpener()
            msurlOpener.addheader("Accept-Encoding", "gzip")
            msurlOpener.addheader("User-Agent", "Microsoft-Symbol-Server/6.2.9200.16384")
            msurlOpener.addheader("Host", "msdl.microsoft.com")
            msurlOpener.addheader("Connection", "Keep-Alive")
            msurlOpener.addheader("Cache-Control", "no-cache")
            urllib._urlopener = msurlOpener
            if cacheFileName:
                outputFileName = cacheFileName
                os.makedirs(os.path.dirname(outputFileName))
            else:
                ext = filename.split(os.path.extsep)[-1]
                outputFileName = tempfile.mktemp('.' + ext)
            try:
                urllib.urlretrieve(url+filenameToDownload, outputFileName)
            except urllib.HTTPError, e:
                continue
            return outputFileName

def normalizeDate(date):
    if isinstance(date, tuple):
        date = int(time.mktime((date[0], date[1], date[2], 0, 0, 0, 0, 0, 0)))
    elif isinstance(date, (int, long)):
        pass
    elif isinstance(date, None):
        date = int(time.mktime(time.strptime(end.ctime())))
    else:
        raise Exception("Don't know how to translate the date to int")
    return date

def _setStartAndEndDate(date):
    # Make the end time/date the begging of the next day
    start = normalizeDate(date)
    start_date = datetime.date.fromtimestamp(start)
    end = start_date + datetime.timedelta(days=1)
    end = int(time.mktime(time.strptime(end.ctime())))
    if end <= start:
        raise Exception("Faild to caculate the end date %x" % end)
    return (start, end)

def bruteForceDateTimeDownload(filename, date, file_size, is_verbose=True):
    start, end = _setStartAndEndDate(date)
    function_timing = time.time()
    if is_verbose:
        print "Starting from timestamp %x" % start
        print "Would end on timestamp  %x" % end
    for date_time in range(start, end):
        try:
            r = downloadBinaryFromSymbolsServer(filename, date_time, file_size)
            if None != r:
                print hex(date_time)
                return r
            attempts = 0
            if is_verbose and date_time == (date_time & 0xfffffff0):
                running_time = time.time() - function_timing
                number_of_execuations = date_time - start
                avg = float(number_of_execuations) / running_time
                if 0 != avg:
                    left = end - date_time
                    left_sec = float(left) / avg
                    print "Last attempt:", hex(date_time), "Secs passed:", int(running_time), "Avg of", avg, "quries/sec. ~%f secs left" % left_sec
        except Exception, e:
            print e
            attempts += 1
            if attempts > 3:
                raise e
            time.sleep(2)

class CreateBruteForceThread(threading.Thread):
    def __init__(self, filename, start, end, file_size, is_verbose=True):
        self.filename = filename
        self.start = start
        self.end = end
        self.file_size = file_size
        self.is_verbose = is_verbose
        self.result = None
        threading.Thread.__init__(self)
    def run(self):
        self.result = bruteForceDateTimeDownload(self.filename, self.start, self.file_size, self.end)

# Fix this shit
def runMultiThreadBruteForce(filename, start, file_size, num_threads=10, is_verbose=True):
    start, end = _setStartAndEndDate(date)
    last_start = start
    thread_range = 0x1000
    running_threads = []
    result = None
    while None == result:
        if len(running_threads) < num_threads:
            t = CreateBruteForceThread(filename, last_start, last_start + thread_range, file_size, is_verbose)
            running_threads.append(t)
            last_start += thread_range

#
#mainModulePE = patFinder.searchOne(PE.ImageDosHeader, base)
#timestamp = mainModulePE.PE.FileHeader.TimeDateStamp
#moduleSize = mainModulePE.PE.OptionalHeader.ImageSize
#debugDirOff = mainModulePE.PE.OptionalHeader.DebugDir.VirtualAddress
#debugDir = patFinder.searchOne(PE.ImageDebugDirectory, base + debugDirOff)
#dbgIdAddr = base + debugDir.AddrOfRawData + 4
#dbgId  = m.readMemory(dbgIdAddr, 4)[::-1].encode('hex').upper(); dbgIdAddr += 4
#dbgId += m.readMemory(dbgIdAddr, 2)[::-1].encode('hex').upper(); dbgIdAddr += 2
#dbgId += m.readMemory(dbgIdAddr, 2)[::-1].encode('hex').upper(); dbgIdAddr += 2
#dbgId += m.readMemory(dbgIdAddr, 8).encode('hex').upper(); dbgIdAddr += 8
#dbgId += '%X' % m.readByte(dbgIdAddr)
#
