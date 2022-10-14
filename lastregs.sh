#!/bin/bash
# RSMS detector register dump at 2022-10-14T22:17:51+0000
busybox devmem 0x60001018 32 0x00000200 # SHAPEON
busybox devmem 0x6000101c 32 0x00000100 # SHAPEOFF
busybox devmem 0x60001020 32 0x00000800 # DET0TH
busybox devmem 0x60001024 32 0x00000600 # DET0DU
busybox devmem 0x60001028 32 0x00000800 # DET1TH
busybox devmem 0x6000102C 32 0x00000600 # DET1DU
