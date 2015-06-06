from oslo_concurrency import processutils
from oslo_utils import excutils
from oslo_log import log as logging

from nova import exception
from nova import utils
import nova.network.linux_net as linux_net

LOG = logging.getLogger(__name__)



class FreeBSDBridgeInterfaceDriver(linux_net.LinuxNetInterfaceDriver):

    def plug(self, network, mac_address, gateway=True):
        FreeBSDBridgeInterfaceDriver.ensure_bridge(
                network['bridge'],
                network['bridge_interface'],
                network, gateway)

        return network['bridge']

    def unplug(self, network, gateway=True):
        FreeBSDBridgeInterfaceDriver.remove_bridge(network['bridge'],
                                                   gateway)

    @staticmethod
    @utils.synchronized('lock_bridge', external=True)
    def ensure_bridge(bridge, interface, net_attrs=None, gateway=True,
                      filtering=True):
        LOG.debug("???? ensure_bridge: %s %s", bridge, interface)
        if not FreeBSDBridgeInterfaceDriver.device_exists(bridge):
            LOG.info("Starting bridge")
            utils.execute("ifconfig", bridge, "create", run_as_root=True)
            utils.execute("ifconfig", bridge, "up", run_as_root=True)
        
        if interface:
            LOG.info('Adding interface %(interface)s to bridge %(bridge)s',
                     {'interface': interface, 'bridge': bridge})
            out, err = utils.execute('ifconfig', bridge, 'addm',  interface,
                                check_exit_code=False, run_as_root=True)
            if (err and not 'File exists' in err):
                msg = ('Failed to add interface: %s') % err
                raise exception.NovaException(msg)

            out, err = utils.execute("ifconfig", interface, "up")


    @staticmethod
    def ensure_vlan_bridge(vlan_num, bridge, bridge_interface,
                           net_attrs=None, mac_address=None,
                           mtu=None):
        LOG.debug("???? ensure_vlan_bridge: %s %s %s",
                  vlan_num, bridge, bridge_interface)

    @staticmethod
    def remove_vlan_bridge(vlan_num, bridge):
        LOG.debug("???? remove_vlan_brdige: %s %s", vlan_num, bridge)


    @staticmethod
    @utils.synchronized('lock_bridge', external=True)
    def remove_bridge(bridge, gateway=True, filtering=True):
        LOG.debug("???? remove_brdige: %s", bridge)
        if not FreeBSDBridgeInterfaceDriver.device_exists(bridge):
            return
        else:
            try:
                utils.execute("ifconfig", bridge, "down")
                utils.execute("ifconfig", bridge, "destroy")
            except processutils.ProcessExecutionError:
                with excutils.save_and_reraise_exception():
                    LOG.error("Failed removing bridge device: '%s'", bridge)


    @staticmethod
    def device_exists(dev):
        return dev in utils.execute("ifconfig", "-l")[0].split()

    def get_dev(self, network):
        return network['bridge']
