from dataclasses import dataclass
from typing import List, Optional, Union, Dict
import random

GREEN = 36
BLUE = 9
WHITE = 18

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

command_codes = {'Repeat': '0x22', 'EndOfRepeat': '0x23', 'Pause': '0x36'}

dir_dict = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}

index_mapping = [[1, 8, 15, 22, 29, 36, 43, 50, 57],
                 [2, 9, 16, 23, 30, 37, 44, 51, 58],
                 [3, 10, 17, 24, 31, 38, 45, 52, 59],
                 [4, 11, 18, 25, 32, 39, 46, 53, 60],
                 [5, 12, 19, 26, 33, 40, 47, 54, 61]]


@dataclass
class Group:
    name: str
    leds: List[int]
    effects: List[str]


@dataclass
class Frame:
    brghtnss: List[int]

    def h_dump(self, calibrated=True) -> str:
        """
        dumps frame as list of hex integers (with command 0x18 at the beginning of dump)
        :param calibrated: take calibrated brightness instead of real
        :return:
        """
        row: List[str] = ['0x' + str(x.to_bytes(1, byteorder='big').hex()) for x in self.brghtnss] if not calibrated \
            else ['0x' + str(calibr_list[x].to_bytes(1, byteorder='big').hex()) for x in self.brghtnss]
        dumpdata: str = ','.join(row)
        return '0x18,' + dumpdata


@dataclass
class Command:
    command: str
    parameter: Optional[int]

    def h_dump(self, calibrated=True) -> str:
        """
        dumps command data as code and parameters as hex number
        :return:
        """
        dumpdata: str = command_codes[self.command]
        if self.parameter:
            dumpdata += ',0x' + str(self.parameter.to_bytes(1, byteorder='big').hex())
        return dumpdata


@dataclass
class Effect:
    effect: List[Union[Frame, Command]]
    effect_type: str
    parameters: Dict[str, Optional[int]]

    def h_dump(self, calibrated: bool) -> str:
        """
        dumps all commands and frames
        :return:
        """
        return ',\n'.join([x.h_dump(calibrated) for x in self.effect])


def smooth(first: Effect, second: Effect, period: int) -> Effect:
    """
    create Smooth path from first to second effects for period ms as a number of frames and dump it
    :param first: first effect
    :param second: second effect
    :param period: time of smoothing
    :return: effect for smoothing effect1 and effect2
    """
    smoothing: List[Frame] = list()
    i: int = -1
    while isinstance(last_frame := first.effect[i], Command):
        i -= 1
    i = 0
    while isinstance(first_frame := second.effect[i], Command):
        i += 1
    for j in range(period // 10):
        frame: Frame = Frame(brghtnss=list())
        for i in range(len(last_frame.brghtnss)):
            start_br = last_frame.brghtnss[i]
            end_br = first_frame.brghtnss[i]
            step = ((end_br - start_br) / period) * 10
            frame.brghtnss.append(round(start_br + i * step))
        smoothing.append(frame)
    smooth_effect = Effect(effect=smoothing, effect_type="Smooth", parameters=dict())
    return smooth_effect


def smooth_all(effects: List[Effect], period: int):
    """
    smooth all effects
    :param period: period for smoothing
    :param effects:
    :return: smoothed effects
    """
    new_effects = list()
    i = 0
    while i < len(effects):
        while isinstance(effects[i], Command) and i < len(effects):
            i += 1
        new_effects.append(effects[i])
        j = i + 1
        while isinstance(effects[j], Command) and j < len(effects):
            j += 1
        if j < len(effects):
            new_effects.append(smooth(effects[i], effects[j], period))
        i = j
    return new_effects


def get_last_frame(effects: List[Effect]) -> Optional[Frame]:
    """
    gets last from from list of Effects
    :param effects:
    :return:
    """
    if not effects:
        return None
    i = -1
    while abs(i) <= len(effects) and not isinstance(last_effect := effects[i], Effect):
        i -= 1
    if abs(i) > len(effects):
        return None
    i = -1
    while abs(i) <= len(last_effect.effect) and not isinstance(last_frame := last_effect.effect[i], Frame):
        i -= 1
    if abs(i) > len(last_effect.effect):
        return None
    return last_frame


def create_turn_on(start_start: int, start_end: int, lowest_br: int, highest_br: int, period_start: int,
                   period_end: int, used_keys: List[int], last_frame: Optional[Frame]) -> Effect:
    """
    creates turn on/off effect
    :param last_frame: last frame to take brightness if necessary
    :param used_keys: list of keys for effect
    :param start_start: min start time
    :param start_end: max start time
    :param lowest_br: lowest brightness
    :param highest_br: highest brightness
    :param period_start: min period
    :param period_end: max period
    :return: effect created
    """
    leds: [Dict[int, List[int]]] = dict()
    for i in range(1, GREEN + BLUE + WHITE + 1):
        leds[i] = list()
    for led in [leds[key] for key in leds.keys() if key in used_keys]:
        n: int = random.randint(start_start, start_end)
        for i in range((start_start + n) // 10):
            led.append(0)
    for (led, key) in [(leds[key], key) for key in leds.keys() if key in used_keys]:
        start_br: int = last_frame.brghtnss[key-1] if last_frame else 0
        period: int = max(period_start + random.randint(0, period_end - period_start), 1)
        brightness: int = lowest_br + random.randint(0, highest_br - lowest_br) if lowest_br < highest_br else \
            lowest_br - random.randint(0, lowest_br - highest_br)
        step = ((brightness - start_br) / period) * 10
        for i in range(period // 10 + 1):
            led.append(min(max(round(start_br + i * step), 0), 255))
    longest: int = max([len(x) for x in leds.values()])
    for led in leds.values():
        last = led[-1] if (current := len(led)) > 0 else 0
        for i in range(longest - current):
            led.append(last)
    parameters = create_param_dict_to(start_start, start_end, lowest_br, highest_br, period_start, period_end)
    effect = Effect(effect=list(), effect_type="TurnOn", parameters=parameters)
    for i in range(longest):
        frame = Frame(brghtnss=[led[i] for led in leds.values()])
        effect.effect.append(frame)
    return effect


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


def create_shine(start_br: int, end_br: int, period_start: int, period_end: int, length: int, used_keys: List[int]) \
        -> Effect:
    """
    creates shine effect
    :param used_keys: used leds
    :param start_br: min brightness
    :param end_br: max brightness
    :param period_start: min period
    :param period_end: max period
    :param length:general length
    :return: effect created
    """
    leds: [Dict[int, List[int]]] = dict()
    for i in range(1, GREEN + BLUE + WHITE + 1):
        leds[i] = list()
    for led in [leds[key] for key in leds.keys() if key in used_keys]:
        period: int = max(period_start + random.randint(0, period_end - period_start), 1)
        brightness: int = start_br + random.randint(0, end_br - start_br)
        step: float = ((brightness - start_br) / period) * 10
        cycles: float = (length * 100) / (2 * period // 10)
        for j in range(round(cycles)):
            for i in range(period // 10):
                led.append(round(start_br + i * step))
            for i in range(period // 10):
                led.append(round(brightness - i * step))
    longest: int = max([len(x) for x in leds.values()])
    for led in leds.values():
        last = led[-1] if (current := len(led) > 0) else 0
        for i in range(longest - current):
            led.append(last)
    parameters = create_shine_params(start_br, end_br, period_start, period_end, length)
    effect = Effect(effect=list(), effect_type="Shine", parameters=parameters)
    for i in range(longest):
        frame = Frame(brghtnss=[led[i] for led in leds.values()])
        effect.effect.append(frame)
    return effect


def create_shine_params(start_br: int, end_br: int, period_start: int, period_end: int, length: int) \
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


def shift_iteration(brightness: int, direction: int, tail: int, period: int, k: int, tail_range: int, forward: bool,
                    pause: bool, key_matrix: List[List[bool]], effect: Effect):
    """

    :param pause: use pause commands
    :param brightness: brightness of shift
    :param direction: direction of shifting
    :param tail: length of tail
    :param period: period of shifting
    :param effect: effect to add iteration to
    :param k: number of iteration
    :param tail_range: range of tail (differnt for first and other iterations)
    :param forward: use forward tail too
    :param key_matrix: leds used
    :return:
    """
    move_i, move_j = dir_dict[direction][0], dir_dict[direction][1]
    leds: [Dict[int, List[int]]] = dict()
    for i in range(1, GREEN + BLUE + WHITE + 1):
        leds[i] = list()
    for row in range(len(key_matrix)):
        for col in range(len(key_matrix[0])):
            if key_matrix[row][col]:
                current_i = col
                current_j = row
                for t in range(tail_range):
                    br = brightness - t * brightness // (tail + 1)
                    next_i = (current_i + move_i * (k - t)) % 9
                    next_j = (current_j + move_j * (k - t)) % 5
                    led = (leds[index_mapping[next_j][next_i]])
                    if not len(led):
                        led.append(br)
                    elif led[-1] < br:
                        led[-1] = br
                    if forward:
                        next_i = (current_i + move_i * (k + t)) % 9
                        next_j = (current_j + move_j * (k + t)) % 5
                        led = (leds[index_mapping[next_j][next_i]])
                        if not led:
                            led.append(br)
                        elif led[-1] < br:
                            led[-1] = br
    for led in leds.values():
        if not led:
            led.append(0)
    frame = Frame(brghtnss=[led[0] for led in leds.values()])
    effect.effect.append(frame)
    if period > 1:
        if not pause:
            for ms in range(period - 1):
                effect.effect.append(frame)
        else:
            effect.effect.append(Command(command='Pause', parameter=period))


def create_shift_effect(direction: int, brightness: int, period: int, tail: int, forward: bool, pause: bool,
                        repeat_flag: bool, all_effects: List[Union[Effect, Command]], key_matrix: List[List[bool]]) \
        -> Effect:
    """
    сreate iteration for shifting
    :param direction: direction of shift
    :param brightness: brightness of shifted leds
    :param period: period to shift
    :param tail: length of tail
    :param forward: if tail is forward too
    :param pause: use pause command or use multiplicating of frames
    :param repeat_flag: if repeat is enabled
    :param all_effects: all created effects
    :param key_matrix: matrix of leds used
    :return:
    """
    # first effect iteration
    effect = Effect(effect=list(), effect_type="shift", parameters=dict())
    repeat = 5 if direction in (2, 3) else 9
    if not forward:
        for k in range(repeat):
            shift_iteration(brightness, direction, tail, period, k, min(tail + 1, k + 1), False, pause,
                            key_matrix, effect)
        # second effect iteration for repeat
        if repeat_flag:
            i = -1
            while not isinstance(all_effects[i], Command) or all_effects[i].command != 'Repeat':
                i -= 1
            repeats = all_effects[i].parameter
            all_effects.pop(i)
            effect.effect.append(Command(command='Repeat', parameter=repeats))
            for k in range(repeat):
                shift_iteration(brightness, direction, tail, period, k, tail + 1, False, pause, key_matrix, effect)
    else:
        for k in range(repeat):
            shift_iteration(brightness, direction, tail, period, k, tail + 1, True, pause, key_matrix, effect)
    return effect


def create_shift_params(brightness: int, direction: int,  period: int, tail: int, forward: bool) \
        -> Dict[str, int]:
    """
    create parameters for shift
    :param brightness: brightness of shift
    :param direction: direction of shift
    :param period: period of shifting
    :param tail: length of tail
    :param forward: move forwards or not
    :return: dict of parameters
    """
    parameters = dict()
    parameters['brightness'] = brightness
    parameters['direction'] = direction
    parameters['period'] = period
    parameters['tail'] = tail
    parameters['forward'] = forward
    return parameters
