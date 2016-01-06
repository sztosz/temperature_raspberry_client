#!/usr/bin/env python
from TempThread import TempThread

SERVER_ULR = 'http://192.168.1.101:8000'

temp_thread = TempThread()
temp_thread.start()

raw_input('\n *******Press ENTER key to stop and quit program******* \n')

temp_thread.stop()
temp_thread.join()
