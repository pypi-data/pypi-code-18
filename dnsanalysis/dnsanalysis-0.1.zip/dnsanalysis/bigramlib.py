from collections import Counter


def importFromFile(filename):
        f = open(filename, 'r')
        domains = f.readlines()
        f.close()
        return domains

def domainToBigrams(domain):
        bigram = []
        for text in domain.split('.'):
                for i in range(len(text)-1):
                        bigram.append(text[i] + text[i+1])
        return bigram


def domainsToBigrams(domains):
        bigram = []
        for domain in domains:
                bigram.extend(domainToBigrams(domain))
        return bigram


def bigramFrequencyList(bigram):
        return Counter(bigram).most_common()
