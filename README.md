# AI API 状态与维护观察

[![English](https://img.shields.io/badge/English-README_EN-blue)](README_EN.md)
[![状态参考](https://img.shields.io/badge/状态-目录与维护信息-blue)](https://kkwang4444.github.io/api-status/)
[![Gitee](https://img.shields.io/badge/Gitee-镜像-red)](https://gitee.com/kkwwww4444/AI-API-Stability-Tracker)

这个仓库记录模型目录、维护公告和接入排错方法。它不是实时监控系统，也不承诺固定延迟、成功率、在线率、节点数量或 SLA。

## 状态应该怎么判断

判断一个模型能否用于生产，至少要看三层信息：

1. **目录配置**：确认模型 ID 是否存在；
2. **维护公告**：确认是否正在维护、下架或迁移；
3. **当前请求**：从实际部署网络发送鉴权请求。

配置存在不等于在线，单次请求成功也不等于长期稳定。

## 当前目录中的样例模型

以下 ID 于 2026-07-13 对照 AI快站公开模型配置复核：

| 供应商 | 样例 ID |
|:---|:---|
| OpenAI | `gpt-5.6-sol`、`gpt-5.6-terra`、`gpt-5.6-luna` |
| Anthropic | `claude-sonnet-5`、`claude-opus-4-8`、`claude-fable-5` |
| xAI | `grok-4.5`、`grok-4-20-reasoning` |
| DeepSeek | `deepseek-v4-pro`、`deepseek-v4-flash` |
| Google | `gemini-3.5-flash`、`gemini-3.1-pro-preview` |
| 阿里 | `qwen3.7-max`、`qwen3.7-plus` |
| 智谱 | `glm-5.2` |
| 月之暗面 | `kimi-k2.7-code` |

这张表只用于展示 ID 格式，不表示全部模型此刻在线。

## 最小请求

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://www.aifast.club/v1",
    api_key=os.environ["AIFAST_API_KEY"],
)

response = client.chat.completions.create(
    model="gpt-5.6-terra",
    messages=[{"role": "user", "content": "reply with ok"}],
)

print(response.choices[0].message.content)
```

`/v1/models` 需要有效 API Key。遇到问题时保存 HTTP 状态码和响应体。

## 可复现的测试记录

如果要发布延迟或可用率数据，记录以下字段：

```text
timestamp:
model_id:
test_region:
network:
sample_count:
p50_ms:
p95_ms:
success_count:
http_status_distribution:
request_features: text / stream / tools / image
```

缺少时间、地区、样本量和分位数的数据，不应写成性能结论。

## 生产接入建议

- 对 429 使用指数退避和随机抖动；
- 只重试可安全重复的请求；
- 设置连接、首字和总请求超时；
- 在应用侧定义模型回退，不允许静默换模型；
- 记录请求模型和最终响应模型；
- 分别测试 streaming、tools、图片和结构化输出。

## 支付说明

国内账户可用方式以控制台当前页面为准。

国际用户只能使用加密货币。**1 个 AI快站余额刀（“1刀”）= 0.07 USDC 或 0.07 USDT。** 国际用户不支持法币支付，充值前必须核对控制台支持的链和充值说明。

## 相关入口

- [AI快站模型广场与控制台](https://www.aifast.club)
- [目录和维护信息页面](https://kkwang4444.github.io/api-status/)
- [接入指南](https://github.com/KKWANG4444/ai-api-proxy-china-guide)
- [English](README_EN.md)

---

**披露：** 本仓库由 AI快站运营者维护，属于第一方状态与接入说明。生产决策应以真实请求、服务条款和当前控制台信息为准。
