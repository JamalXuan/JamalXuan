from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3
from ryu.controller.handler import set_ev_cls
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller import ofp_event
from ryu.ofproto import ofproto_v1_3_parser
 
class MyRyu(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    normal_port = []
 
    def __init__(self, *args, **kwargs):
        super(MyRyu, self).__init__(*args, **kwargs)
 
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        self.send_port_stats_request(datapath)
 
 
    def send_port_stats_request(self, datapath):
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser
        req = ofp_parser.OFPPortStatsRequest(datapath, 0, ofp.OFPP_ANY)
        datapath.send_msg(req)
 
 
    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def port_stats_reply_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
 
        for stat in ev.msg.body:
            if stat.port_no < ofproto.OFPP_MAX:
                self.normal_port.append(stat.port_no)
 
        if len(self.normal_port) == 2:
            # port B to port A
            match = parser.OFPMatch(in_port=self.normal_port[0])
            actions = [parser.OFPActionOutput(self.normal_port[1])]
            self.add_flow(datapath, 0, match, actions)
 
            # port A to port B
            match = parser.OFPMatch(in_port=self.normal_port[1])
            actions = [parser.OFPActionOutput(self.normal_port[0])]
            self.add_flow(datapath, 0, match, actions)
 
        # clear port record after add flow entry
        self.normal_port = []
 
    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
 
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
 
        mod = parser.OFPFlowMod(
         datapath=datapath, 
         priority=priority, 
         command=ofproto.OFPFC_ADD, 
         match=match, 
         instructions=inst)
        
   if buffer_id:
      mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                              match=match,instructions=inst)
     datapath.send_msg(mod)
     
   def send_flow_mod(self,datapath):
    ofp = datapath.ofproto
    ofp_parser = datapath.ofproto_parser
    
    cookie = cookie_mask = 0
    table_id = 0
    idle_timeout = hard_timeout = 0
    priority = 32768
    buffer_id = ofp.OFP_NO_BUFFER
    match = ofp_parser.OFPMatch(in_port=1, eth_dst='xx:xx:xx:xx:xx:xx')
    actions = [ofp_parser.OFPActionOutput(ofp.OFPP_NORMAL,0)]
    inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                             actions)]
    req = ofp_parser.OFPlowMod(datapath,cookie,cookie_mask,
                               table_id, ofp.OFPFC_ADD,
                               idle_timeout,hard_timeout,
                               priotity,buffer_id,
                               ofp.OFPP_ANY, ofp.OFPG_ANY,
                               ofp.OFPFF_SEND_FLOW_REM,
                               math,inst)
    datapath.send_msg(req)
   
   
