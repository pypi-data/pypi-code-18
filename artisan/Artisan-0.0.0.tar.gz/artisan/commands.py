def combine(*commands):

    def init(app):
        for command in commands:
            app.cli.add_command(command)

    return init
