#set -e
umount ~/parallella_snaps
mkdir -p ~/parallella_snaps
sshfs root@parallella.lan:/tmp/snaps ~/parallella_snaps
D=$PWD

(cd ~/parallella_snaps/ ; python3 ${D}/snapvizu.py)
