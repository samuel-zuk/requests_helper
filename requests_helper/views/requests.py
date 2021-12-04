from requests_helper.common import window


class RequestsWindow(window.Window):
    def __init__(self, width, height, x=None, y=None):
        super().__init__(width, height, x, y, border=False)
        
    
