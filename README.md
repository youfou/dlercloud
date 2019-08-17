# python-dlercloud-api

## 这是什么

一个用于访问 DlerCloud API 的非官方 Python 客户端。

你可以用它实现自动节点筛选和配置更新等操作。

> 支持 Python 3.x，未验证 Python 2.x 中的兼容性。

## 怎么安装

使用 pip 安装:

```bash
pip3 install -U dlercloud
```

## 如何使用

DlerCloud 在其 Telegram 频道中提供了 API 的简要说明：
https://t.me/dlercloud_news/1090

此 Python 模块按照上述说明进行构建。

登陆后，你只需简单的将官方说明中的地址转换为 Python 语句 (`login` 除外)。例如:

1. `/managed/v1/node_ss` >> `.managed.node_ss()`
2. `/subscribe/v1/sub_ssonly` >> `.subscribe.sub_ssonly()`
> 注意地址中的 `/v1` 在转换后被省略掉了

## 示例代码

这些示例代码可以帮助你更好的理解：

```python
from dlercloud import DlerCloudAPI

api = DlerCloudAPI()

# 使用邮箱和密码登录
api.login('your@email.com', 'YoUr*PasSwoRD')
# 若不想每次重复登陆，可将获得的 access_token 保存下来
# 并在下次创建 DlerCloudAPI 实例时作为初始化参数传入

# 例: 使用 SSNode 节点信息，创建一条 Surge 节点配置

# 请求 /managed/v1/node_ss, 获得 ss 节点列表 
ss_nodes = api.managed.node_ss()
# [<SSNode: 节点1>, <SSNode: 节点2>, <SSNode: 节点3>, ...]

node = ss_nodes[0]
# <SSNode: 节点1>

surge_node_conf = '''
{n.name} = ss, {n.server}, {n.port}, encrypt-method={n.cipher}, password={n.password}, obfs={o}, udp-relay={u}
'''.format(
    n=node,
    o=node.advanced['obfs'],
    u='true' if node.udp else 'false'
).strip()

print(surge_node_conf)
# 节点1 = ss, 1.2.3.4, 1234, encrypt-method=aes-256-gcm, password=abc123, ...

```

## 免责声明

此 Python 模块的作者并非 DlerCloud 网站或公司的人员，不参与 DlerCloud 的运营和建设，也并非其投资者。
