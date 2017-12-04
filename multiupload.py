#!/usr/bin/python3

import os,sys,platform
from subprocess import check_output
from pathlib import Path
from string import Template
from time import sleep

scriptPath = os.path.realpath(__file__)

# Start in script current directory
os.chdir(os.path.dirname(scriptPath))

baud = 115200

def guess_port_identifier():
    port = None

    ostype = platform.system()
    if ostype=='Linux':
        port = "/dev/ttyUSB0"
    elif ostype=='Darwin':
        port = "/dev/tty.SLAB_USBtoUART"

    if port == None:
        sys.exit("Couldn't identify operating system and guess serial port location")
    elif not os.path.exists(port):
        sys.exit("Serial port not present as expected, is it plugged in? Are drivers installed?")

    return port

def hardware_config():
    return dict(
        baud=baud,
        port=guess_port_identifier()
    )

def emulate_invocation(templateString, config):
    command = Template(templateString).substitute(config)
    #print("Emulating '" + command + "'")
    sys.argv=command.split()

def call(command, shell=True):
	sys.stdout.write(check_output(command, shell=shell).decode("ascii"))

def replaceall(pattern, replacement, filepath):
	call(["perl", "-pi", "-E", "s/{}/{}/g".format(pattern, replacement),  filepath], shell=False)

def ampyRelease():
    from ampy import cli
    if cli._board is not None:
        try:
            cli._board.close()
        except:
            pass

def putFile(frompath, topath):
    from ampy import pyboard, cli
    try:
        putCommand = "ampy --port ${port} put ${frompath} ${topath}"
        putConfig = hardware_config()
        putConfig.update(
            frompath=frompath,
            topath=topath
        )
        emulate_invocation(putCommand, putConfig)
        try:
            cli.cli()
        except SystemExit:
            pass

    except pyboard.PyboardError:
        print("Is cockle unplugged or in use by another program?")

    ampyRelease()


gitFolder = os.path.realpath("../")
retrotextualFolder = os.path.realpath(gitFolder + "/retrotextual/code/cockle")
mainFile = os.path.realpath(retrotextualFolder + "/main.py")
configFile = os.path.realpath(retrotextualFolder + "/config.py")
neopixelFile = os.path.realpath("/home/cefn/Developer/git/ws2812-SPI/neoSPI.py")

eraseCommand = "esptool.py --port /dev/ttyUSB0 erase_flash"
# D1 Mini
# flashCommand = "esptool.py --port /dev/ttyUSB0 --baud 1500000 write_flash --flash_size=32m 0 build/firmware-combined.bin"
# NodeMCU
flashCommand = "esptool.py --port /dev/ttyUSB0 --baud 1500000 write_flash --flash_mode dio --flash_size=32m 0 ports/esp8266/build/firmware-combined.bin"

def configureBoard(boardId):
	input("Ready to flash board {} : Press Enter".format(boardId))
	
	print("Erasing board {}...".format(boardId))
	call(eraseCommand)
	
	print("Flashing board {}...".format(boardId))
	call(flashCommand)
	
	print("Waiting for board {}...".format(boardId))
	sleep(4)
	
	print("Uploading neopixel library to board {}...".format(boardId))
	putFile(neopixelFile, 'neoSPI.py')

	print("Uploading config.py to board {}...".format(boardId))
	putFile(configFile, 'config.py')

	print("Uploading main.py to board {}...".format(boardId))
	replaceall("boardId.*=.*$", "boardId = '{}'".format(boardId), mainFile)
	putFile(mainFile, 'main.py')

if __name__ == "__main__":
	for boardId in range(0, 20):
		successful = False
		while not(successful):
			try:
				configureBoard(boardId)
				successful = True
			except:
				pass
