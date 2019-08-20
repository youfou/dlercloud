import inspect
import weakref
from urllib.parse import urljoin

import requests

from .exceptions import ResponseError
from .models import SSNode, V2Node


class DlerCloudAPI:
    def __init__(self, access_token=None, host='dlercloud.co'):
        """
        Python wrapper for DlerCloud API

        :param access_token: if you have cached access token, fill it here
        :param host: if the default domain is inaccessible, try another
        """
        self.access_token = access_token
        self.user_id = None

        self.host = host
        self.base_url = 'https://{}/api/v1/'.format(self.host)

        self._sess = requests.Session()

    def _request(self, path, data=None, **kwargs):
        data = data or dict()
        if self.access_token and path not in ('login', 'logout'):
            data.update(access_token=self.access_token)
        url = urljoin(self.base_url, path)
        resp = self._sess.post(url, data=data, **kwargs)
        resp.raise_for_status()
        resp_json = resp.json()
        ret_code = int(resp_json.get('ret'))
        if ret_code < 200 or ret_code >= 300:
            raise ResponseError('[{}] {}'.format(ret_code, resp_json.get('msg')))
        return resp_json.get('data')

    def login(self, email, password):
        """
        log in via email and password, and get access token

        :param email: your account email
        :param password: your account password
        """
        data = self._request('login', dict(email=email, passwd=password))
        self.access_token = data['token']
        self.user_id = data['user_id']
        return self.access_token

    def logout(self, email=None, password=None):
        """
        log out, to abandon current access token.
        if email or password is not provided, current access token will be used as payload.

        :param email: your account email
        :param password: your account password
        """

        if email and password:
            self._request('logout', dict(email=email, passwd=password))
            self.access_token = None
        elif self.access_token:
            self._request('logout', dict(access_token=self.access_token))
            self.access_token = None
        else:
            raise ValueError('email and password, or access token (.access_token) is needed at least')

    @property
    def nodes(self):
        return Nodes(weakref.proxy(self))

    @property
    def managed(self):
        return Managed(weakref.proxy(self))

    @property
    def subscribe(self):
        return Subscribe(weakref.proxy(self))


# noinspection PyProtectedMember
class Category:
    def __init__(self, _api: DlerCloudAPI):
        self._api = _api
        self._category_name = self.__class__.__name__.lower() + '/'

    def _request(self):
        return self._api._request(urljoin(self._category_name, inspect.stack()[2][3]))

    def _get(self):
        return self._request()

    def _get_nodes(self, node_type):
        nodes = list()
        for node in self._request():
            nodes.append(node_type(node))
        return nodes


class Nodes(Category):
    def ss(self):
        return self._get_nodes(SSNode)

    def v2ray(self):
        return self._get_nodes(V2Node)


class Managed(Category):
    def clash_ss(self):
        return self._get()

    def clash_v2(self):
        return self._get()


class Subscribe(Category):
    def ss(self):
        return self._get()

    def ssd(self):
        return self._get()

    def ssr(self):
        return self._get()

    def av2(self):
        return self._get()

    def qv2(self):
        return self._get()
