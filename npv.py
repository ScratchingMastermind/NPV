import curses
import time
import subprocess
import psutil
import shutil
from curses import wrapper
from datetime import datetime

'''
Adafruit 2.8" TFT Display terminal number of colums and rows(lines)
cols = 53
lines =20
'''

def date_time(stdscr):
    time = datetime.now().strftime("%H:%M")
    date = datetime.now().strftime("%d-%b-%Y")
    stdscr.addstr(1, 1, date, curses.A_BOLD)
    stdscr.addstr(2, len(date)//2-len(time)//2, time, curses.A_BOLD)
    stdscr.refresh()


def network(stdscr, y_pos=None, x_pos=None, color=None):
    def find_interface():
        interface = subprocess.run(
            ["ifconfig"], capture_output=True).stdout.decode().strip()
        a = interface.split('\n\n')
        for word in a:
            if 'eth0:' in word:
                return 'Ethernet'
            else:
                return 'Wireless'

    IP = subprocess.run(["hostname", "-i"],
                        capture_output=True).stdout.decode().strip()
    network_window = curses.newwin(5, 20, 3, 1)
    network_window.attron(color)
    network_window.border()
    network_window.attroff(color)
    network_window.addstr(0, 20//2-len("Network")//2, "NETWORK", curses.A_BOLD)
    network_window.addstr(1, 2, f"Conn: {find_interface()}", curses.A_BOLD)
    network_window.addstr(3, 2, f"IP: {IP} ", curses.A_BOLD)
    stdscr.refresh()
    network_window.refresh()


def performance(stdscr, y_pos=None, x_pos=None, color=None):
    performance_window = curses.newwin(5, 27, 8, 1)
    performance_window.attron(color)
    performance_window.border()
    performance_window.attroff(color)
    performance_window.addstr(
        0, 27//2-len("PERFORMANCE")//2, "PERFORMANCE", curses.A_BOLD)

    with open(r"/sys/class/thermal/thermal_zone0/temp") as Temp, open('/proc/uptime', 'r') as time_seconds:
        CurrentTemp = Temp.readline()
        uptime_seconds = float(time_seconds.readline().split()[0])
        mins, sec = divmod(uptime_seconds, 60)
        hour, mins = divmod(mins, 60)
        days, hour = divmod(hour, 24)

        performance_window.addstr(
            1, 2, f"Temp: {int(float(CurrentTemp) / 1000)}°C", curses.A_BOLD)
        performance_window.addstr(
            3, 2, f"Uptime: {days:.0f} days, {hour:.0f}:{mins:.0f}:{sec:.0f}", curses.A_BOLD)
    stdscr.refresh()
    performance_window.refresh()


def hardware(stdscr, y_pos=None, x_pos=None, color=None):
    '''
    Both windows width and text alignment in top-middle of the window is control by
    variable 'HRDWindow_width'.
     '''
    HRDWindow_width = 24
    bar = '█'
    # max number for characters for '100%' diviion and win. width
    # Variables to help Group the windows together
    CPU_RAMWindow_width = 13
    win_posY = y_pos-17
    win_posX = x_pos-25

    hardware_window = curses.newwin(10, HRDWindow_width, win_posY , win_posX )
    hardware_window.attron(color)
    hardware_window.border()
    hardware_window.attroff(color)
    hardware_window.addstr(0, HRDWindow_width//2 -
                           len("Hardware")//2, "HARDWARE", curses.A_BOLD)
    hardware_window.addstr(2, 1, "CPU:", curses.A_BOLD)
    hardware_window.addstr(7, 1, "RAM: ", curses.A_BOLD)
    # CPU & RAM Window
    cpu_window = curses.newwin(3, CPU_RAMWindow_width,  win_posY+1,  win_posX+5)
    ram_window = curses.newwin(3, CPU_RAMWindow_width, win_posY+6, win_posX+5)
    cpu_window.border()
    ram_window.border()
    # Retriving values
    cpu_decimal = psutil.cpu_percent()/100
    ram_decimal = psutil.virtual_memory().percent/100
    cpu_bar = bar*int(cpu_decimal*CPU_RAMWindow_width-2)
    ram_bar = bar*int(ram_decimal*CPU_RAMWindow_width-2)
    # Adding the values to be displayed
    hardware_window.addstr(2, 19,f"{int(cpu_decimal*100)}%", curses.A_BOLD)
    hardware_window.addstr(7, 19, f"{int(ram_decimal*100)}%", curses.A_BOLD)
    # Adding the dynamic bars
    cpu_window.addstr(1, 1, cpu_bar, color)
    ram_window.addstr(1, 1, ram_bar, color)
    stdscr.refresh()
    hardware_window.refresh()
    cpu_window.refresh()
    ram_window.refresh()


def resources(stdscr, y_pos=None, x_pos=None, color=None):
    bar = '█'
    Window_width = 37
    total, used, free = shutil.disk_usage("/mnt/Documents")
    total1, used1, free1 = shutil.disk_usage("/mnt/General")

    maxfullhd = (total // (2**30))
    usedspace = (used // (2**30))

    maxfullhd1 = (total1 // (2**30))
    usedspace1 = (used1 // (2**30))

    drive_1 = bar*int(((usedspace - 0)/(maxfullhd-0))*Window_width-2)
    drive_2 = bar*int(((usedspace1 - 0)/(maxfullhd1-0))*Window_width-2)

    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    MAGENTA_AND_BLACK = curses.color_pair(2)


    drive1_window = curses.newwin(3, Window_width, 13, 10)
    drive2_window = curses.newwin(3, Window_width, 16, 10)
    drive1_window.attron(color)
    drive2_window.attron(color)
    drive1_window.border()
    drive2_window.border()
    drive1_window.attroff(color)
    drive2_window.attroff(color)

    stdscr.addstr(14, 2, "Drive 1:", curses.A_BOLD)
    stdscr.addstr(17, 2, "Drive 2:", curses.A_BOLD)

    stdscr.addstr(
    14, 48, f"{int((usedspace - 0)/(maxfullhd-0)*100)}%", curses.A_BOLD)
    stdscr.addstr(
        17, 48, f"{int((usedspace1 - 0)/(maxfullhd1-0)*100)}%", curses.A_BOLD)

    drive1_window.addstr(1, 1, drive_1, MAGENTA_AND_BLACK)
    drive2_window.addstr(1, 1, drive_2, MAGENTA_AND_BLACK)

    stdscr.refresh()
    drive1_window.refresh()
    drive2_window.refresh()


def main(stdscr):
    # Global Variables
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_AND_BLACK = curses.color_pair(1)

    y, x = stdscr.getmaxyx()
    ch = ""
    curses.curs_set(0)
    stdscr.nodelay(True)
    # Main window descriptions
    HEADER = "NAS Perfomance Viewer"
    # Getting the RPI model name
    name = subprocess.run(["cat", "/sys/firmware/devicetree/base/model"],
                          capture_output=True).stdout.decode().strip()
    # formating to desired output
    deviceName = name.replace(chr(0), "")
    for line in name.splitlines():
        deviceName = line[:15]

    stdscr.clear()
    stdscr.attron(GREEN_AND_BLACK)
    stdscr.border()
    stdscr.attroff(GREEN_AND_BLACK)
    stdscr.addstr(0, x//2 - len(HEADER)//2, HEADER, curses.A_BOLD)
    stdscr.addstr(1, x-16, deviceName, curses.A_BOLD)

    network(stdscr, color=GREEN_AND_BLACK)

    while ch != ord('q'):
        date_time(stdscr)
        hardware(stdscr, y, x, color=GREEN_AND_BLACK)
        resources(stdscr,color=GREEN_AND_BLACK)
        performance(stdscr, color=GREEN_AND_BLACK)
        time.sleep(.2)
        ch = stdscr.getch()


wrapper(main)
