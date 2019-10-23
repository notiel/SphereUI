import design
import PyQt5
from PyQt5 import QtCore, QtWidgets
import sys
import os
import csv
from loguru import logger
import random

calibr_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
               1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2,
               2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5,
               5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10,
               10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
               17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
               25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
               37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
               51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
               69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
               90, 92, 93, 95, 96, 98, 99, 101, 102, 104, 105, 107, 109, 110, 112, 114,
               115, 117, 119, 120, 122, 124, 126, 127, 129, 131, 133, 135, 137, 138, 140, 142,
               144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 167, 169, 171, 173, 175,
               177, 180, 182, 184, 186, 189, 191, 193, 196, 198, 200, 203, 205, 208, 210, 213,
               215, 218, 220, 223, 225, 228, 231, 233, 236, 239, 241, 244, 247, 249, 252, 255]


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

        self.mapping = {self.CBG1: 1, self.CBG2: 2, self.CBG3: 3, self.CBG4: 4, self.CBG5: 5,
                        self.CBG6: 6, self.CBG7: 7, self.CBG8: 8, self.CBG9: 9, self.CBG10: 10,
                        self.CBG11: 11, self.CBG12: 12, self.CBG13: 13, self.CBG14: 14, self.CBG15: 15,
                        self.CBG16: 16, self.CBG17: 17, self.CBG18: 18, self.CBG19: 19, self.CBG20: 20,
                        self.CBG21: 21, self.CBG22: 22, self.CBG23: 23, self.CBG24: 24, self.CBG25: 25,
                        self.CBG26: 26, self.CBG27: 27, self.CBG28: 28, self.CBG29: 29, self.CBG30: 30,
                        self.CBG31: 31, self.CBG32: 32, self.CBG33: 33, self.CBG34: 34, self.CBG35: 35,
                        self.CBG36: 36, self.CBB1: 37, self.CBB2: 38, self.CBB3: 39, self.CBB4: 40,
                        self.CBB5: 41, self.CBB6: 42, self.CBB7: 43, self.CBB8: 44, self.CBB9: 45}

        self.matrix = [[self.CBG1, self.CBB2, self.CBG9, self.CBG13, self.CBG17, self.CBG21, self.CBG25, self.CBB8,
                        self.CBG33],
                       [self.CBG2, self.CBG5, self.CBG10, self.CBB4, self.CBG18, self.CBG22, self.CBB7, self.CBG29,
                        self.CBG34],
                       [self.CBB1, self.CBG6, self.CBG11, self.CBG14, self.CBB5, self.CBG23, self.CBG26, self.CBG30,
                        self.CBG35],
                       [self.CBG3, self.CBG7, self.CBB3, self.CBG15, self.CBG19, self.CBG24, self.CBG27, self.CBG31,
                        self.CBB9],
                       [self.CBG4, self.CBG8, self.CBG12,  self.CBG16, self.CBG20, self.CBB6, self.CBG28, self.CBG32,
                        self.CBG36]]

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
        self.CBSmooth.stateChanged.connect(self.smooth_cb)

        self.BtnCreate.clicked.connect(self.dump)
        self.BtnAdd.clicked.connect(self.dump)

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

    def smooth_cb(self):
        value = self.CBSmooth.isChecked()
        self.BtnCreate.setEnabled(not value)

    def dump(self):
        """
        dumps effect to csv file
        :return:
        """
        sender = self.sender()
        if sender == self.BtnCreate:
            for i in range(1, 46):
                self.effect[i] = list()
        self.CBSmooth.setEnabled(True)
        if self.tabWidget.currentIndex() == 0:
            self.create_turnon_effect()
        if self.tabWidget.currentIndex() == 1:
            self.create_shine_effect()
        if self.tabWidget.currentIndex() == 2:
            self.create_shift_effect()
        with open("effect.csv", "w", encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for i in range(min([len(x) for x in self.effect.values()])):
                if self.CBCalibr.isChecked():
                    pass
                else:
                    writer.writerow([self.effect[led][i] for led in self.effect.keys()])
            self.statusbar.showMessage("Эффект сохранен")

    def create_turnon_effect(self):
        used_keys = [self.mapping[x] for x in self.mapping.keys() if x.isChecked()]
        if not self.CBTOStart.isChecked():
            for led in [self.effect[key] for key in self.effect.keys() if key in used_keys]:
                n = random.randint(self.SpinTOStartFrom.value(), self.SpinToStartTo.value())
                for i in range(n // 10):
                    led.append(0)
        lowest_br = self.SpinToBrTo.value() if self.CBTOBrightness.isChecked() else self.SpinTOBrFrom.value()
        highest_br = self.SpinToBrTo.value()
        period_start = self.SpinToPeriodFrom.value() if not self.CBTOPeriod.isChecked() else \
            self.SpinTOPeriodTo.value()
        period_end = self.SpinTOPeriodTo.value()
        for led in [self.effect[key] for key in self.effect.keys() if key in used_keys]:
            start_br = led[-1] if self.CBSmooth.isChecked() else 0
            period = max(period_start + random.randint(0, period_end - period_start), 1)
            brightness = lowest_br + random.randint(0, highest_br - lowest_br) if lowest_br < highest_br else \
                lowest_br - random.randint(0, lowest_br - highest_br)
            step = ((brightness - start_br)/period) * 10
            for i in range(period // 10):
                led.append(round(start_br + i * step))
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

    def create_shine_effect(self):
        """
        create shining effect from second tab
        :return:
        """
        used_keys = [self.mapping[x] for x in self.mapping.keys() if x.isChecked()]
        start_br = self.SpinShineBrFrom.value()
        end_br = self.SpinShineBrTo.value()
        period_start = self.SpinShinePeriodFrom.value()
        period_end = self.SpinShinePeriodTo.value()
        for led in [self.effect[key] for key in self.effect.keys() if key in used_keys]:
            period = max(period_start + random.randint(0, period_end - period_start), 1)
            brightness = start_br + random.randint(0, end_br - start_br)
            step = ((brightness - start_br) / period) * 10
            first_br = led[-1] if self.CBSmooth.isChecked() else start_br
            first_step = ((brightness - first_br) / period) * 10
            for i in range(period // 10):
                led.append(round(first_br + i * first_step))
            cycles = (self.SpinShineLength.value()*100 - period // 10) / (2*period // 10)
            for j in range(round(cycles)):
                for i in range(period // 10):
                    led.append(round(brightness - i * step))
                if len(led) > 0:
                    led[-1] = start_br
                else:
                    led.append(start_br)
                for i in range(period // 10):
                    led.append(round(start_br + i * step))
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

    def create_shift_effect(self):
        """
        creates shift effect
        :return:
        """
        brightness = self.SpinMoveBrightness.value()
        # for led in [self.effect[key] for key in self.effect.keys() if key in used_keys]:
        #    led.append(brightness)
        direction = self.CBMoveDir.currentIndex()
        repeat = 5 if direction in (2, 3) else 9
        tail = self.SpinMoveTail.value()
        if direction == 0:
            i, j = -1, 0
        elif direction == 1:
            i, j = 1, 0
        elif direction == 2:
            i, j = 0, -1
        else:
            i, j = 0, 1
        period = self.SpinMovePeriod.value() // 10
        for k in range(repeat):
            length = len(self.effect[1])
            for line in self.matrix:
                for CB in line:
                    if CB.isChecked():
                        current_i = line.index(CB)
                        current_j = self.matrix.index(line)
                        for t in range(tail+1):
                            br = brightness - t*brightness//(tail+1)
                            next_i = (current_i + i*(k-t)) % 9
                            next_j = (current_j + j*(k-t)) % 5
                            next_cb = self.matrix[next_j][next_i]
                            led = (self.effect[self.mapping[next_cb]])
                            if len(led) == length:
                               led.append(br)
                            else:
                                current = led[-1]
                                if current < br:
                                    led[-1] = br
            longest = max([len(x) for x in self.effect.values()])
            for led in self.effect.values():
                if len(led) < longest:
                    led.append(0)
            if period > 1:
                for led in self.effect.values():
                    for ms in range(period - 1):
                        led.append(led[-1])

@logger.catch
def main():
    setup_exception_logging()
    app = QtWidgets.QApplication(sys.argv)
    window = SphereUi()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
