# SLUGScan

An RFID (via RDM6300 module) register system, with database storage, capable of running on the Raspberry Pi computer system.

## Usage

* Connect RDM6300 to the Raspberry Pi's GPIO. 
* Execute slugscan.py, with an eventname as an argument. `./slugscan.py eventname`
Note that the eventname can be set as an environment variable.

 
## Functionality

* Read a scanned card's ID.
* Check if the card is assigned to a member.
* If not, prompt to register the card to a member - this allows new members to easily register at an event.
* Otherwise, set the member as signing into or out of an event, which is defined as a parameter on starting the program.

## References

* RDM6300 reading routine based on https://behindthesciences.com/electronics/raspberry-pi-rfid-tag-reader/
* Further RDM6300 access inspiration and GPIO connection based on https://github.com/motom001/DoorPi/blob/master/doorpi/keyboard/from_rdm6300.py
* Background image from [Subtle Patterns](https://www.toptal.com/designers/subtlepatterns/gaming/)
