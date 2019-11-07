import socket

class gnuRadio(object):
    def __init__(self):
        self.text = ""

    def writeTxt(self, text):
        f = open(str("gnuText") + str('.txt'), 'w')
        f.write(text)
        f.close()
        self.text = text

    