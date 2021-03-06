import json
import sys
import threading

import time
from PyQt4 import QtGui, QtCore

from form import Ui_Dialog

from Controller.ObjectTracker import Tracker
from Controller.client import Client


class MainMenu(QtGui.QMainWindow):
    RUN = 'run'
    STOP = 'stop'
    MANUAL = 'manual'

    def __init__(self, host='raspberrypi', port=1234, url=None):
        super(MainMenu, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton_3.clicked.connect(self.start_tracking)
        self.ui.pushButton_4.clicked.connect(self.stop_tracking)
        self.ui.pushButton_5.clicked.connect(self.robot_initializer)
        self.ui.pushButton_6.clicked.connect(self.show_tracker)
        self.ui.pushButton.clicked.connect(self.closeAll)

        self.show()
        self.client = Client(host=host, port=port)

        self.object_tracker = Tracker(video_url=url, buffer_size=64)
        self.status = self.STOP

    def keyPressEvent(self, event1):
        self.status = self.MANUAL
        self.ui.label_2.setText(self.status)

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

        json_data = json.dumps(verbose)
        if verbose["LR"] != "" or verbose["FB"] != "":
            print(verbose)
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

        json_data = json.dumps(verbose)
        if verbose["LR"] != "" or verbose["FB"] != "":
            print(verbose)
            self.client.send(json_data)
            self.client.send(json_data)

    def start_tracking(self):
        self.status = self.RUN
        if self.object_tracker.is_working:
            print('start tracking')
            verbose = {
                "status": self.RUN
            }
            json_data = json.dumps(verbose)
            self.client.send(json_data)

            self.ui.label_2.setText(self.status)
            data_sender_thread = threading.Thread(target=self.data_sender)
            data_sender_thread.start()

    def stop_tracking(self):
        self.status = self.STOP
        verbose = {
            "status": self.STOP
        }
        json_data = json.dumps(verbose)
        self.client.send(json_data)
        self.ui.label_2.setText(self.status)

    def closeAll(self):

        self.status = self.STOP
        verbose = {
            "status": self.STOP
        }
        json_data = json.dumps(verbose)
        self.client.send(json_data)
        QtCore.QCoreApplication.instance().quit()

    def show_tracker(self):
        if not self.object_tracker.is_working:
            tracking_thread = threading.Thread(target=self.object_tracker.track)
            tracking_thread.start()

    def robot_initializer(self):

        try:
            x_min = round(float(self.ui.lineEdit_5.text()), 2)
        except:
            x_min = 200

        try:
            x_max = round(float(self.ui.lineEdit_2.text()), 2)
        except:
            x_max = 300
        try:
            minArea = round(float(self.ui.lineEdit_3.text()), 2)
        except:
            minArea = 20
        try:
            maxArea = round(float(self.ui.lineEdit_4.text()), 2)
        except:
            maxArea = 100

        verbose = {
            "x_min": x_min,
            "x_max": x_max,
            "maxArea": maxArea,
            "minArea": minArea,
        }
        json_data = json.dumps(verbose)
        print(json_data)
        self.client.send(json_data)

    def data_sender(self):
        verbose = {"radius": "", "x": ""}
        while self.object_tracker.is_working and self.status != self.STOP:
            if len(self.object_tracker.positions) > 0:
                currentPosition = self.object_tracker.positions[0]
                if currentPosition[0] is not None:
                    print(currentPosition)
                    verbose["radius"] = currentPosition[1]
                    verbose["x"] = currentPosition[0][1]
                    json_data = json.dumps(verbose)
                    self.client.send(json_data)
            time.sleep(0.5)
        self.status = self.STOP
        self.ui.label_2.setText(self.status)


def main(ip, port, url):
    app = QtGui.QApplication(sys.argv)
    ex = MainMenu(host=ip, port=port, url=url)
    app.exec_()


if __name__ == '__main__':
    # videoURL = 0
    # videoURL = "./testData/ball_tracking_example.mp4"
    videoURL = "http://raspberrypi:8080/stream/video.mjpeg"
    IP = "raspberrypi"
    PORT = 1234
    main(IP, PORT, videoURL)
