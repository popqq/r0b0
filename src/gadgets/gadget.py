'''
GVR's design goals for Python
An easy and intuitive language just as powerful as major competitors
Open source, so anyone can contribute to its development
Code that is as understandable as plain English
Suitability for everyday tasks, allowing for short development times
'''
from src.config import LOCALHOST, SERVER_PORT
from src.utils.data import load_pickle, dump_pickle

from socketio import Client, AsyncClient, ClientNamespace
import asyncio
import pickle
from threading import Thread
import urllib3
urllib3.disable_warnings()

class Message(object):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(**kwargs)

class Gadget(Client, Thread):
    def __init__(self, config: dict, hostname=LOCALHOST, port=SERVER_PORT, **kwargs):
        Client.__init__(self,
                        
            ssl_verify=False,            
            )
        Thread.__init__(self,
            target=self._connect,
            # target=Client.wait
            # args=(LOCALHOST, SERVER_PORT)
        )
        self.name = config.get('name','')
        self.namespace = f"/{config.get('namespace',self.name)}"
        # self.namespace = [f"/{config.get('namespace',self.name)}"]
        self.hostname = config.get('hostname',hostname)
        self.port = config.get('port',port)
        self.__dict__.update({'config':config})
        self.__dict__.update(**kwargs)
        self.message = Message
        # self._connect()
    
    # def gadget_connect(self, ):
    #     Thread.start(self)
    
    def _connect(self,):
        hostname=LOCALHOST
        
        port=SERVER_PORT
        header='https'
        print(f"{self.name} connecting to {header}://{hostname}:{port}/{self.namespace}")
        print(self.namespace)
        Client.connect(self,
            url=f"{header}://{hostname}:{port}",
            # "https://r0b0.ngrok.io/",
            namespaces=["/",self.namespace],
            wait=False,
            wait_timeout=1,
            )
        Client.wait(self)
    
    @dump_pickle
    def emit(self, event, data, **kwargs):
        super().emit(
            event,
            data,
            **kwargs)
        
    # def check_msg(self, data):
    def check_msg(event_func):
        def check_func(event, data):
            msg = pickle.loads(data)
            # breakpoint()
            # assert isinstance(msg, self.message), f"{type(msg)} not readable by {type(self)}"
            return event_func(msg)
        return check_func
        
    def pack_msg(self,func,**msg_kwargs):
        return self.message(**msg_kwargs)
    def unpack_msg(self,func,msg):
        return msg.__dict__
    
    def disconnect(self) -> None:
        if self.connected:
            self.join()    
            super().disconnect()

class GamePad(Gadget):
    def __init_(self, **kwargs):
        super.__init__(**kwargs)
