import sys

sys.path.append("/home/zen/.local/lib/python2.7/site-packages/")

import os
import codecs
from ulauncher.search.SortedList import SortedList

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


FILE_PATH = os.path.dirname(sys.argv[0])

class SearchableItem:
    def __init__(self, name, item):
        self._name = name
        self._item = item

    def get_search_name(self):
        return self._name

class UnicodeCharExtension(Extension):
    def __init__(self):
        super(UnicodeCharExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def __init__(self):
        print('======'*40)
        f = open(os.path.dirname(sys.argv[0]) + "/unicode_list.txt", "r")
        data = f.readlines()
        self.data = {}
        # self.names = []
        self.items = []
        self.items_ = []
        # self.blocks = []
        for item in data:
            item = item.strip()
            name, code, block = item.split("\t")
            self.data[name + " " + block] = (name, block, code)
            self.items.append(name + " " + block)
            self.items_.append(SearchableItem(name , (name, block, code)))
            # self.names.append(name)
            # self.blocks.append(block)

    def on_event(self, event, extension):
        items = []
        arg = event.get_argument()
        if arg:

            m_ = SortedList(arg, min_score=60, limit=10)
            m_.extend(self.items_)
            for m in m_:
                name, block, code = m._item
                image_path = self.create_icon_image(code)
                items.append(
                    ExtensionResultItem(
                        icon=image_path,
                        name=name + " - " + unichr(int(code, 16)),
                        description=block,
                        on_enter=CopyToClipboardAction(unichr(int(code, 16))),
                    )
                )

        return RenderResultListAction(items)

    def create_icon_image(self, code):
        path = sys.argv[0] + "images/cache/icon_%s.svg" % code
        if os.path.isfile(path):
            return path
        return create_character_icon(code)


def load_icon_template():
    with open(os.path.join(FILE_PATH, "images/unicode.svg"), "r") as i:
        return i.read()


def is_icon_cached(code):
    return os.path.isfile(os.path.join(FILE_PATH, "images/cache/icon_%s.svg" % code))


def create_character_icon(code, font='sans-serif'):
    template = load_icon_template()
    icon = template.replace("{symbol}", unichr(int(code, 16))).replace('{font}', font)
    with codecs.open(
        os.path.join(FILE_PATH, "images/cache/icon_%s.svg" % code), "w", "utf-8"
    ) as target:
        target.write(icon)
    return os.path.join(FILE_PATH, "images/cache/icon_%s.svg" % code)


if __name__ == "__main__":
    UnicodeCharExtension().run()
