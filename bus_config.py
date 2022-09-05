i2c = {
    "port": 0,
    "driver":"smbus"
    }

bus = [{
        "type": "i2chub",
        "address": 0x73,
        "children": [
                    {"name": "i2cspi", "type": "i2cspi" , "channel": 0, "address": 44 },
                    {"name": "lighting", "type": "LIGHTNING01A", "TUN_CAP": 0, "address": 0x02, "channel": 6, },
                    { "name":"ADC_clock", "type":"clkgen01", "channel": 4, },
                    { "name":"clkgen", "type":"clkgen01", "channel": 5, },
                ],
    }]
