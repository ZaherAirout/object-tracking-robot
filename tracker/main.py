import sys
from PyQt4 import QtGui, QtCore
import time, socket, json

from form import Ui_MainWindow

from tracker.client import Client


class main_menu(QtGui.QMainWindow):

    def __init__(self, host='raspberrypi', port=1234):
        super(main_menu, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.client = Client(host=host, port=port)

    def keyPressEvent(self, event1):
        verbose = {"FB": "", "LR": ""}
        if event1.key() == QtCore.Qt.Key_W:
            # print "Up pressed"
            verbose["FB"] = "F"
        if event1.key() == QtCore.Qt.Key_S:
            # print "D pressed"
            verbose["FB"] = "B"

        if event1.key() == QtCore.Qt.Key_A:
            # print "L pressed"
            verbose["LR"] = "L"
        if event1.key() == QtCore.Qt.Key_D:
            # print "R pressed"
            verbose["LR"] = "R"

        print(verbose)
        json_data = json.dumps(verbose)
        self.client.send(json_data)

    def keyReleaseEvent(self, event):
        verbose = {"FB": "", "LR": ""}
        if event.key() == QtCore.Qt.Key_W:
            # print "Up rel"
            verbose["FB"] = "S"
        if event.key() == QtCore.Qt.Key_S:
            # print "D rel"
            verbose["FB"] = "S"

        if event.key() == QtCore.Qt.Key_A:
            # print "L pressed"
            verbose["LR"] = "S"
        if event.key() == QtCore.Qt.Key_D:
            # print "R pressed"
            verbose["LR"] = "S"

        print(verbose)
        json_data = json.dumps(verbose)
        self.client.send(json_data)


def main():
    app = QtGui.QApplication(sys.argv)

    IP = "raspberrypi"
    PORT = 1234
    ex = main_menu(host=IP, port=1234)
    app.exec_()


if __name__ == '__main__':
    main()
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # IP = "192.168.1.18"
    # PORT = 1234
    # s.sendto("HELP ME".encode(), (IP, PORT))
