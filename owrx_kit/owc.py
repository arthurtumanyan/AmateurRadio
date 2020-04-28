#!/usr/bin/python3.8

from enum import Enum
from bands import sdrs
from signal import SIGINT, signal
import sys
import pprint

CONFIG_FILE = "bands.py"

modulations = ["NFM", "AM", "LSB", "USB", "CW", "DMR", "DSTAR", "NXDN", "YSF", "BPSK31", "BPSK63", "FT8", "FT4", "WSPR",
               "JT65", "JT9", "Packet", "Pocsag"]


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


def exit_me(result_code=0):
    exit(result_code)


def print_current_config():
    # print common information
    sdr_index = 0
    for rtlsdr, data in sdrs.items():
        band_index = 0
        print("\n\nSDR-NO: {0}, SDR_NAME: '{1}', PPM: {2:<3}\n".format(sdr_index + 1, data["name"], data["ppm"]))
        # print detailed information
        print("{0:>3} {1:>32} {2:>20} {3:>18} {4:>3} {5:>8} {6:>5}\n".format("NO", "NAME", "CENTER FREQ", "START FREQ",
                                                                             "RF GAIN", "S-RATE", "MOD"))
        for k, v in data["profiles"].items():
            print(
                f"{band_index + 1:>3} {v['name']:>32} {(v['center_freq'] / 1000000):>16} Mhz {(v['start_freq'] / 1000000):>16} Mhz {v['rf_gain']:>3} {v['samp_rate']:>10} {v['start_mod'].upper():>5}")
            band_index += 1
        sdr_index += 1


def ask(phrase: object, r_type: object) -> object:
    while True:
        try:
            input_value: object = r_type(input(phrase))
            break
        except ValueError:
            print("Invalid value, try again.")
    return input_value


def save_sdr_info():
    config_file = open(CONFIG_FILE, "w")
    pp = pprint.PrettyPrinter(indent=4, width=80, depth=None, stream=None, compact=False, sort_dicts=False)
    formatted = pp.pformat(sdrs)
    formatted = "sdrs = " + str(formatted)
    config_file.write(formatted)
    config_file.close()


def add_band():
    print("Make sure for what SDR you want to add band info.\nGrab desired SDR info by viewing current configuration.")

    while True:
        user_input = str(input("Continue ? [Y/N]"))
        if user_input.upper() == 'Y' or user_input.upper() == 'N':
            break

    if user_input.upper()[0] == "N":
        exit_me(0)
    elif user_input.upper()[0] == "Y":
        pass

    while True:
        sdr_no: int = int(ask("Enter SDR no: ", int))
        try:
            sdr_name = str(list(sdrs)[sdr_no - 1])
            break
        except IndexError:
            print("No such SDR")

    name = str(ask("Enter band name (16 chars max): ", str))
    name = name[:16]

    start_freq: float = float(ask("Enter start frequency in MHz: ", float))
    start_freq = int(abs(start_freq * 1000000))

    center_freq: float = float(ask("Enter center frequency in Mhz: ", float))
    center_freq = int(abs(center_freq * 1000000))

    gain: int = int(ask("Enter gain value: ", int))

    sample_rate: float = float(ask("Enter sample rate in MHz: ", float))
    sample_rate = int(abs(sample_rate * 1000000))

    for data in RfMod:
        print('{:15} = {}'.format(data.name, data.value))
    while True:
        modulation: int = int(ask("Modulation: ", int))
        if any(f.value == modulation for f in RfMod):
            break
        else:
            print("No such modulation")

    new_band = {'name': name, 'center_freq': center_freq, 'rf_gain': gain, 'samp_rate': sample_rate,
                'start_freq': start_freq, 'start_mod': modulations[modulation].lower()}
    sdrs[sdr_name]["profiles"][name] = new_band

    save_sdr_info()


def del_band():
    print("Make sure for what SDR you want to delete band.\nGrab desired SDR info by viewing current configuration.")

    while True:
        user_input = str(input("Continue ? [Y/N]"))
        if user_input.upper() == 'Y' or user_input.upper() == 'N':
            break

    if user_input.upper()[0] == "N":
        exit_me(0)
    elif user_input.upper()[0] == "Y":
        pass

    while True:
        sdr_no: int = int(ask("Enter SDR no: ", int))
        try:
            sdr_name = str(list(sdrs)[sdr_no - 1])
            break
        except IndexError:
            print("No such SDR")

    while True:
        band_no = int(ask("Enter band no to delete: ", int))
        d_to_l = list(sdrs[sdr_name]["profiles"])
        try:
            delitem = d_to_l[band_no]
            break
        except IndexError:
            print('No such band')
    del sdrs[sdr_name]["profiles"][delitem]
    save_sdr_info()

def signal_handler(sig, frame):
    sys.exit(0)


INCORRECT_SELECTION = "Incorrect selection!"

menu = {
    1: "Print current configuration",
    2: "Add band",
    3: "Delete band",
    4: "Quit"
}

menu_handlers = {
    1: print_current_config,
    2: add_band,
    3: del_band,
    4: exit_me
}


def get_input() -> object:
    for no, desc in menu.items():
        print("{0:>3}: {1}".format(no, desc))
    while True:
        try:
            user_input: int = int(input("Select: "))
            break
        except ValueError:
            print(INCORRECT_SELECTION)

    first_key = list(menu.keys())[0]
    last_key = list(menu.keys())[-1]

    if user_input < first_key or user_input > last_key:
        print(INCORRECT_SELECTION)
    else:
        menu_handlers[user_input]()
    return


def main() -> object:
    signal(SIGINT, signal_handler)
    get_input()
    return


if __name__ == '__main__':
    main()
