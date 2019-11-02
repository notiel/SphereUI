from dataclasses import dataclass
from typing import List, Optional, Union, Dict

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
        row = ['0x' + str(x.to_bytes(1, byteorder='big').hex()) for x in self.brghtnss] if not calibrated \
            else ['0x' + str(calibr_list[x].to_bytes(1, byteorder='big').hex()) for x in self.brghtnss]
        dumpdata = ','.join(row)
        return '0x18,' + dumpdata


@dataclass
class Command:
    command: str
    parameter: Optional[int]

    def h_dump(self) -> str:
        """
        dumps command data as code and parameters as hex number
        :return:
        """
        dumpdata = command_codes[self.command] + ','
        if self.parameter:
            dumpdata += str(self.parameter.to_bytes(1, byteorder='big').hex())
        return dumpdata


@dataclass
class Effect:
    effect: List[Union[Frame, Command]]
    effect_type: str
    parameters: Dict[str, Optional[int]]
    descr: str = ""

    def h_dump(self)-> str:
        """
        dumps all commands and frames
        :return:
        """
        return ',\n'.join([x.h_dump() for x in self.effect])





