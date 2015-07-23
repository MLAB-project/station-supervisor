Measuring Station Supervisor
=======================

Measuring station management software package. It is used for controlling MLAB's measurement station systems.

Supported measurement stations
-------------

*   Radio meteor detection stations - RMDS01A, RMDS01B, RMDS02A, RMDS02B, RMDS02C

Station hardware supported in future
-------------

*   Weather stations AWS01B
*   Visual meteod detection stations VMDS01A 

Installation
=======

This scripts have to be copyed to ~/Bolidozor directory.
Preferencis -> Default applications fo LXsession -> Autostart -> Add < x-terminal-emulator --geometry=100x20 -e /home/odroid/Bolidozor/station-supervisor/start.sh >

Dependencies
===========

Uses pymlab I2C bindings to control I2C devices such as CLKGEN01B
