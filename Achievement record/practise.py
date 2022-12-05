from ryu.base import app_manager
      #控制管理員
from ryu.ofproto import ofproto_v1_3
      #通訊協定版本
from ryu.controller.handler import set_ev_cls
      #指定事件類別得以接受訊息和交換器狀態作為參數
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPTCHER
      #接收交換機特徵訊息,一般狀態
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
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self,ev):
      datapath = ev.msg.datapath
            #數據路徑 = 交換機送來的消息
      ofproto = datapath.ofproto
            #通訊協定 = 數據路徑(從通訊協定管道來的)
      parser = datapath.ofproto_parser
            #解析 = 數據路徑(解析來自通訊協定管道)
      match = parser.OFPMatch()
            #匹配 = 解析(來自通訊協管道的匹配)
      actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                        ofproto.OFPCML_NO_BUFFER)]      
            #actions = 解析通訊協定管道所輸出的動作(將通訊協定管道的訊息傳送至控制端,形成緩衝)
      self.add_flow(datapath , 0 , match , actions)
            # 將Table-Miss FlowEntry 設定至交換機，並指定優先權為0(最低) PS：數字越大優先權越高
    def add_flow(self , datapath , priority , match , actions):
            #取得與交換機使用的IF版本對應的通訊協定版本及解析
      ofproto = datapath.ofproto
            #同29行      
      parser = datapath.ofproto_parser
            #同31行
      
      inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                           actions)]
            #Instruction定義當封包滿足匹配時接下來要執行的動作
            #所以將Action以OFPInstructionActions包起來
      
      #FlowMod Function可以讓我們對交換機寫入我制定的Flow Entry(解釋第52~55行)
      mod = parser.OFPFlowMod(datapath=datapath,
                              priority=priority,
                              match=match,
                              instructions=inst)
      datapath.send_msg(mod)
            #將制定好的Flow Entry 送給交換機
      
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
            #制定封包進入通訊協定管道，一般狀態
    def _packet_in_handler(self,ev):
            #收到來自交換機不知道如何處理的封包(匹配到Table-Miss FlowEntry)
      msg = ev.msg
      datapath = msg.datapath.ofproto
      parser = datapath.ofproto
      
      in_port = msg.match['in_port']
            #in_port 相當於封包從交換機的哪個連接埠進到交換機
            #同時也代表source Host MAC要往in_port送，才能送達
      pkt = packet.Packet(msg.data)
      eth = pkt.get_protocols(ethernet.ethernet)[0]
      
      dst = eth.dst
      #得到封包目的端 MAC address
      src = eth.src
      #得到封包來源端 MAC address
      
      dpid = datapath.id
      #交換機的數據路徑ID(獨一無二的ID)
      
      
      
      
      
      
