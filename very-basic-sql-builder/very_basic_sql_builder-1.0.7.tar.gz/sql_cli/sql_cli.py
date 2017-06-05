from __future__ import print_function

import re
import json
import click

TAB = "\t"
NEW_LINE = "\n"
COMMA = ","
COMMENT_OPEN = "/*"
COMMENT_CLOSE = "*/"

# Helper functions
## General
def shallow_flatten_uniq(list_of_lists):
    "Helper function returns a 1D list of unique items in a 2D list"
    new_list = []
    for list_ in list_of_lists:
        for item in list_:
            if item not in new_list:
                new_list.append(item)
    return new_list

## Configuration file
def handle_config_item(config_file, item):
    "Load item from `config_file` or prompt then save to `config_file`"
    try:
        datum = load_value_from_file(config_file, item["name"])
        item["value"] = datum
        return item
    except KeyError:
        data = load_data(config_file)
        datum = confirm_or_prompt(item["prompt"])
        data[item["name"]] = datum
        item["value"] = datum
        with open(config_file, "w") as fout:
            json.dump(data, fout)
        return item
    except FileNotFoundError:
        item["value"] = confirm_or_prompt(item)["value"]
        with open(config_file, "w") as fout:
            config = {item["name"]: datum}
            json.dump(config, fout)
        return item

# Load value(s) from main file
def load_data(filename):
    "Helper method returns json.load() of `filename`"
    with open(filename, "r") as fin:
        return json.load(fin)


def load_value_from_file(filename, key):
    "Helper function return `key` item from `filename`"
    return load_data(filename)[key]


def load_blocks(filename):
    "Return `blocks` item from `filename`"
    return load_value_from_file(filename, "blocks")


def load_meta_data(filename):
    "Return `meta_data` item from `filename`"
    return load_value_from_file(filename, "meta_data")


def load_variables(filename):
    "Return `variables` item from `filename`"
    return load_value_from_file(filename, "variables")


# click.prompt() / click.confirm() functions
def confirm_or_prompt(item):
    "Parent method, used to split calls to click.prompt/click.confirm"
    prompt = item["prompt"]

    if prompt["type"].lower() == "confirm":
        return get_value_from_confirm_prompt(item)
    return get_value_from_regular_prompt(item)


def get_value_from_confirm_prompt(item):
    "Add result from click.confirm to `item` and return"
    prompt = item["prompt"]
    text = prompt["text"]

    if "default" in prompt:
        default = prompt["default"]
        if default.lower() in ["y", "yes", "true"]:
            default = True
        else:
            default = False
        prompt_value = click.confirm(text, default=default)
    else:
        prompt_value = click.confirm(text)

    item["value"] = prompt_value

    return item


def get_value_from_regular_prompt(item):
    "Add result from click.prompt to `item` and return"
    prompt = item["prompt"]
    text = prompt["text"]

    if prompt["default"]:
        default = prompt["default"]
        if prompt["type"]:
            type_ = eval(prompt["type"]) # @TODO: remove eval
            item["value"] = click.prompt(text, default=default, type=type_)
            return item
        item["value"] = click.prompt(text, default=default)
        return item

    if prompt["type"]:
        type_ = eval(prompt["type"]) # @TODO: remove eval
        item["value"] = click.prompt(text, type=type_)
        return item

    item["value"] = click.prompt(text)
    return item

# SQL
## SQL variable definitions/declarations
def find_required_variables(from_clause):
    "Yield SQL variables present in from clause"
    lines = from_clause.split("\n")
    match_string = re.compile(r"@[a-zA-Z]+")
    for line in lines:
        variables = match_string.finditer(line)
        for variable in variables:
            yield variable.string[variable.start():variable.end()]

def generate_variable_definition(filename, variable_name):
    "Return SQL variable definition from file or commented declaration"
    name = variable_name.replace("@", "")
    print(name)
    try:
        variables = load_variables(filename)

        if name in variables:
            return variables[name]

    except: #  TODO: Make this intelligent
        return "-- DECLARE {variable_name} -- definition required;".format(
            variable_name=variable_name
        )


def generate_variable_definitions(config_file, variable_declarations):
    "Create an iterable with variable definitions"
    for decl in variable_declarations:
        yield generate_variable_definition(config_file, decl)


# Build SQL strings
def generate_meta_data_string(meta_data):
    "Builds a formatted string from filtered metadata components"
    meta_data_string = "{comment_open}{whitespace}".format(
        comment_open=COMMENT_OPEN,
        whitespace=NEW_LINE
        )

    for item in meta_data:
        meta_data_string += "{tabs}{value}{new_lines}".format(
            tabs=TAB,
            value=item["string"],
            new_lines=NEW_LINE
            )
        meta_data_string += "{tabs}{value}{new_lines}".format(
            tabs=(TAB * 2),
            value=str(item["value"]),
            new_lines=(NEW_LINE * 2)
            )

    meta_data_string += "{comment_close}{whitespace}".format(
        comment_close=COMMENT_CLOSE,
        whitespace=(NEW_LINE * 2)
        )

    return meta_data_string


def join_variable_definitions(variable_definitions):
    "Create new_line separated string from iterable of SQL variables definitions"
    variable_string = "{new_line}".format(
        new_line=NEW_LINE
        ).join(variable_definitions)

    return "{new_line}{variable_string}{new_lines}".format(
        new_line=NEW_LINE,
        variable_string=variable_string,
        new_lines=(NEW_LINE * 2)
    )


def generate_select_clause_string(blocks):
    "Generate a SELECT clause string from `blocks`"
    select_statements = shallow_flatten_uniq(
        [
            block["select_fields"]
            for block
            in blocks
        ]
    )

    select_string = "SELECT{new_line}{tab}".format(
        new_line=NEW_LINE,
        tab=TAB
        )

    whitespace = "{new_line}{tab}{comma}".format(
        new_line=NEW_LINE,
        tab=TAB,
        comma=COMMA
    )

    return "{start}{end}".format(
        start=select_string,
        end=whitespace.join(select_statements)
    )


def generate_from_clause_string(blocks):
    "Generate a FROM clause string from `blocks`"
    from_statements = shallow_flatten_uniq(
        [
            block["from_clauses"]
            for block
            in blocks
        ]
    )

    from_string = "{new_line}FROM{new_line}{tab}".format(
        new_line=NEW_LINE,
        tab=TAB
    )

    whitespace = "{new_line}".format(new_line=NEW_LINE)

    return "{start}{end}".format(
        start=from_string,
        end=whitespace.join(from_statements)
    )



# Filters
def filter_meta_data(meta_data, config_file):
    """Parent method that will store and retrieve values from a config file
    if `item['store_in_config'] == True`"""
    for item in meta_data:
        if "store_in_config" in item:
            if item["store_in_config"].lower() == "true":
                yield handle_config_item(config_file, item)
            else:
                yield confirm_or_prompt(item) # test this
        else:
            yield confirm_or_prompt(item)


def filter_blocks(blocks):
    "Yield SELECT and FROM blocks as per user selection (confirm/prompt)"
    for item in blocks:
        prompt_value = confirm_or_prompt(item)
        
        if prompt_value["value"]:
            yield prompt_value


# Create suggested filename
def suggest_output_filename(meta_data):
    """Generate a recommended filename if `title`, `dataset` and `version` exist in `meta_data`,
    otherwise suggest `abc.sql`"""
    for item in meta_data:
        if ("name" in item) and ("value" in item):
            if item["name"].lower() == "title":
                title = item["value"]
            if item["name"].lower() == "dataset":
                dataset = item["value"]
            if item["name"].lower() == "version":
                version = str(item["value"])

    try:
        return "{title} - {dataset} Dataset - v{version}.sql".format(
            title=title,
            dataset=dataset,
            version=version
        )
    except UnboundLocalError:
        return "abc.sql"

# Join SQL components and write to file
def build_sql_file(
        filename,
        meta_data_string,
        select_clause,
        from_clause,
        variable_declarations=None):
    "Build SQL file string from components and write to `filename`"

    with open(filename, 'w') as fout:
        print("Writing meta-data to {filename}...".format(filename=filename))
        fout.write(meta_data_string)
        if variable_declarations:
            print("Writing variable declarations to {filename}...".format(filename=filename))
            fout.write(variable_declarations)
        print("Writing select clause to {filename}...".format(filename=filename))
        fout.write(select_clause)
        print("Writing from clause to {filename}...".format(filename=filename))
        fout.write(from_clause)


def main():
    # File locations
    DATA_FILE = "sql_cli_data.json"
    CONFIG_FILE = "config.json"

    # Meta data
    meta_data = load_meta_data(DATA_FILE)
    meta_data = filter_meta_data(meta_data, CONFIG_FILE)
    meta_data = list(meta_data)
    meta_data_string = generate_meta_data_string(meta_data=meta_data)

    # Filename
    OUTPUT_FILENAME_SUGGESTION = suggest_output_filename(meta_data)
    OUTPUT_FILENAME = click.prompt(
        "Filename",
        default=OUTPUT_FILENAME_SUGGESTION
    )

    # Blocks
    blocks = load_blocks(DATA_FILE)
    blocks = filter_blocks(blocks)
    blocks = list(blocks)

    # SELECT
    select_clause = generate_select_clause_string(blocks)

    # FROM
    from_clause = generate_from_clause_string(blocks)

    # DECLARE @variable_declarations
    variable_declarations = find_required_variables(from_clause)
    variable_definitions = generate_variable_definitions(DATA_FILE, variable_declarations)
    variable_declaration_string = join_variable_definitions(variable_definitions)


    # Write contents to file
    build_sql_file(
        OUTPUT_FILENAME,
        meta_data_string,
        select_clause,
        from_clause,
        variable_declaration_string
    )


if __name__ == "__main__":
    main()