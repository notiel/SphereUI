import design
import PyQt5
from PyQt5 import  QtCore, QtWidgets
import sys
import os
import csv
from loguru import logger
import random


def setup_exception_logging():
    # generating our hook
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        logger.exception(f"{exctype}, {value}, {traceback}")
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        # sys.exit(1)

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


class SphereUi(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.green_list = [self.CBG1, self.CBG2, self.CBG3, self.CBG4, self.CBG5, self.CBG6, self.CBG7, self.CBG8,
                           self.CBG9, self.CBG10,
                           self.CBG11, self.CBG12, self.CBG13, self.CBG14, self.CBG15, self.CBG16, self.CBG17,
                           self.CBG18, self.CBG19, self.CBG20, self.CBG21, self.CBG22, self.CBG23, self.CBG24,
                           self.CBG25, self.CBG26, self.CBG27, self.CBG28, self.CBG29, self.CBG31, self.CBG32,
                           self.CBG33, self.CBG34, self.CBG35, self.CBG36, self.CBG30]

        self.blue_list = [self.CBB1, self.CBB2, self.CBB3, self.CBB4, self.CBB5, self.CBB6, self.CBB7, self.CBB8,
                          self.CBB9]
        self.effect = dict()
        for i in range(1, 46):
            self.effect[i] = list()

        self.CBGreen.clicked.connect(self.check_all)
        self.CBBlue.clicked.connect(self.check_all)
        self.CBAll.clicked.connect(self.check_all)
        for CB in self.green_list:
            CB.clicked.connect(self.check_led)
        for CB in self.blue_list:
            CB.clicked.connect(self.check_led)

        self.CBTOStart.stateChanged.connect(self.to_start_cb)
        self.CBTOBrightness.stateChanged.connect(self.to_brightness_cb)
        self.CBTOPeriod.stateChanged.connect(self.to_period_cb)

        self.BtnCreate.clicked.connect(self.dump)

    def check_led(self):
        led = self.sender()
        if led in self.green_list:
            checked = len([cb for cb in self.green_list if cb.isChecked()])
            if checked == 36:
                self.CBGreen.setCheckState(QtCore.Qt.Checked)
            elif checked == 0:
                self.CBGreen.setCheckState(QtCore.Qt.Unchecked)
            else:
                self.CBGreen.setCheckState(QtCore.Qt.PartiallyChecked)
        if led in self.blue_list:
            checked = len([cb for cb in self.blue_list if cb.isChecked()])
            if checked == 9:
                self.CBBlue.setCheckState(QtCore.Qt.Checked)
            elif checked == 0:
                self.CBBlue.setCheckState(QtCore.Qt.Unchecked)
            else:
                self.CBBlue.setCheckState(QtCore.Qt.PartiallyChecked)

    def check_all(self):
        sender = self.sender()
        if sender == self.CBGreen or sender == self.CBBlue:
            if self.CBGreen.checkState() == QtCore.Qt.Checked and self.CBBlue.checkState() == QtCore.Qt.Checked:
                self.CBAll.setCheckState(QtCore.Qt.Checked)
            elif self.CBGreen.checkState() == QtCore.Qt.Unchecked and self.CBBlue.checkState() == QtCore.Qt.Unchecked:
                self.CBAll.setCheckState(QtCore.Qt.Unchecked)
            else:
                self.CBAll.setCheckState(QtCore.Qt.PartiallyChecked)
            if self.CBGreen.checkState() == QtCore.Qt.Checked or self.CBGreen.checkState() == QtCore.Qt.Unchecked:
                value = True if self.CBGreen.checkState() else False
                for CB in self.green_list:
                    CB.setChecked(value)
            if self.CBBlue.checkState() == QtCore.Qt.Checked or self.CBBlue.checkState() == QtCore.Qt.Unchecked:
                value = True if self.CBBlue.checkState() else False
                for CB in self.blue_list:
                    CB.setChecked(value)

        if self.CBAll.checkState() == QtCore.Qt.Checked or self.CBAll.checkState() == QtCore.Qt.Unchecked:
            value = True if self.CBAll.checkState() == QtCore.Qt.Checked else False
            for CB in self.green_list:
                CB.setChecked(value)
            for CB in self.blue_list:
                CB.setChecked(value)
            self.CBGreen.setCheckState(self.CBAll.checkState())
            self.CBBlue.setCheckState(self.CBAll.checkState())

    def to_start_cb(self):
        value = self.CBTOStart.isChecked()
        self.SpinToStartTo.setEnabled(not value)
        self.SpinTOStartFrom.setEnabled(not value)

    def to_brightness_cb(self):
        value = self.CBTOBrightness.isChecked()
        self.SpinTOBrFrom.setEnabled(not value)

    def to_period_cb(self):
        value = self.CBTOPeriod.isChecked()
        self.SpinToPeriodFrom.setEnabled(not value)

    def dump(self):
        """
        dumps effect to csv file
        :return:
        """
        if self.tabWidget.currentIndex() == 0:
            if not self.CBTOStart.isChecked():
                for led in self.effect.values():
                    n = random.randint(self.SpinTOStartFrom.value(), self.SpinToStartTo)
                    for i in range(n):
                        led.append(0)
            start_br = self.SpinTOStartFrom.value() if not self.CBTOBrightness.isChecked() else self.SpinToBrTo.value()
            end_br = self.SpinToBrTo.value()
            period_start = self.SpinToPeriodFrom.value() if not self.CBTOPeriod.isChecked() else \
                self.SpinTOPeriodTo.value()
            period_end = self.SpinTOPeriodTo.value()
            for led in self.effect.values():
                period = max(period_start + random.randint(0, period_end - period_start), 1)
                brightness = start_br + random.randint(0, end_br - start_br)
                step = (brightness / period) * 10
                for i in range (period // 10):
                    led.append(round(i*step))
                if len(led) > 0:
                    led[-1] = brightness
                else:
                    led.append(brightness)
            longest = max([len(x) for x in self.effect.values()])
            for led in self.effect.values():
                current = len(led)
                last = led[-1] if current > 0 else 0
                for i in range(longest - current):
                    led.append(last)
        with open("effect.csv", "w", encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for i in range(min([len(x) for x in self.effect.values()])):
                writer.writerow([self.effect[led][i] for led in self.effect.keys()])
            self.statusbar.showMessage("Эффект сохранен")


@logger.catch
def main():
    setup_exception_logging()
    app = QtWidgets.QApplication(sys.argv)
    window = SphereUi()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
