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
                                                  max_len=ofproto.OFPCML_NO_BUFFER)]
                inst = [parser.OFPInstructionActions(type_=ofproto.OFPIT_APPLY_ACTIONS,
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
                req = ofp_parser.OFPPortSftatsRequest(datapath, 0 , ofp.OFPP_ANY)
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
                        self.logger.debug("packet truncated: only %s of %s bytes",
                                          ev.msg.msg_len, ev.msg.total_len)
                msg = ev.msg
                datapath = msg.datapath
                ofproto = datapath.ofproto
                parser = datapath.ofproto_parser
                in_port = msg.match['in_port']

                pkt = packet.Packet(msg.data)
                eth = pkt.get_protocols(ethernet.ethernet)[0]

                if eth.ethertype == ether_type.ETH_TYPE_LLDP:
                        return
                dst = eth.dst
                src = eth.src

                dpid = format(datapath.id, "d").zfill(16)
                self.mac_to_port.setfault(dpid, {})
                self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
                self.mac_to_port[dpid][src] = in_port

                if dst in self.mac_to_port[dpid]:
                        out_port = self.mac_to_port[dpid][dst]
                else:
                        out_port = ofproto.OFPP_FLOOD

                actions = [parser.OFPActionOutput(out_port)]

                if out_port != ofproto.OFPP_FLOOD:
                        match = parser.OFPMatch(in_port=in_port , eth_dst=dst ,eth_src=src)

                        if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                                self.add_flow(datapath , 1 , match , actions , msg.buffer_id)
                                return
                        else:
                                self.add_flow(datapath , 1 , match , actions)
                data = None
                if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                        data = msg.data

                out = parser.OFPPacketOut(datapath=datapath,buffer_id=msg.buffer_id,
                                          in_port=in_port,actions=actions,data=data)
                datapath.send_msg(out)

        def send_flow_mod(self,datapath):
                ofproto = datapath.ofproto
                parser = datapath.ofproto_parser
                table_id = 2
                priority = 11
                buffer_id = ofproto.OFP_NO_BUFFER
                match = parser.OFPMatch(in_port=1,eth_dst='00:50:c5:00:00:a3')
                actions = [parser.OFPActionOutput(ofproto.OFPP_NORMAL,0)]
                inst = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                                     actions)]
                req = ofp_parser.OFPFlowMod(datapath,table_id,ofp.OFPFC_ADD,priority,
                                            buffer_id,ofp.OFPP_ANY,ofp.OFPG_ANY,
                                            ofp.OFPFF_SEND_FLOW_REM,match,inst)
                datapath.send_msg(req)

        def _handle_arp(self,datapath,port,pkt_ethernet,pkt_arp):
                if pkt_arp.opcode != arp.ARP_REQUEST:
                        return
                pkt = packet.Packet.Packet()
                pkt.add_protocol(ethernet.ethernet(ethertype=pkt_ethernet.ethertype,
                                 dst=pkt_ethernet.src,
                                 src=self.hw_addr))
                pkt.add_protocol(ipv4.ipv4(dst=pkt_ipv4.src,src=self.hw_addr,
                                 proto=pkt_ipv4.proto))
                pkt.add_protocol(icmp.icmp(type_=icmp.ICMP_ECHO_REPLY,
                                 code=icmp.ICMP_ECHO_REPLY_CODE,
                                 csum=0,data=pkt_icmp_icmp.data))
                self._send_packet(datapath,port,pkt)

        def _send_packet(self,datapath,port,pkt):
                ofproto = datapath.ofproto
                parser = datapath.ofproto_parser
                pkt.serialize()
                self.logger.info("packet-out %s" % (pkt,))
                data = pkt.data
                actions = [parser.OFPActionOutput(port=port)]
                out = parser.OFPPacketOut(datapath=datapath,
                                          buffer_id=ofproto.OFP_NO_BUFFER,
                                          in_port=ofproto.OFPP_CONTROLLER,
                                          actions=actions,data=data)
                datapath.send_msg(out)

