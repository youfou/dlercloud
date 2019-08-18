# Python DlerCloud API



## 这是什么

这是一个可用于调用 DlerCloud API 的非官方 Python 模块。

你可以用它实现自动节点筛选和配置更新等操作。

> 支持 Python 3.x，尚未验证 Python 2.x 中的兼容性。

## 怎么安装

使用 pip 安装:

```bash
pip3 install -U dlercloud
```

## 如何使用

DlerCloud 在其 Telegram 频道中提供了 API 的简要说明:
https://t.me/dlercloud_news/1113

本 Python 模块按照上述说明进行构建。

| API                       | URL                      | `DlerCloudAPI()`            |
| ------------------------- | ------------------------ | ------------------------- |
| 登陆                      | /api/v1/login            | `.login(email, password)` |
| SS 节点列表               | /api/v1/nodes/ss         | `.nodes.ss()`             |
| V2ray 节点列表            | /api/v1/nodes/v2ray      | `.nodes.v2ray()`          |
| Clash SS 托管配置         | /api/v1/managed/clash_ss | `.managed.clash_ss()`     |
| Clash V2ray 托管配置      | /api/v1/managed/clash_v2 | `.managed.clash_v2()`     |
| SS 订阅地址               | /api/v1/subscribe/ss     | `.subscribe.ss()`         |
| SSD 订阅地址              | /api/v1/subscribe/ssd    | `.subscribe.ssd()`        |
| SSR 订阅地址              | /api/v1/subscribe/ssr    | `.subscribe.ssr()`        |
| V2RayN 的订阅地址         | /api/v1/subscribe/av2    | `.subscribe.av2()`        |
| Quantumult V2ray 订阅地址 | /api/v1/subscribe/qv2    | `.subscribe.qv2()`        |

## 示例代码

这些示例代码可以帮助你更好的理解：

```python
from dlercloud import DlerCloudAPI

api = DlerCloudAPI()

# 使用邮箱和密码登录
api.login('your@email.com', 'YoUr*PasSwoRD')

# 若不想每次重复登陆，可将获得的 access_token 保存下来，
# 并在下次创建 DlerCloudAPI 实例时作为初始化参数传入，如:
# api = DlerCloudAPI('mYtOkEnAbCdEf0123456789')
# 目前 access_token 的有效期为 24 小时

# 例: 使用 SSNode 节点信息，创建一条 Surge 节点配置

# 请求 /managed/v1/node_ss, 获得 ss 节点列表
nodes = api.nodes.ss()
# [<SSNode: 节点 1>, <SSNode: 节点 2>, <SSNode: 节点 3>, ...]

node = nodes[0]
# <SSNode: 节点 1>

surge_node_conf = '''
{n.name} = ss, {n.server}, {n.port}, encrypt-method={n.cipher}, password={n.password}{o}{u}
'''.format(
    n=node,
    o=', obfs={}'.format(node.advanced['obfs'][12:])
    if node.advanced.get('obfs') not in ('plain', None) else '',
    u=', udp-relay=true' if node.udp else ''
).strip()

print(surge_node_conf)
# 节点 1 = ss, 1.2.3.4, 1234, encrypt-method=aes-256-gcm, password=abc123, obfs=tls, udp-relay=true
```

## 免责声明

本 Python 模块的作者并非 DlerCloud 网站或公司的人员，不参与 DlerCloud 的经营和建设，也并非其投资者。

