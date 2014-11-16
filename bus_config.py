i2c = {
    "port": 1,
    }

bus = [{
    "type": "i2chub",
    "address": 0x70,
    "children": [
                { "name":"counter", "type":"acount02", "channel": 5, },
                { "name":"clkgen", "type":"clkgen01", "channel": 3, },
        ],
},]


