/* GNU linker script for ESP8266 
CH Changed line
    irom0_0_seg :  org = 0x40209000, len = 0x87000
...to...
	irom0_0_seg :  org = 0x40209000, len = 0xa7000
...following https://github.com/micropython/micropython/issues/2700#issuecomment-287737238
Possibly could go as large as 0xc0000 following http://wiki.serafim.eti.br/ht-txt:esp-too-big-irom0
*/

MEMORY
{
    dport0_0_seg : org = 0x3ff00000, len = 0x10
    dram0_0_seg :  org = 0x3ffe8000, len = 0x14000
    iram1_0_seg :  org = 0x40100000, len = 0x8000
    irom0_0_seg :  org = 0x40209000, len = 0xb7000
}

/* define common sections and symbols */
INCLUDE esp8266_common.ld
