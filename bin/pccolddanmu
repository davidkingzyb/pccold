#!/usr/bin/env python3
from pccold import Danmu
import threading
print('PcCold with DKZ')
danmu = Danmu()
danmu.login()
danmu.join()
threading.Thread(target=danmu.keeplive).start()
danmu.recv()