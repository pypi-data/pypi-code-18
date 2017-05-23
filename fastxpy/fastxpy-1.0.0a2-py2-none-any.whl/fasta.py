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
