i2c = {
    "port": 1,
    }

bus = [{
    "type": "i2chub",
    "address": 0x72,
    "children": [
                { "name":"counter", "type":"acount02", "channel": 2, },
                { "name":"clkgen", "type":"clkgen01", "channel": 5, },
        ],
},]


