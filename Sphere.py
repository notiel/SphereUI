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

        self.white_list = {self.CBW1, self.CBW2, self.CBW3, self.CBW4, self.CBW5, self.CBW6, self.CBW7, self.CBW8,
                           self.CBW9, self.CBW10, self.CBW11, self.CBW12, self.CBW13, self.CBW14, self.CBW15,
                           self.CBW16, self.CBW17, self.CBW18}

        self.mapping = {self.CBG1: 1, self.CBG2: 2, self.CBG3: 3, self.CBG4: 4, self.CBG5: 5,
                        self.CBG6: 6, self.CBG7: 7, self.CBG8: 8, self.CBG9: 9, self.CBG10: 10,
                        self.CBG11: 11, self.CBG12: 12, self.CBG13: 13, self.CBG14: 14, self.CBG15: 15,
                        self.CBG16: 16, self.CBG17: 17, self.CBG18: 18, self.CBG19: 19, self.CBG20: 20,
                        self.CBG21: 21, self.CBG22: 22, self.CBG23: 23, self.CBG24: 24, self.CBG25: 25,
                        self.CBG26: 26, self.CBG27: 27, self.CBG28: 28, self.CBG29: 29, self.CBG30: 30,
                        self.CBG31: 31, self.CBG32: 32, self.CBG33: 33, self.CBG34: 34, self.CBG35: 35,
                        self.CBG36: 36, self.CBB1: 37, self.CBB2: 38, self.CBB3: 39, self.CBB4: 40,
                        self.CBB5: 41, self.CBB6: 42, self.CBB7: 43, self.CBB8: 44, self.CBB9: 45}
        self.white_mapping = {self.CBW1: 46, self.CBW2: 47, self.CBW3: 48, self.CBW4: 49, self.CBW5: 50,
                              self.CBW6: 51, self.CBW7: 52, self.CBW8: 53, self.CBW9: 54, self.CBW10: 55,
                              self.CBW11: 56, self.CBW12: 57, self.CBW13: 58, self.CBW14: 59, self.CBW15: 60,
                              self.CBW16: 61, self.CBW17: 62, self.CBW18: 63}

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
        self.repeat = False
        self.commands = list()
        for i in range(1, 46):
            self.effect[i] = list()
        self.white_effect = dict()
        for i in range(46, 64):
            self.white_effect[i] = list()

        self.CBGreen.clicked.connect(self.check_all)
        self.CBBlue.clicked.connect(self.check_all)
        self.CBAll.clicked.connect(self.check_all)
        self.CBWhite.clicked.connect(self.check_all_white)

        for CB in self.green_list:
            CB.clicked.connect(self.check_led)
        for CB in self.blue_list:
            CB.clicked.connect(self.check_led)
        for CB in self.white_list:
            CB.clicked.connect(self.check_white)

        self.CBTOStart.stateChanged.connect(self.to_start_cb)
        self.CBTOBrightness.stateChanged.connect(self.to_brightness_cb)
        self.CBTOPeriod.stateChanged.connect(self.to_period_cb)
        self.CBSmooth.stateChanged.connect(self.smooth_cb)

        self.BtnCreate.clicked.connect(self.dump)
        self.BtnAdd.clicked.connect(self.dump)
        self.BtnStartRepeat.clicked.connect(self.start_repeat_pressed)
        self.BtnEndRepeat.clicked.connect(self.end_repeat_pressed)
        self.BtnDelete.clicked.connect(self.delete_all)

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

    def check_white(self):
        checked = len([cb for cb in self.white_list if cb.isChecked()])
        if checked == 18:
            self.CBWhite.setCheckState(QtCore.Qt.Checked)
        elif checked == 0:
            self.CBWhite.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.CBWhite.setCheckState(QtCore.Qt.PartiallyChecked)


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

    def check_all_white(self):
        if self.CBWhite.checkState() == QtCore.Qt.Checked or self.CBWhite.checkState() == QtCore.Qt.Unchecked:
            value = True if self.CBWhite.checkState() == QtCore.Qt.Checked else False
            for CB in self.white_list:
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
                self.LstEffects_2.clear()
                if len(self.commands) == 1 and self.commands[0][0] == '0x22':
                    self.LstEffects_2.addItem("Repeat %i" % self.commands[0][1])
                else:
                    self.commands = list()
        self.CBSmooth.setEnabled(True)
        used_keys = [self.mapping[x] for x in self.mapping.keys() if x.isChecked()]
        if not used_keys:
            error_message("Диоды не выбраны")
            return
        if self.tabWidget.currentIndex() == 0:
            self.create_turnon_effect()
        if self.tabWidget.currentIndex() == 1:
            self.create_shine_effect()
        if self.tabWidget.currentIndex() == 2:
            self.create_shift_effect()
        # csv dump
        if self.CBCsv.isChecked():
            self.csv_dump()
        if self.CBH.isChecked():
            self.h_dump()
        self.statusbar.showMessage("Эффект сохранен")
        self.LstEffects_2.addItem(self.get_description())

    def csv_dump(self):
        """
        dump to csv
        :return:
        """
        with open("effect.csv", "w", encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            # get first command data
            command_i = 0
            if self.commands:
                next_command_index = self.commands[0][-1]
            else:
                next_command_index = len(self.effect[1])

            for i in range(min([len(x) for x in self.effect.values()])):
                # write command if necessary
                while i == next_command_index:
                    if self.commands[command_i][0] == '0x23':
                        row = ['0x23']
                    else:
                        row = [self.commands[command_i][0],
                               '0x' + str(self.commands[command_i][1].to_bytes(1, byteorder='big').hex())]
                    writer.writerow(row)
                    if command_i < len(self.commands) - 1:
                        command_i += 1
                        next_command_index = self.commands[command_i][-1]
                    else:
                        next_command_index = len(self.effect[1]) + 1
                row = [self.effect[led][i] for led in self.effect.keys()]
                if self.CBCalibr.isChecked():
                    row = [calibr_list[x] for x in row]
                #row = ['0x' + str(x.to_bytes(1, byteorder='big').hex()) for x in row]
                #new_row = ['0x18']
                #new_row.extend(row)
                writer.writerow(row)
            # add last command if needed
            if next_command_index == len(self.effect[1]) and command_i < len(self.commands):
                 if self.commands[command_i][0] == '0x23':
                    row = ['0x23']
                 else:
                    row = [self.commands[command_i][0],
                           '0x' + str(self.commands[command_i][1].to_bytes(1, byteorder='big').hex())]
                 writer.writerow(row)

    def h_dump(self):
        """
        dump to csv
        :return:
        """
        with open("effect.h", "w", encoding='utf-8') as f:
            dump = 'uint8_t ThePic[] = {\n'
            # get first command data
            command_i = 0
            self.commands.sort(key=lambda x: x[-1])
            if self.commands:
                next_command_index = self.commands[0][-1]
            else:
                next_command_index = len(self.effect[1])
            for i in range(min([len(x) for x in self.effect.values()])):
                # write command if necessary
                while i == next_command_index:
                    dump += self.commands[command_i][0]
                    dump += ','
                    if len(self.commands[command_i]) == 3:
                        dump += '0x' + str(self.commands[command_i][1].to_bytes(1, byteorder='big').hex())
                        dump += ','
                    dump += '\n'
                    if command_i < len(self.commands) - 1:
                        command_i += 1
                        next_command_index = self.commands[command_i][-1]
                    else:
                        next_command_index = len(self.effect[1]) + 1
                row = [self.effect[led][i] for led in self.effect.keys()]
                if self.CBCalibr.isChecked():
                    row = [calibr_list[x] for x in row]
                row = ['0x' + str(x.to_bytes(1, byteorder='big').hex()) for x in row]
                new_row = ['0x18']
                new_row.extend(row)
                dump += ','.join(new_row)
                dump += ',\n'
            if len(self.effect[1]) == next_command_index and command_i < len(self.commands) :
                dump += self.commands[command_i][0]
                dump += ','
                if len(self.commands[command_i]) == 3:
                    dump += '0x' + str(self.commands[command_i][1].to_bytes(1, byteorder='big').hex())
                    dump += ','
                dump += '\n'
            dump = dump[:-2]
            dump += '\n};'
            f.write(dump)

    def create_turnon_effect(self):
        """
        creates effect for turning on/off
        :return:
        """
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
        first_brs = list()
        for led in [self.effect[key] for key in self.effect.keys() if key in used_keys]:
            period = max(period_start + random.randint(0, period_end - period_start), 1)
            brightness = start_br + random.randint(0, end_br - start_br)
            step = ((brightness - start_br) / period) * 10
            first_br = led[-1] if self.CBSmooth.isChecked() else start_br
            first_brs.append(first_br)
            first_step = ((brightness - first_br) / period) * 10
            for i in range(period // 10):
                led.append(round(first_br + i * first_step))
        # longest = max([len(x) for x in self.effect.values()])
        # for led in self.effect.values():
        #     current = len(led)
        #     last = led[-1] if current > 0 else 0
        #     for i in range(longest - current):
        #         led.append(last)
        # if self.repeat and self.CBSmooth.isChecked():
        #     self.commands[-1][-1] = longest
        #     self.repeat = False
        # for led in [self.effect[key] for key in self.effect.keys() if key in used_keys]:
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
            last_step = ((first_br - brightness) / period) * 10
            for i in range(period // 10):
                led.append(max(min(round(brightness + i * last_step), 255), 0))

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
        # first effect iteration
        for k in range(repeat):
            length = len(self.effect[1])
            for line in self.matrix:
                for CB in line:
                    if CB.isChecked():
                        current_i = line.index(CB)
                        current_j = self.matrix.index(line)
                        for t in range(min(tail+1, k+1)):
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
                if not self.CBMovePause.isChecked():
                    for led in self.effect.values():
                        for ms in range(period - 1):
                            led.append(led[-1])
                else:
                    self.commands.append(['0x36', period, len(self.effect[1])])
        # second effect iteration for repeat
        if self.repeat:
            command_repeat = len(self.commands) - 1
            while command_repeat >=0 and self.commands[command_repeat][0] != '0x22':
                command_repeat -= 1
            if command_repeat >= 0:
                self.commands[command_repeat][-1] = len(self.effect[1]) - 1
            self.repeat = False
            for k in range(repeat):
                length = len(self.effect[1])
                for line in self.matrix:
                    for CB in line:
                        if CB.isChecked():
                            current_i = line.index(CB)
                            current_j = self.matrix.index(line)
                            for t in range(tail + 1):
                                br = brightness - t * brightness // (tail + 1)
                                next_i = (current_i + i * (k - t)) % 9
                                next_j = (current_j + j * (k - t)) % 5
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
                    if not self.CBMovePause.isChecked():
                        for led in self.effect.values():
                            for ms in range(period - 1):
                                led.append(led[-1])
                    else:
                         self.commands.append(['0x36', period, len(self.effect[1])])

    def get_description(self) -> str:
        """
        creates effect description
        :return: description
        """
        descr: str = ""
        if self.tabWidget.currentIndex() == 0:
            descr = self.turn_on_descr()
        if self.tabWidget.currentIndex() == 1:
            descr = self.get_shine_descr()
        if self.tabWidget.currentIndex() == 2:
            descr = self.get_shift_descr()
        descr += ' Диоды: %s.' % self.get_selected_leds()
        return descr

    def turn_on_descr(self) -> str:
        """
        creates description for turn onn effect
        :return: description
        """
        descr: str = "Turn on/off: "
        start_end: int = self.SpinToStartTo.value()
        if self.CBTOStart.isChecked():
            descr += 'старт: %i мс, ' % start_end
        else:
            start_start: int = self.SpinTOStartFrom.value()
            descr += 'старт: %i-%i мс, ' % (start_start, start_end)
        br_end: int = self.SpinToBrTo.value()
        if self.CBTOBrightness.isChecked():
            descr += "яркость: %i, " % br_end
        else:
            br_start: int = self.SpinTOBrFrom.value()
            descr += "яркость: %i-%i, " % (br_start, br_end)
        period_end: int = self.SpinTOPeriodTo.value()
        if self.CBTOPeriod.isChecked():
            descr += "за: %i мс." % period_end
        else:
            period_start: int = self.SpinToPeriodFrom.value()
            descr += "за: %i-%i мс." % (period_start, period_end)
        return descr

    def get_shine_descr(self) -> str:
        """
        creates description for shine effect
        :return:
        """
        descr = "Сияние: "
        descr += 'яркость от %i до %i, ' % (self.SpinShineBrFrom.value(), self.SpinShineBrTo.value())
        descr += ' период от %i мс до %i мс, ' % (self.SpinShinePeriodFrom.value(), self.SpinShinePeriodTo.value())
        descr += ' в течение %i с.' % (self.SpinShineLength.value())
        return descr

    def get_shift_descr(self) -> str:
        """
        get description for shift effect
        :return: description
        """
        descr = "Сдвиг "
        descr += self.CBMoveDir.currentText()
        descr += " c яркостью %i " % self.SpinMoveBrightness.value()
        descr += "каждые %i мс, " % self.SpinMovePeriod.value()
        descr += "шлейф: %i диода." % self.SpinMoveTail.value()
        return descr

    def get_selected_leds(self) -> str:
        """
        gets led list str
        :return: str for descr
        """
        if self.CBAll.checkState() == QtCore.Qt.Checked:
            return "Все"
        if self.CBGreen.checkState() == QtCore.Qt.Checked:
            if self.CBBlue.checkState() == QtCore.Qt.Unchecked:
                return "Все зеленые"
            blue_leds = ', '.join([led.text() for led in self.blue_list if led.isChecked()])
            return "Все зеленые, " + blue_leds
        if self.CBBlue.checkState() == QtCore.Qt.Checked:
            if self.CBGreen.checkState() == QtCore.Qt.Unchecked:
                return "Все синие"
            green_leds = ', '.join([led.text() for led in self.green_list if led.isChecked()])
            return "Все синие, " + green_leds
        blue_leds = ', '.join([led.text() for led in self.blue_list if led.isChecked()])
        green_leds = ', '.join([led.text() for led in self.green_list if led.isChecked()])
        if not blue_leds:
            return green_leds
        if not green_leds:
            return blue_leds
        return green_leds + ', ' + blue_leds

    def start_repeat_pressed(self):
        """
        add repeat command
        :return:
        """
        count = self.SpinRepeat.value()
        self.LstEffects_2.addItem("Повтор %i раз" % count)
        self.commands.append(['0x22', count, len(self.effect[1])])
        self.repeat = True

    def end_repeat_pressed(self):
        """
        add repeat command
        :return:
        """
        self.LstEffects_2.addItem("Конец повтора")
        self.commands.append(['0x23', len(self.effect[1])])
        self.repeat = False

    def delete_all(self):
        """
        delete all effects and commands
        :return:
        """
        self.commands = list()
        self.LstEffects_2.clear()
        for k in self.effect.keys():
            self.effect[k] = list()
        self.CBSmooth.setChecked(False)
        self.CBSmooth.setEnabled(False)
        self.BtnAddEffect.setEnabled(False)


def error_message(text):
    """
    shows error window with text
    :param text: error text
    :return:
    """
    error = QtWidgets.QMessageBox()
    error.setIcon(QtWidgets.QMessageBox.Critical)
    error.setText(text)
    error.setWindowTitle('Ошибка!')
    error.setStandardButtons(QtWidgets.QMessageBox.Ok)
    error.exec_()


@logger.catch
def main():
    setup_exception_logging()
    app = QtWidgets.QApplication(sys.argv)
    window = SphereUi()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
