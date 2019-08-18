class Node:
    _common_attributes = (
        'id',
        'name',
        'type',
        'server',
        'port',
        'cipher',
        ('proxy_group', 'proxy group')
    )

    def __init__(self, _raw: dict):
        """
        Base node class

        :param _raw: raw json dict parsed from api response
        """
        self._raw: dict = _raw

        self.id = None
        self.name = None
        self.type = None
        self.server = None
        self.port = None
        self.cipher = None
        self.proxy_group = None

        self._parse_from_raw()

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    def _parse_from_raw(self):
        for attr in self._common_attributes:
            if isinstance(attr, tuple):
                prop, key = attr
            else:
                prop = key = attr
            setattr(self, prop, self._raw.get(key))


class SSNode(Node):

    def __init__(self, _raw: dict):
        """
        Base node class

        :param _raw: raw json dict parsed from api response
        """
        self._common_attributes += (
            'password',
            'advanced',
            'udp',
            'more',
            'group',
        )

        self.password = None
        self.advanced = None
        self.udp = None
        self.group = None

        super(SSNode, self).__init__(_raw)


class V2Node(Node):

    def __init__(self, _raw: dict):
        """
        Base node class

        :param _raw: raw json dict parsed from api response
        """
        self._common_attributes += (
            'uuid',
            ('alter_id', 'alterId'),
            'network',
            ('ws_headers', 'ws-headers'),
            'tls',
            'host',
        )

        self.uuid = None
        self.alter_id = None
        self.network = None
        self.ws_headers = None
        self.tls = None
        self.host = None

        super(V2Node, self).__init__(_raw)
