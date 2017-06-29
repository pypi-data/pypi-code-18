import etcd
import common


def do_list(server=common.ETCD):
    """
    list eaas machines
    :param server:
    """
    client = etcd.Client(host=server)
    print "EAAS Nodes:"
    print "=" * 50
    nodes = client.read("/eaas/nodes", recursive=False)
    for child in nodes.children:
        address = child.key.rsplit("/", 1)[-1]
        # caps
        caps = client.read("{}/caps".format(child.key)).value
        print " {} caps={}".format(address, caps.split(","))
        containers = client.read("{}/containers".format(child.key)).children
        for container in containers:
            containername = container.key.rsplit("/", 1)[-1]
            containerinfo = client.read("{}/image".format(container.key))
            print "   {} image={}".format(containername, containerinfo.value)


def get_nodes(server=common.ETCD, filtercaps=None):
    """
    List the EAAS nodes we can see
    :param server:
    :param filtercaps: filter to only include nodes with these caps
    :return:
    """
    nodelist = {}
    client = etcd.Client(host=server)
    nodes = client.read("/eaas/nodes", recursive=False)
    for child in nodes.children:
        address = child.key.rsplit("/", 1)[-1]

        try:
            caps = client.read("{}/caps".format(child.key)).value
            caps = caps.decode("utf-8", 'ignore')
            caps = caps.strip().split(",")

            if filtercaps:
                if isinstance(filtercaps, list):
                    filtercaps = filtercaps[0].split(",")
                skip = False
                for cap in filtercaps:
                    if cap not in caps:
                        skip = True
                if skip:
                    continue

            nodelist[address] = {
                "caps": caps
            }
            nodelist[address]["containers"] = []
            containers = client.read("{}/containers".format(child.key)).children
            for container in containers:
                containername = container.key.rsplit("/", 1)[-1]
                containerinfo = client.read("{}/image".format(container.key))
                nodelist[address]["containers"].append(
                    {
                        "name": containername,
                        "image": containerinfo.value
                    }
                )
        except etcd.EtcdKeyNotFound:
            pass
        
    return nodelist
