i2c = {
    "port": 0
    }

bus = [{
        "type": "i2chub",
        "address": 0x73,
        "children": [
                    {"name": "i2cspi", "type": "i2cspi" , "channel": 0, "address": 44 },
                    {"name": "lighting", "type": "LIGHTNING01A", "TUN_CAP": 6, "channel": 6, },
                ],
    }]

