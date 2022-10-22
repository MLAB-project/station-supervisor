#set -e
umount ~/parallella_snaps
mkdir -p ~/parallella_snaps
#sshfs -o Ciphers=arcfour -o Compression=no -o cache=no root@parallella.lan:/tmp/snaps ~/parallella_snaps
sshfs -o Compression=no -o cache=no root@parallella-vlf.lan:/tmp/snaps ~/parallella_snaps
D=$PWD

(cd ~/parallella_snaps/ ; python3 ${D}/snapvizu.py)
