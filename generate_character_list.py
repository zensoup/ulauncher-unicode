"""
Download the latest unicode tables from  https://www.unicode.org and create a .txt file
containing all the names, blocks and character codes
"""
import os
import logging
from urllib import request

curr_path = os.path.dirname(__file__)
logging.basicConfig(level=logging.DEBUG)


def get_blocks():
    """ Download the info file for Unicode blocks.
    """
    logging.info("Downloading block data...")
    req = request.urlopen("https://www.unicode.org/Public/UCD/latest/ucd/Blocks.txt")
    content = req.read().decode()
    logging.info("Done")
    return content


def get_data():
    """ Download the info file for Unicode blocks.
    """
    logging.info("Downloading block data...")
    req = request.urlopen(
        "https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt"
    )
    content = req.read().decode()
    logging.info("Done")
    return content


def clean(text):
    """ Remove all blank or commented lies from a string
    """
    lines = text.strip().split("\n")
    clean_lines = [line.strip() for line in lines if line.strip() and line[0] != "#"]
    return "\n".join(clean_lines)


def load_blocks():
    """ Load and parse the block data and return a function that provides block
    search based on a character code.
    """
    indices = []
    blocks = []
    block_data = clean(get_blocks())
    for line in block_data.split("\n"):
        l, name = line.split(";")
        start, stop = l.split("..")
        indices.append((int(start, 16), int(stop, 16)))
        blocks.append(name.strip())

    def locate_block(code):
        for index, [start, stop] in enumerate(indices):
            if code > stop:
                continue
            else:
                if code >= start:
                    return blocks[index]

    return locate_block


def main():
    get_block = load_blocks()
    characters = clean(get_data())

    logging.info("Parsing character data...")

    output = []
    for line in characters.split("\n"):
        # Parse the needed data
        attributes = line.strip().split(";")
        code = attributes[0]
        name = attributes[1]
        comment = attributes[10]

        # Convert character code to unicode
        try:
            num = int(code, 16)
        except ValueError:
            logging.warn("Could not convert " + code)
            continue

        # Find the character's block
        blk = get_block(num)
        if blk is not None:
            output.append("\t".join((name, comment, code, blk)))
        else:
            logging.warn("Code %s not found in any block, char: %s", num, unichr(num))
            output.append(name + "\t" + comment + "\t" + code + "\t")

    with open("unicode_list.txt", "w") as target:
        target.write("\n".join(output))


if __name__ == "__main__":
    main()
