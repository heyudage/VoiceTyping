import sys
import json
import asyncio
import websockets

import pyaudio
import numpy as np

import pyperclip
import win32api
import win32con

import gui
from PyQt5.Qt import *
from PyQt5.QtCore import *

sample_rate = 16000


class Thread(QThread):
    text_signal = pyqtSignal(str)
    voice_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    async def asr(self):
        while 1:
            num_sen = 0
            async with websockets.connect('ws://127.0.0.1:8090/paddlespeech/asr/streaming') as ws:
                audio_info = json.dumps(
                    {"name": "test.wav", "signal": "start", "nbest": 1},
                    sort_keys=True, indent=4, separators=(',', ': '))
                await ws.send(audio_info)
                msg = await ws.recv()
                while 1:
                    b = self.stream.read(85 * 16)
                    numpy_b = np.frombuffer(b, dtype=np.int16)
                    self.voice_signal.emit(int(np.absolute(numpy_b).mean() / 10))
                    await ws.send(b)
                    msg = await ws.recv()
                    msg = json.loads(msg)
                    text = msg['result']
                    if len(text) > num_sen:
                        _t = text[num_sen:len(text)]
                        self.text_signal.emit(_t)
                        if self.paste:
                            pyperclip.copy(_t)
                            win32api.keybd_event(17, 0, 0, 0)
                            win32api.keybd_event(86, 0, 0, 0)
                            win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
                            win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
                        num_sen = len(text)

                    if len(text) == 0:
                        num_sen = 0
                    if 'signal' in msg.keys():
                        # audio_info = json.dumps(
                        #     {"name": "test.wav", "signal": "end", "nbest": 1},
                        #     sort_keys=True, indent=4, separators=(',', ': '))
                        # await ws.send(audio_info)
                        # msg = await ws.recv()
                        break

    def run(self):
        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16, channels=1,
                             rate=sample_rate, input=True,
                             frames_per_buffer=int(85 * 16))

        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.asr())


class Main(QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.setText('启用粘贴')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.thread = Thread()
        self.thread.start()
        self.thread.voice_signal.connect(self.display_voice)
        self.thread.text_signal.connect(self.display_text)
        self.paste = False
        self.thread.paste = False
        self.pushButton.clicked.connect(self.paste_text)

    def display_text(self, text):
        self.label.setText(text)

    def display_voice(self, db):
        self.progressBar.setValue(db)

    def paste_text(self):
        if self.paste:
            self.paste = False
            self.thread.paste = False
            self.pushButton.setText('启用粘贴')
        else:
            self.paste = True
            self.thread.paste = True
            self.pushButton.setText('禁用粘贴')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    sys.exit(app.exec_())
