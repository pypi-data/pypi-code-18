import os
import networkx as nx


def load_network(config):
    network_params = config['network']
    path = network_params.get('path', None)
    if path:
        extension = os.path.splitext(path)[1][1:]
        kwargs = {}
        if extension == 'gexf':
            kwargs['version'] = '1.2draft'
            kwargs['node_type'] = int
        try:
            method = getattr(nx.readwrite, 'read_' + extension)
        except AttributeError:
            raise AttributeError('Unknown format')
        return method(path, **kwargs)

    net_args = config['network'].copy()
    net_type = net_args.pop('network_type')

    method = getattr(nx.generators, net_type)
    return method(**net_args)
