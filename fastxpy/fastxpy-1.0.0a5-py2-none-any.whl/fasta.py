def getseqs(file_name):
    with open(file_name, "r") as f:
        seqs =[]
        seq = ""
        f.readline()

        for line in f:
            line = line.strip()

            if line[0] == ">":
                seqs.append(seq)
                seq = ""
            else:
                seq += line

    return seqs

def getheads(file_name):
    with open(file_name, "r") as f:
        headers= []

        for line in f:
            if line[0] == ">":
                headers.append(line.strip())

    return headers

class fa(file):
    def __init__(self, name):
        self._lastheader = 0
        self._offset = 0
        super(fa, self).__init__(name)

    def readline(self):
        line = super(fa, self).readline()

        if line[0] == ">":
            self._lastheader += self._offset
            self._offset = 0

        self._offset += len(line)

        return line

    def readheader(self):
        for line in self:
            if line[0] == ">":
                return line
        return None

    def prevheader(self):
        prev = self.tell()
        self.seek(self._lastheader)
        header = self.readline()
        self.seek(prev)
        return header

    def gotoprevheader(self):
        self.seek(self._lastheader)
        return self.readline()

    def readseq(self, keepstyle=True, processing=False):
        head = self.readline()

        if not head[0] == ">":
            head = self.gotoprevheader()

        line = self.readline()
        seq = ""
        while line and line[0] != ">":
            if not keepstyle:
                line = line.strip()

            seq += line
            line = self.readline()

        offset = len(line)
        if keepstyle: offset += 1

        self.seek(self.tell() - offset)

        if processing:
            return head.strip(), seq.strip()

        else:
            result = head + seq
            return result





