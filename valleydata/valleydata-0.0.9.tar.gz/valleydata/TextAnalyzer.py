import operator
from collections import Counter


class TextAnalyzer:
    def __init__(self, texts):
        self._textList = texts
        self.words_in_groups = {}
        for group in self.groups:
            self.words_in_groups[group] = self.get_most_used_words(group)

    @property
    def texts(self):
        return [text['text'] for text in self.textList]

    @property
    def textList(self):
        return self._textList

    @property
    def groups(self):
        """Return available groups

        Returns:
            list: List of strings
        """
        return list(
            set([item['status'] for item in self.textList])
        )

    def get_group(self, value):
        return [
            text['text'] for text in self.textList if text['status'] is value
        ]

    def get_ranking(self, text):
        points = {}
        totalPoints = 0
        for group in self.groups:
            points[group] = 0
            words = text.split()
            ranking = dict(self.get_most_used_words(group=group))
            for word in words:
                if word in ranking:
                    if group is 'approved':
                        totalPoints += 1
                    else:
                        totalPoints -= 1

                    points[group] += 1
        return points, totalPoints

    def get_most_used_words(self, group):
        word_occurrences = {}
        for text in self.get_group(group):
            single_text_occurrences = Counter(text.lower().split())
            for sto in single_text_occurrences.most_common():
                word = sto[0]
                qty = sto[1]
                if word in word_occurrences:
                    word_occurrences[word] = word_occurrences[word] + qty
                else:
                    word_occurrences[word] = qty

        sorted_wo = sorted(
            word_occurrences.items(),
            key=operator.itemgetter(1)
        )
        sorted_wo.reverse()
        return sorted_wo