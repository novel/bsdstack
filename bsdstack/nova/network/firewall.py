from nova.network.linux_net import IptablesManager


class NoopFirewallManager(IptablesManager):

    def apply(self):
        pass

