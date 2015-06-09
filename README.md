## bsdstack

Set of helper classes for running OpenStack with FreeBSD/Xen.

More details:

http://empt1e.blogspot.ru/2015/06/openstack-on-freebsdxen-proof-of-concept.html

## Usage

	# python setup.py install

Then add the following to your nova.conf:

	[DEFAULT]
        ...
	linuxnet_interface_driver = bsdstack.nova.network.freebsd_net.FreeBSDBridgeInterfaceDriver
	firewall_manager = bsdstack.nova.network.firewall.NoopFirewallManager
        ...

## TODO

* Implement VLAN routines
* Add unit tests
