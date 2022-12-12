from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3
from ryu.controller.handler import set_ev_cls
from ryu.controller.handler import CONFIG_DISPATCHER,MAIN_DISPATCHER
from ryu.controller import ofp_event
from ryu.ofproto import ofproto_v1_3_parser
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4
from ryu.lib.packet import icmp

class Jamal(app_manager.RyuApp):
        OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
        normal_port = []

        def __init__(self, *args, **kwargs):
                super(Jamal,self).__init__(*args, **kwargs)
                self.mac_to_port = {}
                self.hw_addr = 'b8:27:eb:85:68:0f'
                self.ip_addr = '192.168.1.5'

        @set_ev_cls(ofp_event.EventOFPSwitchFeatures,CONFIG_DISPATCHER)
        def switch_features_handler(self,ev):
                datapath = ev.msg.datapath
                ofproto = datapath.ofproto
                parser = datapath.ofproto_parser
                match = parser.OFPMatch()
                actions = [parser.OFPActionOutput(port=ofproto.OFPP_CONTROLLER,
                                                  max_len=ofproto.OFPCML_NO_BUF$
                inst = [parser.OFPInstructionActions(type_=ofproto.OFPIT_APPLY_$
                                                      actions=actions)]
                self.send_port_stats_request(datapath)
                mod = parser.OFPFlowMod(datapath=datapath,
                                        priority=0,
                                        match=parser.OFPMatch(),
                                        instructions=inst)
                datapath.send_msg(mod)

        def send_port_stats_request(self,datapath):
                ofproto = datapath.ofproto
                ofp_parser = datapath.ofproto_parser
                req = ofp_parser.OFPPortSftatsRequest(datapath, 0 , ofp.OFPP_AN$
                datapath.send_msg(req)

        @set_ev_cls(ofp_event.EventOFPPortStatsReply,MAIN_DISPATCHER)
        def port_stats_reply_handler(self,ev):
                msg = ev.msg
                datapath = msg.datapth
                ofproto = datapath.ofproto
                parser = datapath.ofproto_parser

                for stat in ev.msg.body:
                        if stat.port_no < ofproto.OFPP_MAX:
                                self.normal_port.append(stat.port_no)
                if len(self.normal_port) == 2:
                        match = parser.OFPMatch(in_port=self.normal_port[0])
                        actions = [parser.OFPActionOutput(self.normal_port[1])]
                        self.add_flow(datapath, 0 , match , actions)

                        match = parser.OFPMatch(in_port=self.normal_port[1])
                        actions = [parser.OFPActionOutput(self.normal_port[0])]
                        self.add_flow(datapath, 0 , match , actions)

                self.normal_port = []

        @set_ev_cls(ofp_event.EventOFPPacketIn,MAIN_DISPATCHER)
        def _packet_in_handler(self, ev):
                if ev.msg.msg_len < ev.msg.total_len:
                        self.logger.debug("packet truncated: only %s of %s byte$
                                          ev.msg.msg_len, ev.msg.total_len)
                msg = ev.msg
                datapath = msg.datapath
                ofproto = datapath.ofproto
                parser = datapath.ofproto_parser
                in_port = msg.match['in_port']

                pkt = packet.Packet(msg.data)
