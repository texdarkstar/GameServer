import xmltodict


class XMLParser(object):
    def parse(self, text):
        text = xmltodict.parse(text)
        return text
