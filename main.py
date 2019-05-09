import sys

sys.path.append("/home/zen/.local/lib/python2.7/site-packages/")

import os
from os.path import join
import time
import codecs
from ulauncher.search.SortedList import SortedList

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

# Be compatible with both python 2 and 3
if sys.version_info[0] >= 3:
    unichr = chr

FILE_PATH = os.path.dirname(sys.argv[0])

ICON_TEMPLATE = """
<svg  width="100" height="100">
    <text x="50" y="50" dy=".35em" text-anchor="middle" font-family="{font}" font-size="80">{symbol}</text>
</svg>
"""


class UnicodeChar:
    """ Container class for unicode characters """

    def __init__(self, name, block, code):
        self.name = name
        self.block = block
        self.code = code
        self.character = unichr(int(code, 16))

    def get_search_name(self):
        """ Called by `ulauncher.search.SortedList` to get the string that should be used in searches """
        return self.name


class UnicodeCharExtension(Extension):
    def __init__(self):
        super(UnicodeCharExtension, self).__init__()
        self._load_character_table()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    def _load_character_table(self):
        """ Read the data file and load to memory """
        self.character_list = []
        with open(join(FILE_PATH, "unicode_list.txt"), "r") as f:
            for line in f.readlines():
                name, code, block = line.strip().split("\t")
                character = UnicodeChar(name, block, code)
                self.character_list.append(character)


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        arg = event.get_argument()
        if arg:
            result_list = SortedList(arg, min_score=60, limit=10)
            result_list.extend(extension.character_list)
            for char in result_list:
                image_path = self._get_character_icon(char)
                items.append(
                    ExtensionResultItem(
                        icon=image_path,
                        name=char.name + " - " + char.character,
                        description=char.block + " - " + char.code,
                        on_enter=CopyToClipboardAction(char.character),
                    )
                )

        return RenderResultListAction(items)

    def _get_character_icon(self, char):
        path = sys.argv[0] + "images/cache/icon_%s.svg" % char.code
        if os.path.isfile(path):
            return path
        return create_character_icon(char)


def is_icon_cached(code):
    return os.path.isfile(os.path.join(FILE_PATH, "images/cache/icon_%s.svg" % code))


def create_character_icon(char, font="sans-serif"):
    """ Create an SVG file containing the unicode glyph for char to be used
    as a result icon.

    Note: this could be avoided by providing a gtk.PixBuf without creating a file,
    but ulauncher pickles the returned results, so it doesn't work currently.
    """
    icon = ICON_TEMPLATE.replace("{symbol}", char.character).replace("{font}", font)
    with codecs.open(
        os.path.join(FILE_PATH, "images/cache/icon_%s.svg" % char.code), "w", "utf-8"
    ) as target:
        target.write(icon)
    return os.path.join(FILE_PATH, "images/cache/icon_%s.svg" % char.code)


if __name__ == "__main__":
    UnicodeCharExtension().run()
