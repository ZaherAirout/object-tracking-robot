import sys
import threading

from PyQt4 import QtGui, QtCore
import time, socket, json

from form import Ui_MainWindow

from Controller.ObjectTracker import Tracker
from Controller.client import Client


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
    # main()
    videoURL = "./testData/ball_tracking_example.mp4"
    objectTracker = Tracker(video_url=videoURL)
    movement_thread = threading.Thread(target=objectTracker.track)
    movement_thread.start()
    if True:
        for i in range(10):
            print(objectTracker.position)
            print(objectTracker.center)

            time.sleep(1)
