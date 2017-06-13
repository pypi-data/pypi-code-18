from pycopa.exception import PycopaException
from pycopa.result import ParserResult


class Parser:
    __DEFAULT_ARG_NAME = "arg"

    def parse(self, tokens):
        waiting_for_token = ["command"]
        current_arg = self.__DEFAULT_ARG_NAME
        args = [current_arg]
        result = {self.__DEFAULT_ARG_NAME: ""}

        for token in tokens:
            value, cls = token

            if cls not in waiting_for_token:
                raise PycopaException("Waiting for {} but {} given".format(" or ".join(waiting_for_token), cls))

            if cls == "command":
                waiting_for_token = ["string", "arg"]
                result["command"] = value

            if cls == "arg":
                waiting_for_token = ["string"]
                result[value] = ""
                current_arg = value
                args.append(value)

            if cls == "string":
                waiting_for_token = ["string", "arg"]
                result[current_arg] += value

        for arg in args:
            result[arg] = result[arg].strip()

        return ParserResult(result)
