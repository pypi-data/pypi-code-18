import re


class Lexer:
    def parse(self, line):
        words = re.split(r'(\s+)', line)
        result = []

        for word in words:
            if word.startswith("/"):
                result.append((word, "command"))
                continue

            if ":" in word:
                ts = word.split(":")
                result.append((ts[0], "arg"))
                if ts[1]:
                    result.append((ts[1], "string"))
                continue

            if word:
                result.append((word, "string"))


        return result