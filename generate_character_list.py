"""
Download the latest unicode tables from  https://www.unicode.org and create a .txt file
containing all the names, blocks and character codes
"""


def main():
    indices = []
    blocks = []
    with open("Blocks.txt", "r") as block_file:
        for line in block_file.readlines():
            if line.startswith("#"):
                continue
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
                    return index

    with open("unicode_list.txt", "w") as target:
        with open("UnicodeData.txt", "r") as names:
            for line in names.readlines():
                attributes = line.strip().split(";")
                code = attributes[0]
                name = attributes[1]
                comment = attributes[10]
                try:
                    num = int(code, 16)
                except ValueError:
                    print("could not convert " + code)
                    continue
                index = locate_block(num)
                if index is not None:
                    target.write(name + "\t" + comment + "\t" + code + "\t" + blocks[index] + "\n")
                else:
                    print(
                        "Code " + str(num) + " not found in block, char: " + unichr(num)
                    )
                    target.write(name + "\t" + comment + "\t" + code + "\t" + "\n")


if __name__ == "__main__":
    main()
