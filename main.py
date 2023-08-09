from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock

from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams
import time

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name='mainscreen')
        self.sm = kwargs
        self.connect_board()
        self.running = True
        
    
    def start_process(self):
        is_connected = self.board.is_prepared()
        if is_connected:
            pass
        else:
            self.connect_board()  
            self.running = True  
        self.get_data()

    def connect_board(self):
        BoardShim.enable_board_logger()
        params = BrainFlowInputParams()
        self.board_id = BoardIds.SYNTHETIC_BOARD.value
        self.sf = BoardShim.get_sampling_rate(self.board_id)
        
        self.board = BoardShim(self.board_id, params)
        self.board.prepare_session()
        self.board.start_stream()
    
    def get_data(self):
        while self.running:
            time.sleep(1)
            self.data = self.board.get_board_data()
            self.ids.brainflowdata.text += str(self.data[0])
            # self.ids.brainflow.data.text += str(len(self.data))
            print(self.data)
            return self.data

    def stop_connection(self):
        self.running = False
        print('stop process!!!!!!!!!!!!!')
        self.board.stop_stream()
        self.board.release_session()

class WindowManager(Screen):
    pass

class MainWindow(App):
    def build(self):

        Builder.load_file('main.kv')
        self.sm = ScreenManager()
        k_args = {'sm':self.sm}
        screens = [
                MainScreen(**k_args), 
                # WindowManager(**k_args)
                ]
        
        for screen in screens:
            self.sm.add_widget(screen)
        
        return self.sm
if __name__ == "__main__":
    MainWindow().run()