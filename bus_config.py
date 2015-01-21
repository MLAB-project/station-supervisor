i2c = {
    "port": 4,
    }

bus = [{
    "type": "i2chub",
    "address": 0x73,
    "children": [
                { "name":"counter", "type":"acount02", "channel": 5, },
                { "name":"clkgen", "type":"clkgen01", "channel": 3, },
        ],
},]


