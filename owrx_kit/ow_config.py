#!/usr/bin/python3.8

from enum import Enum
from signal import SIGINT, signal
import sys
import pprint

class OwConfig:
    path: object = "bands.py"
    modulations = [
        "NFM",
        "AM",
        "LSB",
        "USB",
        "CW",
        "DMR",
        "DSTAR",
        "NXDN",
        "YSF",
        "BPSK31",
        "BPSK63",
        "FT8",
        "FT4",
        "WSPR",
        "JT65",
        "JT9",
        "Packet",
        "Pocsag"
                   ]
    menu_handlers = dict()
    sdrs = dict()
    bad_choice = "Incorrect selection!"

    class RfMod(Enum):
        NFM = 0
        AM = 1
        LSB = 2
        USB = 3
        CW = 4
        DMR = 5
        DSTAR = 6
        NXDN = 7
        YSF = 8
        BPSK31 = 9
        BPSK63 = 10
        FT8 = 11
        FT4 = 12
        WSPR = 13
        JT65 = 14
        JT9 = 15
        PACKET = 16
        POCSAG = 17

    menu = {
        1: "Print current configuration",
        2: "Add band",
        3: "Delete band",
        4: "Quit"
    }

    def __init__(self, path, sdrs=None):
        self.path = path
        self.sdrs = sdrs
        signal(SIGINT, self.signal_handler)
        self.menu_handlers = {
            1: self.print_config,
            2: self.add_band,
            3: self.del_band,
            4: self.exit_me
        }

    @classmethod
    def exit_me(result_code=0):
        exit(result_code)

    @classmethod
    def signal_handler(sig, frame):
        sys.exit(0)

    @classmethod
    def ask(phrase: object, r_type: object) -> object:
        while True:
            try:
                input_value: object = r_type(input(phrase))
                break
            except ValueError:
                print("Invalid value, try again.")
        return input_value

    # print configurtion
    @classmethod
    def print_config(self):
        # print common information
        sdr_index = 0
        for rtlsdr, data in self.sdrs.items():
            band_index = 0
            print("\n\nSDR-NO: {0}, SDR_NAME: '{1}', PPM: {2:<3}\n".format(sdr_index + 1, data["name"], data["ppm"]))
            # print detailed information
            print("{0:>3} {1:>32} {2:>20} {3:>18} {4:>3} {5:>8} {6:>5}\n".format("NO",
                                                                                 "NAME",
                                                                                 "CENTER FREQ",
                                                                                 "START FREQ",
                                                                                 "RF GAIN",
                                                                                 "S-RATE",
                                                                                 "MOD"
                                                                                 )
                  )
            for k, v in data["profiles"].items():
                print(
                    f"{band_index + 1:>3} {v['name']:>32} {(v['center_freq'] / 1000000):>16} Mhz {(v['start_freq'] / 1000000):>16} Mhz {v['rf_gain']:>3} {v['samp_rate']:>10} {v['start_mod'].upper():>5}")
                band_index += 1
            sdr_index += 1

    # save configuration
    @classmethod
    def save_config(self):
        config_file = open(self.path, "w")
        pp = pprint.PrettyPrinter(indent=4, width=80, depth=None, stream=None, compact=False, sort_dicts=False)
        formatted = pp.pformat(self.sdrs)
        formatted = "sdrs = " + str(formatted)
        config_file.write(formatted)
        config_file.close()

    # add band
    @classmethod
    def add_band(self):
        print(
            "Make sure for what SDR you want to add band info.\nGrab desired SDR info by viewing current configuration.")

        while True:
            user_input = str(input("Continue ? [Y/N]"))
            if user_input.upper() == 'Y' or user_input.upper() == 'N':
                break

        if user_input.upper()[0] == "N":
            self.exit_me(0)
        elif user_input.upper()[0] == "Y":
            pass

        while True:
            sdr_no: int = int(self.ask("Enter SDR no: ", int))
            try:
                sdr_name = str(list(self.sdrs)[sdr_no - 1])
                break
            except IndexError:
                print("No such SDR")

        name = str(self.ask("Enter band name (16 chars max): ", str))
        name = name[:16]

        start_freq: float = float(self.ask("Enter start frequency in MHz: ", float))
        start_freq = int(abs(start_freq * 1000000))

        center_freq: float = float(self.ask("Enter center frequency in Mhz: ", float))
        center_freq = int(abs(center_freq * 1000000))

        gain: int = int(self.ask("Enter gain value: ", int))

        sample_rate: float = float(self.ask("Enter sample rate in MHz: ", float))
        sample_rate = int(abs(sample_rate * 1000000))

        for data in self.RfMod:
            print('{:15} = {}'.format(data.name, data.value))
        while True:
            modulation: int = int(self.ask("Modulation: ", int))
            if any(f.value == modulation for f in self.RfMod):
                break
            else:
                print("No such modulation")

        new_band = {'name': name, 'center_freq': center_freq, 'rf_gain': gain, 'samp_rate': sample_rate,
                    'start_freq': start_freq, 'start_mod': self.modulations[modulation].lower()}
        self.sdrs[sdr_name]["profiles"][name] = new_band

        self.save_config()

    # delete band
    @classmethod
    def del_band(self):
        print(
            "Make sure for what SDR you want to delete band.\nGrab desired SDR info by viewing current configuration.")

        while True:
            user_input = str(input("Continue ? [Y/N]"))
            if user_input.upper() == 'Y' or user_input.upper() == 'N':
                break

        if user_input.upper()[0] == "N":
            self.exit_me(0)
        elif user_input.upper()[0] == "Y":
            pass

        while True:
            sdr_no: int = int(self.ask("Enter SDR no: ", int))
            try:
                sdr_name = str(list(self.sdrs)[sdr_no - 1])
                break
            except IndexError:
                print("No such SDR")

        while True:
            band_no = int(self.ask("Enter band no to delete: ", int))
            d_to_l = list(self.sdrs[sdr_name]["profiles"])
            try:
                delitem = d_to_l[band_no]
                break
            except IndexError:
                print('No such band')
        del self.sdrs[sdr_name]["profiles"][delitem]
        self.save_config()

    # get user input
    @classmethod
    def get_input(self) -> object:
        for no, desc in self.menu.items():
            print("{0:>3}: {1}".format(no, desc))
        while True:
            try:
                user_input: int = int(input("Select: "))
                break
            except ValueError:
                print(self.bad_choice)

        first_key = list(self.menu.keys())[0]
        last_key = list(self.menu.keys())[-1]

        if user_input < first_key or user_input > last_key:
            print(self.bad_choice)
        else:
            self.menu_handlers[user_input]()
        return
