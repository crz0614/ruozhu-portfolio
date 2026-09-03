# Deployment origin validation / 部署来源校验

## Verified scope

The health checker previously compared only the final hostname. An HTTPS target
redirected to HTTP on the same hostname, or to another port, could pass if status,
body and headers matched. Regression tests reproduce that false-positive before
the fix. The checker now requires the final HTTPS host and effective port to match
the configured origin. An omitted HTTPS port and explicit port 443 are equivalent;
same-origin path redirects remain allowed. Malformed URLs and embedded credentials
are rejected for configured targets before probing. The existing
`unexpected_final_host` report field remains available; the new
`unexpected_final_origin` field includes protocol and port failures.

Configuration URLs must also be strings: numeric, boolean, null, list and object
values are rejected with the same explicit configuration error before probing.
This prevents an incidental `AttributeError` in URL parsing; it is configuration
hardening, not evidence of a live service outage.

Run `python -m unittest discover -s tests -v`: 15 tests, including origin,
configuration and malformed response-metadata regressions. A server-advertised
unknown charset now falls back to UTF-8 with replacement instead of terminating
the full monitoring run. Test responses are injected; these are not new
live deployment or external CRM acceptance results. This change only validates the
final response URL. It does not inspect every redirect hop or prevent the HTTP
client from following redirects. A future redirect-policy change needs its own
transport-level tests. Invalid final origins are failed checks, while transport
errors remain unverified and continue to block a healthy result.

Delivery is through a branch/PR, not a production deployment. Rollback is code-only:
revert this checker change if necessary, with no database migration or data replay.
Rollback restores the old false-positive risk; keep an independent HTTPS/origin
check until the fix can be reapplied. Existing pending PRs are not merged by this
change.

## 中文

原检查只比较最终域名：同域名降级到 HTTP 或切换端口时，仍可能误报健康。
新增回归测试先复现漏判，再验证最终地址必须保持 HTTPS、相同域名及有效端口。
省略端口与显式 443 等价，同源路径跳转仍允许；配置中的坏地址和内嵌凭据在
发出请求前拒绝。保留旧的域名报告字段，并新增来源不一致字段。

URL 配置必须为字符串：数字、布尔值、空值、列表和对象在请求前统一报配置错误，
不再意外触发地址解析器的 `AttributeError`。这是配置边界加固，不代表线上服务故障。

本地共 15 项测试通过，覆盖来源、配置和异常响应元数据；服务器声明未知字符集时，
现在改用 UTF-8 容错解码，不再中断整轮监控。测试注入响应，
不冒充线上部署或真实 CRM 验收。此修复只核验最终地址，不声称阻止所有跳转
或核验中途每一跳。传输失败仍为“未能验证”，不会通过健康门槛。

通过分支/PR 交付，未合并、未上线。回滚仅涉及代码，不迁移数据库、不重放数据；
回滚会恢复原误报风险，期间需保留独立 HTTPS/来源检查。本次不合并其他待批准 PR。
