# SLUGScan

An RFID (via RDM6300 module) register system, with Google Sheets storage, capable of running on the Raspberry Pi computer system.

## Usage

* Connect RDM6300 to the Raspberry Pi's GPIO. 
* Execute slugscan.py, with an eventname as an argument. `./slugscan.py event_name event_number`

Note that the internet access is required.

## Setup

A Google Sheet and a Google Apps Script deployment of `db/slugscan.gs` configured to use that Google Sheet are required.

You will need to know the `SHEET_ID` (from  `/d/1Nz...` in the Google Sheets URL it's the `1Nz...`) and put this in the Google Apps Script before deploying the App Script. You will also then need to know the Web App `SCRIPT_ID` of the Apps Script Deployment (from the Web app url the `/s/AKf...` it's the `AKF...`) and put this in `slugscan.py` before running `slugscan.py`.
 
## Functionality

* Read a scanned card's ID
* Call to the underlying Google Script with that card number
* Display unknown user if the user is not registered in the Google Sheet
* Otherwise, set the member as signing into or out of an event

## References

* RDM6300 reading routine based on https://behindthesciences.com/electronics/raspberry-pi-rfid-tag-reader/
* Further RDM6300 access inspiration and GPIO connection based on https://github.com/motom001/DoorPi/blob/master/doorpi/keyboard/from_rdm6300.py
