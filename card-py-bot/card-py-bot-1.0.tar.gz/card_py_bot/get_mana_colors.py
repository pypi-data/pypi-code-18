""" Handler function for advanced parsing on the wizzards website,
specifically for grabbing both the image data and mana data of a card """
import re
import os
import urllib.request


def read_in_website(input_link):
    """
    ARGS:

    RETURNS:
    """
    with urllib.request.urlopen(input_link) as response:
        lines = []
        oldline = ""

        for lineprt in response.read():
            lineprt = chr(lineprt)
            if lineprt == '\n':
                oldline = str(oldline)
                if oldline.strip() == "":
                    continue
                else:
                    lines.append(oldline.strip())
                    oldline = ""
            oldline = oldline + lineprt
    return lines


def make_mana_dict():
    mana_dict = dict()

    mana_colors_list = [
        'Green', 'Red', 'Blue', 'Black', 'White',
        'Phyrexian Blue', 'Phyrexian Red', 'Phyrexian Green',
        'Phyrexian Black', 'Phyrexian White',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
        '11', '12', '13', '14', '15', '16', '1000000',
        'Black or Green', 'Red or White', 'Green or Blue',
        'Blue or Red', 'White or Black', 'White or Blue',
        'Blue or Black', 'Black or Red', 'Red or Green',
        'Green or White', 'Two or White', 'Two or Green',
        'Two or Black', 'Two or Red', 'Two or Blue'
    ]

    config_file = open(os.path.dirname(
        os.path.abspath(__file__)) + '/' + 'mana_config.txt', "r")
    counter = 0

    for mana_emoji_id in config_file.readlines():
        mana_dict[mana_colors_list[counter]] = mana_emoji_id
        counter += 1

    config_file.close()
    return mana_dict


def recuse_mana(start_line_counter, lines):
    mana_tot = []

    mana_dict = make_mana_dict()

    def recuse_mana_r(line_pos, line):
        if line.find("alt=", line_pos) >= 0:
            start_indx = line.find("alt=")
            oldline = ""
            for i in range(start_indx + 5, len(line) - 1):
                if line[i] == '"':
                    try:
                        oldline = mana_dict[oldline].strip()
                    except KeyError:
                        for i in range(int(oldline)):
                            mana_tot.append(":white_circle:")
                        break

                    mana_tot.append(oldline)
                    break

                oldline = oldline + line[i]

            recuse_mana_r(0, line[start_indx + 4:])

    div_counter = 0

    for i in range(start_line_counter + 1, len(lines) - 1):
        line = lines[i]

        if line.find('<div') >= 0:
            div_counter += 1
        if line.find('</div>') >= 0:
            div_counter -= 1
        if div_counter == 0:
            break

    recuse_mana_r(0, line)

    mana_string = " ".join(mana_tot)
    return mana_string


def get_img_link(line):
    line = str(line)
    start_indx = line.find('src="')

    line = line[start_indx + 5:]
    end_indx = line.find('"')
    line = line[5:end_indx].strip()

    line = re.sub("amp;", "", line)

    return line


def get_card_mana_string(lines):

    line_counter = 0
    grabbed_mana = 0

    for i in range(len(lines)):
        line = lines[i]

        if line.find('Mana Cost:</div>') >= 0 and grabbed_mana == 0:
            card_mana = recuse_mana(i, lines)
            card_mana = str(card_mana)
            grabbed_mana = 1

        if line.find('<div class="cardImage">') >= 0:
            img_link = get_img_link(lines[i + 1])

        line_counter += 1

    return (card_mana, img_link)


def get_mana(url):
    lines = read_in_website(url)
    return get_card_mana_string(lines)
