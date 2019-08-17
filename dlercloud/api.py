import weakref
from urllib.parse import urljoin

import requests

from .exceptions import ResponseError
from .models import SSNode, V2Node


class DlerCloudAPI:
    def __init__(self, access_token=None, domain='dlercloud.co'):
        """
        Python wrapper for DlerCloud API

        :param access_token: if you have cached access token, fill it here
        :param domain: if the default domain is inaccessible, try another
        """
        self.access_token = access_token
        self.user_id = None

        self.host = domain
        self.base_url = 'https://{}'.format(self.host)

        self._sess = requests.Session()

    @staticmethod
    def __object_hook(obj: dict):
        for k, v in obj.items():
            if v == 'true':
                obj[k] = True
            elif v == 'false':
                obj[k] = False
        return obj

    def _request(self, path, data=None, **kwargs):
        data = data or dict()
        if self.access_token is not None:
            data.update(access_token=self.access_token)
        url = urljoin(self.base_url, path)
        resp = self._sess.post(url, data=data, **kwargs)
        resp.raise_for_status()
        resp_json = resp.json(object_hook=self.__object_hook)
        if resp_json.get('ret') == 0:
            raise ResponseError(resp_json.get('msg'))
        return resp_json.get('data')

    def login(self, email, password):
        """
        log in via email and password, and get access token

        :param email: your login email
        :param password: your login password
        """
        data = self._request('/managed/v1/login', dict(email=email, passwd=password))
        self.access_token = data['token']
        self.user_id = data['user_id']

    @property
    def managed(self):
        return Managed(weakref.proxy(self))

    @property
    def subscribe(self):
        return Subscribe(weakref.proxy(self))


# noinspection PyProtectedMember
def _get_nodes(self, node_api, parser):
    data = self._api._request(self._path.format(node_api))
    nodes = list()
    for node in data:
        nodes.append(parser(node))
    return nodes


# noinspection PyProtectedMember
def _get(self, tail):
    return self._api._request(self._path.format(tail))


# noinspection PyProtectedMember
class Managed:
    _path = '/managed/v1/{}'

    def __init__(self, _api: DlerCloudAPI):
        self._api = _api

    def node_ss(self):
        return _get_nodes(self, 'node_ss', SSNode)

    def node_v2(self):
        return _get_nodes(self, 'node_v2', V2Node)

    def clash_ss(self):
        return self._api._request(self._path.format('clash_ss'))

    def clash_v2(self):
        return self._api._request(self._path.format('clash_v2'))


# noinspection PyProtectedMember
class Subscribe:
    _path = '/subscribe/v1/{}'

    def __init__(self, _api: DlerCloudAPI):
        self._api = _api

    def node_ss(self):
        return _get_nodes(self, 'node_ss', SSNode)

    def node_v2(self):
        return _get_nodes(self, 'node_v2', V2Node)

    def sub_ss(self):
        return _get(self, 'sub_ss')

    def sub_ssonly(self):
        return _get(self, 'sub_ssonly')

    def sub_ssd(self):
        return _get(self, 'sub_ssd')

    def sub_ssr(self):
        return _get(self, 'sub_ssr')

    def sub_av2(self):
        return _get(self, 'sub_av2')

    def sub_qv2(self):
        return _get(self, 'sub_qv2')
