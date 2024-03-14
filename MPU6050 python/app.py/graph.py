import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import serial.tools.list_ports
from PyQt5.QtCore import QTimer
import serial

x = []
y = []
z = []
y1 = []
y2 = []
y3 = []
i = 0


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deprem İkaz Grafiği")
        self.setGeometry(150, 150, 800, 175)
        self.UI()

    def UI(self):
        self.setStyleSheet("background-color:white;font-size:12pt;font-family:Times;")
        mainLayout = QHBoxLayout()
        leftFormLayout = QFormLayout()
        rightLayout = QVBoxLayout()
        mainLayout.addLayout(leftFormLayout, 30)
        mainLayout.addLayout(rightLayout, 70)


        self.accx = QLabel("Acceloremeter X :")
        self.accx_value = QLabel("...")
        self.accx.setStyleSheet("color:red;")
        self.accx_value.setStyleSheet("color:red;")
        self.accy = QLabel("Acceloremeter Y :")
        self.accy_value = QLabel("...")
        self.accy.setStyleSheet("color:green;")
        self.accy_value.setStyleSheet("color:green;")
        self.accz = QLabel("Acceloremeter Z :")
        self.accz_value = QLabel("...")
        self.accz.setStyleSheet("color:blue;")
        self.accz_value.setStyleSheet("color:blue;")
        self.btn_connect = QPushButton("Enter", self)
        self.btn_connect.clicked.connect(self.connect_system)
        self.btn_exit = QPushButton("Exit", self)
        self.btn_exit.clicked.connect(self.exit)
        self.btn_start_graph = QPushButton("Start Graph", self)
        self.btn_start_graph.clicked.connect(self.start_graph)
        leftFormLayout.addRow(self.btn_connect, self.btn_exit)
        leftFormLayout.addRow(self.accx, self.accx_value)
        leftFormLayout.addRow(self.accy, self.accy_value)
        leftFormLayout.addRow(self.accz, self.accz_value)
        rightLayout.addWidget(self.btn_start_graph)
        
        self.graphWidget1 = pg.PlotWidget()
        self.graphWidget2 = pg.PlotWidget()
        self.graphWidget3 = pg.PlotWidget()
        rightLayout.addWidget(self.graphWidget1)
        rightLayout.addWidget(self.graphWidget2)
        rightLayout.addWidget(self.graphWidget3)

        self.setLayout(mainLayout)

        self.timer = QTimer()
        self.timer.setInterval(195)
        self.timer.timeout.connect(self.start_graph)
        self.show()


    def exit(self):
        self.timer.stop()
        sys.exit()

    def connect_system(self):
        global ser
        print("Connecting System")
        ser = serial.Serial(self.port.currentText(), 115200)
        print(str(self.port) + " Connecting Port")
        self.timer.start()

    def start_graph(self):
        global ser, i, x, y, z, y1, y2, y3
        line = str(ser.readline())
        print(line)
        data = line.split(",")
        self.accx_value.setText(str(data[1]))
        self.accy_value.setText(str(data[2]))
        self.accz_value.setText(str(data[3]))

        x.append(i)
        y.append(i)
        z.append(i)
        y1.append(float(data[1]))  # x ekseni için veri
        y2.append(float(data[2]))  # y ekseni için veri
        y3.append(float(data[3]))  # z ekseni için veri
        i = i + 1

        pen = pg.mkPen(color=(255, 0, 0), width=1)
        pen2 = pg.mkPen(color=(0, 255, 0), width=1)
        pen3 = pg.mkPen(color=(0, 0, 255), width=1)

        self.graphWidget1.clear()
        self.graphWidget2.clear()
        self.graphWidget3.clear()

        self.graphWidget1.plot(x, y1, name="X Axis Data", pen=pen)
        self.graphWidget2.plot(y, y2, name="Y Axis Data", pen=pen2)
        self.graphWidget3.plot(z, y3, name="Z Axis Data", pen=pen3)


def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()