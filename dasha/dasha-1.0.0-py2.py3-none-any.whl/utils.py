class Finder(object):
    def search_group(self, content, words):
        if not isinstance(words, list) or not isinstance(words, set):
            raise TypeError('Words must be a list or set')
        if not all(isinstance(word, str) for word in words):
            raise TypeError('All words in words list must be a string')
        matched = {}
        for word in words:
            matched.update({word: len(self.__search__(content, word))})
        return matched

    def search(self, content, word):
        return len(self.__search__(content, word))

    @staticmethod
    def __partial__(pattern):
        """ Calculate partial match table: String -> [Int]"""
        ret = [0]

        for i in range(1, len(pattern)):
            j = ret[i - 1]
            while j > 0 and pattern[j] != pattern[i]:
                j = ret[j - 1]
            ret.append(j + 1 if pattern[j] == pattern[i] else j)
        return ret

    def __search__(self, text, pattern):
        """ 
        KMP search main algorithm: String -> String -> [Int] 
        Return all the matching position of pattern string Pattern in String
        """
        partial, ret, j = self.__partial__(pattern), [], 0

        for i in range(len(text)):
            while j > 0 and text[i] != pattern[j]:
                j = partial[j - 1]
            if text[i] == pattern[j]:
                j += 1
            if j == len(pattern):
                ret.append(i - (j - 1))
                j = 0
        return ret
