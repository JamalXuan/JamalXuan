from ryu.base import app_manager
      #控制管理員
from ryu.ofproto import ofproto_v1_3
      #通訊協定版本
from ryu.controller.handler import set_ev_cls
      #控制端-設置
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPTCHER
      #接收SwitchFeatures訊息,一般狀態
from ryu.controller import ofp_event
      #控制端-事件產生
from ryu.ofproto import ofproto_v1_3_parser
      #解析通訊協定訊息

class MyProject(app_manager.RryuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
          #通訊協定版本
    normal_port = []
          #資料型態以矩陣的方式呈現
    
    def __init__(self, *args, **kwargs):
        super(MyProject).__init__(*args, **kwargs)
        self.mac_to_port = {}
           #連線位置對應連接埠

    def switch_features_handler(self,ev):
           #交換機狀態
      datapath = ev.msg.datapath
      ofproto = datapath.ofproto
      parser = datapath.ofproto_parser
      
