import design_new
from PyQt5 import QtCore, QtWidgets
import sys
import os
from loguru import logger
import random
from typing import List, Dict, Union
from effect_data import *

# import csv

GREEN = 36
BLUE = 9
WHITE = 18


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


class SphereUi(QtWidgets.QMainWindow, design_new.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # list of green led checkboxes
        self.green_list = [self.CBG1, self.CBG2, self.CBG3, self.CBG4, self.CBG5, self.CBG6, self.CBG7, self.CBG8,
                           self.CBG9, self.CBG10,
                           self.CBG11, self.CBG12, self.CBG13, self.CBG14, self.CBG15, self.CBG16, self.CBG17,
                           self.CBG18, self.CBG19, self.CBG20, self.CBG21, self.CBG22, self.CBG23, self.CBG24,
                           self.CBG25, self.CBG26, self.CBG27, self.CBG28, self.CBG29, self.CBG31, self.CBG32,
                           self.CBG33, self.CBG34, self.CBG35, self.CBG36, self.CBG30]

        # list of blue led checkboxes
        self.blue_list = [self.CBB1, self.CBB2, self.CBB3, self.CBB4, self.CBB5, self.CBB6, self.CBB7, self.CBB8,
                          self.CBB9]

        # list of white list checkboxes
        self.white_list = {self.CBW1, self.CBW2, self.CBW3, self.CBW4, self.CBW5, self.CBW6, self.CBW7, self.CBW8,
                           self.CBW9, self.CBW10, self.CBW11, self.CBW12, self.CBW13, self.CBW14, self.CBW15,
                           self.CBW16, self.CBW17, self.CBW18}

        # mapping of checkbox and index of led in effect dict
        self.mapping: Dict[QtWidgets.QCheckBox, int] = {self.CBG1: 1, self.CBG2: 2, self.CBG3: 4, self.CBG4: 5, self.CBG5: 9,
                        self.CBG6: 10, self.CBG7: 11, self.CBG8: 12, self.CBG9: 15, self.CBG10: 16,
                        self.CBG11: 17, self.CBG12: 19, self.CBG13: 22, self.CBG14: 24, self.CBG15: 25,
                        self.CBG16: 26, self.CBG17: 29, self.CBG18: 30, self.CBG19: 32, self.CBG20: 33,
                        self.CBG21: 36, self.CBG22: 37, self.CBG23: 38, self.CBG24: 39, self.CBG25: 43,
                        self.CBG26: 45, self.CBG27: 46, self.CBG28: 47, self.CBG29: 51, self.CBG30: 52,
                        self.CBG31: 53, self.CBG32: 54, self.CBG33: 57, self.CBG34: 58, self.CBG35: 59,
                        self.CBG36: 61, self.CBB1: 3, self.CBB2: 8, self.CBB3: 18, self.CBB4: 23,
                        self.CBB5: 31, self.CBB6: 40, self.CBB7: 44, self.CBB8: 50, self.CBB9: 60,
                        self.CBW1: 6, self.CBW2: 7, self.CBW3: 13, self.CBW4: 14, self.CBW5: 20,
                        self.CBW6: 21, self.CBW7: 27, self.CBW8: 28, self.CBW9: 34, self.CBW10: 35,
                        self.CBW11: 41, self.CBW12: 42, self.CBW13: 48, self.CBW14: 49, self.CBW15: 55,
                        self.CBW16: 56, self.CBW17: 62, self.CBW18: 63}

        # leds in a matrix for shift effect
        self.matrix = [[self.CBG1, self.CBB2, self.CBG9, self.CBG13, self.CBG17, self.CBG21, self.CBG25, self.CBB8,
                        self.CBG33],
                       [self.CBG2, self.CBG5, self.CBG10, self.CBB4, self.CBG18, self.CBG22, self.CBB7, self.CBG29,
                        self.CBG34],
                       [self.CBB1, self.CBG6, self.CBG11, self.CBG14, self.CBB5, self.CBG23, self.CBG26, self.CBG30,
                        self.CBG35],
                       [self.CBG3, self.CBG7, self.CBB3, self.CBG15, self.CBG19, self.CBG24, self.CBG27, self.CBG31,
                        self.CBB9],
                       [self.CBG4, self.CBG8, self.CBG12, self.CBG16, self.CBG20, self.CBB6, self.CBG28, self.CBG32,
                        self.CBG36]]

        self.effect: Dict[int, List[int]] = dict()
        self.repeat: bool = False

        self.groups: List[Group] = list()
        self.effects: List[Effect] = list()

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
        self.BtnStartRepeat.clicked.connect(self.start_repeat_pressed)
        self.BtnEndRepeat.clicked.connect(self.end_repeat_pressed)
        self.BtnPause.clicked.connect(self.pause_pressed)
        self.BtnDelete.clicked.connect(self.delete_all)

    def check_led(self):
        """
        when led is checked it is neseccary to change allleds checkboxes state
        :return:
        """
        led = self.sender()
        checked_green: int = len([cb for cb in self.green_list if cb.isChecked()])
        checked_blue: int = len([cb for cb in self.blue_list if cb.isChecked()])
        if led in self.green_list:
            if checked_green == GREEN:
                self.CBGreen.setCheckState(QtCore.Qt.Checked)
            elif checked_green == 0:
                self.CBGreen.setCheckState(QtCore.Qt.Unchecked)
            else:
                self.CBGreen.setCheckState(QtCore.Qt.PartiallyChecked)
        if led in self.blue_list:
            if checked_blue == BLUE:
                self.CBBlue.setCheckState(QtCore.Qt.Checked)
            elif checked_blue == 0:
                self.CBBlue.setCheckState(QtCore.Qt.Unchecked)
            else:
                self.CBBlue.setCheckState(QtCore.Qt.PartiallyChecked)
        if checked_blue == BLUE and checked_green == GREEN:
            self.CBAll.setCheckState(QtCore.Qt.Checked)
        elif not checked_blue and not checked_green:
            self.CBAll.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.CBAll.setCheckState(QtCore.Qt.PartiallyChecked)

    def check_white(self):
        """
        change allwhiteled checkbox if white checkbox pressed
        :return:
        """
        checked = len([cb for cb in self.white_list if cb.isChecked()])
        if checked == 18:
            self.CBWhite.setCheckState(QtCore.Qt.Checked)
        elif checked == 0:
            self.CBWhite.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.CBWhite.setCheckState(QtCore.Qt.PartiallyChecked)

    def check_all(self):
        """
        if check all blue, check all green ar check oll checkbox is pressed
        :return:
        """
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
        else:
            state = self.CBAll.checkState()
            if state in [QtCore.Qt.Checked, QtCore.Qt.Unchecked]:
                value = True if state == QtCore.Qt.Checked else False
                for CB in self.green_list:
                    CB.setChecked(value)
                for CB in self.blue_list:
                    CB.setChecked(value)
                if not value:
                    self.CBGreen.setCheckState(QtCore.Qt.Unchecked)
                    self.CBBlue.setCheckState(QtCore.Qt.Unchecked)

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
        # if self.CBCsv.isChecked():
        #    self.csv_dump()
        if self.CBH.isChecked():
            self.h_dump()
        self.statusbar.showMessage("Эффект сохранен")
        self.LstEffects_2.addItem(self.get_description())

    # def csv_dump(self):
    #    """
    #    dump to csv
    #    :return:
    #    """
    #    with open("effect.csv", "w", encoding='utf-8', newline='') as csv_file:
    #       writer = csv.writer(csv_file, delimiter=',')
    #       # get first command data
    #       command_i = 0
    #       if self.commands:
    #           next_command_index = self.commands[0][-1]
    #       else:
    #           next_command_index = len(self.effect[1])

    #       for i in range(min([len(x) for x in self.effect.values()])):
    #           # write command if necessary
    #           while i == next_command_index:
    #               if self.commands[command_i][0] == '0x23':
    #                   row = ['0x23']
    #               else:
    #                   row = [self.commands[command_i][0],
    #                          '0x' + str(self.commands[command_i][1].to_bytes(1, byteorder='big').hex())]
    #               writer.writerow(row)
    #               if command_i < len(self.commands) - 1:
    #                   command_i += 1
    #                   next_command_index = self.commands[command_i][-1]
    #               else:
    #                   next_command_index = len(self.effect[1]) + 1
    #           row = [self.effect[led][i] for led in self.effect.keys()]
    #           if self.CBCalibr.isChecked():
    #               row = [calibr_list[x] for x in row]
    #           #row = ['0x' + str(x.to_bytes(1, byteorder='big').hex()) for x in row]
    #           #new_row = ['0x18']
    #           #new_row.extend(row)
    #           writer.writerow(row)
    #       # add last command if needed
    #       if next_command_index == len(self.effect[1]) and command_i < len(self.commands):
    #            if self.commands[command_i][0] == '0x23':
    #               row = ['0x23']
    #            else:
    #               row = [self.commands[command_i][0],
    #                      '0x' + str(self.commands[command_i][1].to_bytes(1, byteorder='big').hex())]
    #            writer.writerow(row)

    def h_dump(self):
        """
        dump to h file
        :return:
        """
        with open("effect.h", "w", encoding='utf-8') as f:
            dump = 'uint8_t ThePic[] = {\n'
            dump += ',\n'.join([effect.h_dump(self.CBCalibr.isChecked()) for effect in self.effects])
            dump += '0xF1'
            dump += '\n};'
            f.write(dump)

    def create_turnon_effect(self):
        """
        creates effect for turning on/off
        :return:
        """
        leds: [Dict[int, List[int]]] = dict()
        for i in range(1, GREEN+BLUE+WHITE+1):
            leds[i] = list()
        used_keys: List[int] = [self.mapping[x] for x in self.mapping.keys() if x.isChecked()]
        start_start: int = self.SpinTOStartFrom.value() if not self.CBTOStart.isChecked() else self.SpinToStartTo.value()
        start_end: int = self.SpinToStartTo.value()
        if not self.CBTOStart.isChecked():
            for led in [leds[key] for key in leds.keys() if key in used_keys]:
                n: int = random.randint(start_start, start_end)
                for i in range(n // 10):
                    led.append(0)
        lowest_br: int = self.SpinToBrTo.value() if self.CBTOBrightness.isChecked() else self.SpinTOBrFrom.value()
        highest_br: int = self.SpinToBrTo.value()
        period_start: int = self.SpinToPeriodFrom.value() if not self.CBTOPeriod.isChecked() else \
            self.SpinTOPeriodTo.value()
        period_end: int = self.SpinTOPeriodTo.value()
        for led in [leds[key] for key in leds.keys() if key in used_keys]:
            start_br: int = led[-1] if self.CBSmooth.isChecked() else 0
            period: int = max(period_start + random.randint(0, period_end - period_start), 1)
            brightness: int = lowest_br + random.randint(0, highest_br - lowest_br) if lowest_br < highest_br else \
                lowest_br - random.randint(0, lowest_br - highest_br)
            step = ((brightness - start_br) / period) * 10
            for i in range(period // 10):
                led.append(round(start_br + i * step))
        longest: int = max([len(x) for x in leds.values()])
        for led in self.effect.values():
            last = led[-1] if (current := len(led)) > 0 else 0
            for i in range(longest - current):
                led.append(last)
        parameters = self.create_param_dict_to(start_start, start_end, lowest_br, highest_br, period_start, period_end)
        effect = Effect(effect=list(), effect_type="TurnOn", parameters=parameters, descr=self.get_description())
        for i in range(longest):
            frame = Frame(brghtnss=[led[i] for led in leds.values()])
            effect.effect.append(frame)
        self.effects.append(effect)

    @staticmethod
    def create_param_dict_to(start_start, start_end, lowest_br, highest_br, period_start, period_end) \
            -> Dict[str, Optional[int]]:
        """
        creates param list for turn on effect
        :param start_start: start of turn on effect start
        :param start_end: end of turn on effect end
        :param lowest_br: lowest brightness of turn on
        :param highest_br:  highest brightness of turn on
        :param period_start: minimal period
        :param period_end: maximum period
        :return: dict of parameters to create description
        """
        parameters = dict()
        parameters['start_start'] = None if start_start == start_end else start_start
        parameters['start_end'] = start_end
        parameters['brightness_start'] = None if highest_br == lowest_br else lowest_br
        parameters['birghtness_end'] = highest_br
        parameters['period_start'] = None if period_start == period_end else period_start
        parameters['period_end'] = period_end
        return parameters

    def create_shine_effect(self):
        """
        create shining effect from second tab
        :return:
        """
        leds: [Dict[int, List[int]]] = dict()
        for i in range(1, GREEN + BLUE + WHITE + 1):
            leds[i] = list()
        used_keys: List [int] = [self.mapping[x] for x in self.mapping.keys() if x.isChecked()]
        start_br: int = self.SpinShineBrFrom.value()
        end_br: int = self.SpinShineBrTo.value()
        period_start: int = self.SpinShinePeriodFrom.value()
        period_end: int = self.SpinShinePeriodTo.value()
        for led in [leds[key] for key in leds.keys() if key in used_keys]:
            period: int = max(period_start + random.randint(0, period_end - period_start), 1)
            brightness: int = start_br + random.randint(0, end_br - start_br)
            step: float = ((brightness - start_br) / period) * 10
            cycles: float = (self.SpinShineLength.value() * 100) / (2 * period // 10)
            for j in range(round(cycles)):
                for i in range(period // 10):
                    led.append(round(start_br + i * step))
                for i in range(period // 10):
                    led.append(round(brightness - i * step))
        longest: int = max([len(x) for x in self.effect.values()])
        for led in self.effect.values():
            last = led[-1] if (current := len(led) > 0) else 0
            for i in range(longest - current):
                led.append(last)
        parameters = self.create_shine_params(start_br, end_br, period_start, period_end, length)
        effect = Effect(effect=list(), effect_type="Shine", parameters=dict(), descr=self.get_description())
        for i in range(longest):
            frame = Frame(brghtnss=[led[i] for led in leds.values()])
            effect.effect.append(frame)
        self.effects.append(effect)

    @staticmethod
    def create_shine_params(self, start_br: int, end_br: int, period_start: int, period_end: int, length: int) \
            -> Dict[str, int]:
        """
        creates parameters dict for shine effect
        :param start_br: lowest lrightness
        :param end_br: highest brightness
        :param period_start:  min period
        :param period_end: max period
        :param length: lenght of effect
        :return: parameters dict
        """

        parameters = dict()
        parameters['start_brightness'] = start_br
        parameters['end_brightness'] = end_br
        parameters['period_start'] = period_start
        parameters['period_end'] = period_end
        parameters['length'] = length
        return parameters

    def create_shift_effect(self):
        """
        creates shift effect
        :return:
        """
        # used_keys = [self.mapping[x] for x in self.mapping.keys() if x.isChecked()]
        # if len([x for x in range(46, 64) if x in used_keys]) > 0:
        #     error_message("Белые диоды не могут участвовать в этом эффекте и будут проигнорированы")
        # brightness = self.SpinMoveBrightness.value()
        direction = self.CBMoveDir.currentIndex()
        # repeat = 5 if direction in (2, 3) else 9
        tail = self.SpinMoveTail.value()
        # first effect iteration
        repeat = 5 if direction in (2, 3) else 9
        if not self.CBMoveForward.isChecked():
            for k in range(repeat):
                self.shift_iteration(k, min(tail + 1, k + 1), False)
        # second effect iteration for repeat
            if self.repeat:
                command_repeat = len(self.commands) - 1
                while command_repeat >= 0 and self.commands[command_repeat][0] != '0x22':
                    command_repeat -= 1
                if command_repeat >= 0:
                    self.commands[command_repeat][-1] = len(self.effect[1])
                self.repeat = False
                for k in range(repeat):
                    self.shift_iteration(k, tail + 1, False)
        else:
            for k in range(repeat):
                self.shift_iteration(k, tail+1, True)

    def shift_iteration_bugged(self, k, tail_range, forward):
        """
        one iteration for shift effect
        :return:
        """
        brightness = self.SpinMoveBrightness.value()
        direction = self.CBMoveDir.currentIndex()
        tail = self.SpinMoveTail.value()
        length = len(self.effect[1])
        period = self.SpinMovePeriod.value() // 10
        if direction == 0:
            i, j = -1, 0
        elif direction == 1:
            i, j = 1, 0
        elif direction == 2:
            i, j = 0, -1
        else:
            i, j = 0, 1
        for line in self.matrix:
            for CB in line:
                if CB.isChecked():
                    current_i = line.index(CB)
                    current_j = self.matrix.index(line)
                    for t in range(tail_range):
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
                        if forward:
                            next_i = (current_i - i * (k - t)) % 9
                            next_j = (current_j - j * (k - t)) % 5
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

    def shift_iteration(self, k, tail_range, forward):
        """
        one iteration for shift effect
        :return:
        """
        brightness = self.SpinMoveBrightness.value()
        direction = self.CBMoveDir.currentIndex()
        tail = self.SpinMoveTail.value()
        length = len(self.effect[1])
        period = self.SpinMovePeriod.value() // 10
        if direction == 0:
            i, j = -1, 0
        elif direction == 1:
            i, j = 1, 0
        elif direction == 2:
            i, j = 0, -1
        else:
            i, j = 0, 1
        for line in self.matrix:
            for CB in line:
                if CB.isChecked():
                    current_i = line.index(CB)
                    current_j = self.matrix.index(line)
                    for t in range(tail_range):
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
                        if forward:
                            next_i = (current_i + i * (k + t)) % 9
                            next_j = (current_j + j * (k + t)) % 5
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
        if self.CBMoveForward.isChecked():
            descr += 'Хвост вперед включен'
        return descr

    def get_selected_leds(self) -> str:
        """
        gets led list str
        :return: str for descr
        """
        # if self.CBAll.checkState() == QtCore.Qt.Checked:
        #     if self.CBWhite.checkState() == QtCore.Qt.Checked:
        #         return "Все"
        #     elif self.CBWhite.checkState() == QtCore.Qt.Unchecked:
        #         return "Все зеленые и синие"
        #     elif
        # if self.CBGreen.checkState() == QtCore.Qt.Checked:
        #     if self.CBBlue.checkState() == QtCore.Qt.Unchecked:
        #         return "Все зеленые"
        #     blue_leds = ', '.join([led.text() for led in self.blue_list if led.isChecked()])
        #     return "Все зеленые, " + blue_leds
        # if self.CBBlue.checkState() == QtCore.Qt.Checked:
        #     if self.CBGreen.checkState() == QtCore.Qt.Unchecked:
        #         return "Все синие"
        #     green_leds = ', '.join([led.text() for led in self.green_list if led.isChecked()])
        #     return "Все синие, " + green_leds
        # blue_leds = ', '.join([led.text() for led in self.blue_list if led.isChecked()])
        # green_leds = ', '.join([led.text() for led in self.green_list if led.isChecked()])
        # if not blue_leds:
        #     return green_leds
        # if not green_leds:
        #     return blue_leds
        # return green_leds + ', ' + blue_leds
        res = ""
        green_leds = [led.text() for led in self.green_list if led.isChecked()]
        blue_leds = [led.text() for led in self.blue_list if led.isChecked()]
        white_leds = [led.text() for led in self.white_list if led.isChecked()]
        if len(green_leds) == 36 and len(blue_leds) == 9 and len(white_leds) == 18:
            return "все"
        if len(green_leds) == 36:
            res += "все зеленые, "
        if len(blue_leds) == 9:
            res += "все синие, "
        if len(white_leds) == 18 and self.tabWidget.currentIndex() != 2:
            res += "все белые, "
        if 0 < len(green_leds) < 36:
            res += "зеленые: "
            res += ', '.join(green_leds)
            res += ', '
        if 0 < len(blue_leds) < 9:
            res += 'синие: '
            res += ', '.join(blue_leds)
            res += ', '
        if 0 < len(white_leds) < 18 and self.tabWidget.currentIndex() != 2:
            res += 'белые'
            res += ', '.join(white_leds)
            res += ', '
        return res[:-2]

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
        self.dump()

    def pause_pressed(self):
        """
        button to add pause
        :return:
        """
        pause = self.SpinPause.value()
        self.commands.append(['0x36', pause, len(self.effect[1])])

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
    print(calibr_list[130])
    setup_exception_logging()
    app = QtWidgets.QApplication(sys.argv)
    window = SphereUi()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
