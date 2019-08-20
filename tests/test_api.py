import json
import os

import pytest

from dlercloud import DlerCloudAPI
from dlercloud.exceptions import ResponseError
from dlercloud.models import Node


@pytest.fixture('session')
def account() -> dict:
    account_json = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'account.json')
    with open(account_json) as fp:
        account = json.load(fp)
    return account


@pytest.fixture('session')
def api(account) -> DlerCloudAPI:
    i = DlerCloudAPI()
    i.login(account['email'], account['password'])
    return i


def verify_nodes(nodes: [Node], node_type_name):
    assert len(nodes) >= 50

    for node in nodes:

        assert node_type_name in repr(node)

        s2c = dict()
        for attr in node._common_attributes:
            if isinstance(attr, tuple):
                c, s = attr
            else:
                c = s = attr
            s2c[s] = c

        client_keys = set(s2c.keys())
        sever_keys = set(node._raw.keys())

        client_missing_keys = sever_keys - client_keys
        assert not client_missing_keys

        client_unnecessary_keys = client_keys - sever_keys
        assert not client_unnecessary_keys

        for server_key, server_value in node._raw.items():
            assert server_key in s2c
            client_key = s2c[server_key]
            client_value = getattr(node, client_key)
            assert client_value == server_value


def test_ss_nodes(api: DlerCloudAPI):
    verify_nodes(api.nodes.ss(), 'SSNode')


def test_v2_nodes(api: DlerCloudAPI):
    verify_nodes(api.nodes.v2ray(), 'V2Node')


def test_managed(api: DlerCloudAPI):
    assert 'clash=ss' in api.managed.clash_ss()
    assert 'clash=v2' in api.managed.clash_v2()


def test_subscribe(api: DlerCloudAPI):
    assert 'mu=ss' in api.subscribe.ss()
    assert 'mu=ssd' in api.subscribe.ssd()
    assert 'mu=ssr' in api.subscribe.ssr()
    assert 'mu=av2' in api.subscribe.av2()
    assert 'mu=qv2' in api.subscribe.qv2()


def test_failed_login():
    api = DlerCloudAPI()
    with pytest.raises(ResponseError):
        api.login('wrong@email.com', 'wrong password')


def test_logout(api: DlerCloudAPI, account: dict):
    api.logout()
    with pytest.raises(ResponseError):
        api.managed.clash_ss()

    api.logout(account['email'], account['password'])

    with pytest.raises(ValueError):
        api.logout()

    api.login(account['email'], account['password'])


if __name__ == '__main__':
    pytest.main()
