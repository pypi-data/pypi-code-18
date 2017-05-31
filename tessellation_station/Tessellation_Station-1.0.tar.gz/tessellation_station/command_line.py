from ast import literal_eval

class Error(Exception):
    def __init__(self, message):
        self.message = message

class CLI(object):

    def __init__(self):
        self.transformations = []
        self.configurations = []
        self.controlls = []
        self.loop = []
        self.capture_loop = False
        self.polygon = None
        self.origin = None

    def add_transformation(self, func):
        self.transformations.append(func)
        return func

    def add_configuration(self, func):
        # The bolean is so we cann track if the command has been ran
        self.configurations.append([func,False])
        return func

    def add_control(self, func):
        self.controlls.append(func)
        return func

    @staticmethod
    def _parse(text):
        parsed = []
        if text[0] == "#":
            return None

        try:
            command, arguments = text.split(">")
        except ValueError:
            if text == "":
                raise Error("No Command")

        arguments = arguments.split(", ")
        parsed_arguments = {}
        for i, arg in enumerate(arguments):
            parsed_arguments.update({i:literal_eval(arg)})

        parsed = [command, parsed_arguments]
        return parsed

    def run_command(self, function, arguments):
        try:
            arguments.update({"polygon":self.polygon, "origin":self.origin})
            result = function(arguments)

        except TypeError:
            if self.polygon == None:
                raise Error("Define a polygon with 'polygon>'")
            raise
        return result

    def step(self, line):
        try:
            command, arguments = self._parse(line)

        except TypeError:
            return "comment"

        try:
            for function in self.controlls:
                if function.__name__ == command:
                    return "controlls"

            if self.capture_loop:
                        self.loop.append(command)

            for function in self.transformations:
                # Check for transformation commands
                if function.__name__ == command:
                    result = self.run_command(function, arguments)
                    self.polygon = result
                    #make movements realative
                    self.origin = self.polygon[0]
                    return result

            for function in self.configurations:
                # Check for configuration commands
                if function[0].__name__ == command:
                    if function[1]:
                        # Config commands should only be used once, so raise an error if they try again
                        raise Error("Configuration command already ran")

                    function[1] = True
                    self.run_command(function[0], arguments)
                    return "config" # return "config" so we know to delete it

            raise Error("Not a Command")

        except KeyboardInterrupt:
            print("\n You can exit using 'leave>()'")

        except Error as error:
            raise