import os, sys, time
import numpy as np

class arpa_parser(object):
    def __init__(self, text_file, script_file, bDeleteFiles=True):
        self.reset()
        
        command = "sh " + script_file + " " + text_file
        os.system(command)

        arpa_file = text_file+'.arpa'
        
        if not os.path.exists(arpa_file):
            raise Exception("Arpa file not generated")

        self.parse(arpa_file)

        if bDeleteFiles:
            files_to_delete = [arpa_file, arpa_file[:-4]+'vocab', arpa_file[:-4]+'wfreq', arpa_file[:-4]+'idngram']
            for f in files_to_delete:
                os.remove(f)
                
    def reset(self):
        self.unigrams = {}
        self.unigrams_fallback = {}
        self.bigrams = {}
        self.bigrams_fallback = {}
        self.trigrams = {}
        self.trigrams_fallback = {}
        
    def get_lines(self,file):
        with open(file, "r") as f:
            lines = []
            while True:
                line = f.readline()
                if line == "":
                    break
                lines.append(line)
        return lines
    
    def parse(self, file):
        lines = self.get_lines(file)
        
        bState = 'header'
        for i, line in enumerate(lines):
            line = line.replace(' ', '\t')
            if bState == 'header':
                if line[:6] == '\\data\\':
                    bState = 'starting'
            elif bState == 'starting':
                if line[:8] == '\\1-grams':
                    bState = '1-grams'
            elif bState == '1-grams':
                if line[:8] == '\\2-grams':
                    bState = '2-grams'
                elif line[:1] == '-':
                    self.add_unigram_line(line)
            elif bState == '2-grams':
                if line[:8] == '\\3-grams':
                    bState = '3-grams'
                elif line[:1] == '-':
                    self.add_bigram_line(line)
            elif bState == '3-grams':
                if line[:5] == '\\end\\':
                    break
                elif line[:1] == '-':
                    self.add_trigram_line(line)
            else:
                print('unknown state, breaking')
                raise Exception('unknown state, breaking')
                
    def add_unigram_line(self, line):
        entries = line[:-1].split('\t')
        self.unigrams[entries[1]] = float(entries[0])
        if len(entries) == 3:
            self.unigrams_fallback[entries[1]] = float(entries[2])
            
    def add_bigram_line(self, line):
        entries = line[:-1].split('\t')
        bg = entries[1].replace(' ', '_')
        self.bigrams[bg] = float(entries[0])
        if len(entries) == 3:
            self.bigrams_fallback[bg] = float(entries[2])
    
    def add_trigram_line(self, line):
        entries = line[:-1].split('\t')
        tg = entries[1].replace(' ', '_')
        self.trigrams[tg] = float(entries[0])
        if len(entries) == 3:
            self.trigrams_fallback[tg] = float(entries[2])
            
    def get_comparative_to_general_lm(self, unigrams_general):
        comparative_language_model = {}
        for key in self.unigrams.keys():
            if key in unigrams_general:
                comparative_language_model[key] = np.log10(max((np.power(10, self.unigrams[key]) - np.power(10, unigrams_general[key])), 0))
            else:
                comparative_language_model[key] = self.unigrams[key]
        return comparative_language_model
