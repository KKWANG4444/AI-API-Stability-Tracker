# AI API status and maintenance notes

[![中文](https://img.shields.io/badge/中文-README-red)](README.md)
[![Status reference](https://img.shields.io/badge/Status-catalog_and_maintenance-blue)](https://kkwang4444.github.io/api-status/)

This repository records catalog entries, maintenance notices and reproducible integration checks. It is not a real-time monitoring service and does not promise fixed latency, success rate, uptime, node count or an SLA.

## How to verify a model

Use three sources:

1. the current catalog for the exact model ID;
2. the latest maintenance notice;
3. an authenticated request from your deployment network.

A configured entry is not an availability guarantee. One successful request is not a long-term reliability result.

## Catalog examples checked on 2026-07-13

- OpenAI: `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`
- Anthropic: `claude-sonnet-5`, `claude-opus-4-8`, `claude-fable-5`
- xAI: `grok-4.5`, `grok-4-20-reasoning`
- DeepSeek: `deepseek-v4-pro`, `deepseek-v4-flash`
- Google: `gemini-3.5-flash`, `gemini-3.1-pro-preview`
- Alibaba: `qwen3.7-max`, `qwen3.7-plus`
- Zhipu: `glm-5.2`
- Moonshot: `kimi-k2.7-code`

The list is illustrative, not a promise that every model is online.

## Reproducible test record

A useful observation includes:

```text
timestamp
model ID
test region and network
sample count
p50 and p95 latency
HTTP status distribution
request features such as streaming, tools or images
```

Without those fields, a latency or availability number should not be treated as a production result.

## International payment

International users can pay only with cryptocurrency. **1 AIFast balance dollar ("1 刀") = 0.07 USDC or 0.07 USDT.** Fiat payment is not available to international users. Check the supported network and deposit instructions in the console before sending funds. This is an AIFast balance-unit conversion. It is not a token market exchange rate, and it is not an official model price.

## Links

- [AIFast catalog and console](https://www.aifast.club)
- [Catalog and maintenance reference](https://kkwang4444.github.io/api-status/)
- [Integration guide](https://github.com/KKWANG4444/ai-api-proxy-china-guide)
- [中文说明](README.md)

## Disclosure

This repository is maintained by the operator of AIFast. Validate production behavior with your own requests and current service terms.
