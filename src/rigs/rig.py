# from src import gadgets
# import src.gadgets
from src import gadgets as gadget_shelf
from src.utils import loaders
# from src.gadgets.rig import start_server
from src.rigs.server import Host
from src.messages import msg_funcs
from multiprocessing import Process
import pickle

class Rig(Host):
    def __init__(self, hostname='localhost', port=8080, **kwargs):
        Host.__init__(self, hostname, port, **kwargs)
        self.gadgets = {
            'phone':self,
        }
        self.hostname = hostname
        self.port = port
        self.power = False
    
    def add_gadget(self, gadget_name):
        config = loaders.load_gadget(gadget_name)
        gadget = getattr(gadget_shelf, config['type'], None)
        assert gadget is not None, f"Gadget type {config['type']} does not exist"
        gadget = gadget(config)
        self.gadgets.update({
            gadget_name:gadget
        })
        return gadget
    
    def _get_gadget_namespace(self, gadget):
        return self.gadgets.get(gadget).namespace
        
    def add_message(self, tx_gadget, rx_gadget, msg_func):
        print(tx_gadget, rx_gadget, msg_func)
        tx_namespace, rx_namespace = map(
            self._get_gadget_namespace,
            [tx_gadget, rx_gadget])
        msg_func = getattr(msg_funcs,msg_func)
        def func_emit(data):
            if not isinstance(data,dict): data = pickle.loads(data)
            emit_data = self.gadgets[rx_gadget].message(
                **msg_func(data))
            print(data)
            self.emit(
                event=emit_data.event,
                data=pickle.dumps(emit_data),
                to=None,
                namespace=rx_namespace
            )
        print('tx',tx_namespace)
        self.on_event(
            msg_func()['event'],
            handler=func_emit,
            namespace=tx_namespace
        )
        
        
    def power_on(self,):
        self.start()
        # breakpoint()
        [g.start() for g in self.gadgets.values()]
        self.power = True
            
    def power_off(self,*args,**kwargs):
        assert self.power, "Rig not powered on"
        self.join()
        [g.join() for g in self.gadgets.values()]
        self.power = False
        