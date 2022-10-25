"""
OpenFlow related APIs of ryu.controller module.
"""

import netaddr

from ryu.base import app_manager
from ryu.lib import hub
from ryu.lib import ip
from . import ofp_event


_TMP_ADDRESSES = {}


def register_switch_address(addr, interval=None):
    """
    Registers a new address to initiate connection to switch.
    Registers a new IP address and port pair of switch to let
    ryu.controller.controller.OpenFlowController to try to initiate
    connection to switch.
    :param addr: A tuple of (host, port) pair of switch.
    :param interval: Interval in seconds to try to connect to switch
    """
    assert len(addr) == 2
    assert ip.valid_ipv4(addr[0]) or ip.valid_ipv6(addr[0])
    ofp_handler = app_manager.lookup_service_brick(ofp_event.NAME)
    _TMP_ADDRESSES[addr] = interval

    def _retry_loop():
        # Delays registration if ofp_handler is not started yet
        while True:
            if ofp_handler is not None and ofp_handler.controller is not None:
                for a, i in _TMP_ADDRESSES.items():
                    ofp_handler.controller.spawn_client_loop(a, i)
                    hub.sleep(1)
                break
            hub.sleep(1)

    hub.spawn(_retry_loop)


def unregister_switch_address(addr):
    """
    Unregister the given switch address.
    Unregisters the given switch address to let
    ryu.controller.controller.OpenFlowController stop trying to initiate
    connection to switch.
    :param addr: A tuple of (host, port) pair of switch.
    """
    ofp_handler = app_manager.lookup_service_brick(ofp_event.NAME)
    # Do nothing if ofp_handler is not started yet
    if ofp_handler is None or ofp_handler.controller is None:
        return
    ofp_handler.controller.stop_client_loop(addr)
