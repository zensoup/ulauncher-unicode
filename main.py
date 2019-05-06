import sys
sys.path.append('/home/zen/.local/lib/python2.7/site-packages/')

import os
from fuzzywuzzy import process

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def __init__(self):
        f = open(os.path.dirname(sys.argv[0]) + '/unicode_list.txt', 'r')
        data = f.readlines()
        self.data = {}
        # self.names = []
        self.items = []
        # self.blocks = []
        for item in data:
            item = item.strip()
            name, code, block = item.split('\t')
            self.data[name + ' ' + block] = (name, block, code)
            self.items.append(name + ' ' + block)
            # self.names.append(name)
            # self.blocks.append(block)

    def on_event(self, event, extension):
        items = []
        arg = event.get_argument()
        if arg:
            matches = process.extract(arg, self.items, limit=15)
            for m in matches:
                name, block, code = self.data[m[0]]
                items.append(ExtensionResultItem(icon='images/bookmark.svg',
                                                 name=name + ' - ' + unichr(int(code, 16)),
                                                 description=block,
                                                 on_enter=CopyToClipboardAction(unichr(int(code, 16)))))

        return RenderResultListAction(items)

if __name__ == '__main__':
    DemoExtension().run()
