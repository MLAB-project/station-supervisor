ulimit -c unlimited
~/Bolidozor/frequency-guard.py&
jackd -c system -p128 -m -dalsa -dhw:CODEC -r48000 -p4096 -n4 -m -C -i2&
sleep 3
#qjackctl&
#~/Bolidozor/pysdr/pysdr-waterfall -d ~/Bolidozor/pysdr/detectors/meteor_echo.py -b 8192&
#sleep 5
#jack_connect system:capture_1 pysdr:input_i
#jack_connect system:capture_2 pysdr:input_q
#~/Bolidozor/whistle/whistle -p freqx,-10400:kbfir,41,0,400,100:freqx,400:amplify,20&
#sleep 3
#jack_connect system:capture_1 whistle:input_i
#jack_connect system:capture_2 whistle:input_q
#jack_connect whistle:output_i system:playback_1
#jack_connect whistle:output_q system:playback_2
~/git/radio-observer/radio-observer -c ~/Bolidozor/uFlu/uFlu-R1.json&
sleep 3
#jack_connect TEST-R0:midi_out pysdr:input_events
