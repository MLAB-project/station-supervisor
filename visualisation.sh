ulimit -c unlimited
qjackctl&
~/git/pysdr/pysdr-waterfall  -b 16384&
sleep 5
jack_connect system:capture_1 pysdr:input_i
jack_connect system:capture_2 pysdr:input_q
~/git/pysdr/whistle/whistle -p freqx,-26300:kbfir,201,0,400,200:freqx,500:amplify,200&
sleep 3
jack_connect system:capture_1 whistle:input_i
jack_connect system:capture_2 whistle:input_q
jack_connect radio-observer:midi_out pysdr:input_events
alsa_out -d hw:2 -r48000&
sleep 2
jack_connect whistle:output_i alsa_out:playback_1
jack_connect whistle:output_q alsa_out:playback_2
