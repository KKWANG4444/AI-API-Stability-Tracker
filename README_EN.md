# LLM API Stability Tracker: Claude, GPT, DeepSeek, Gemini and Grok

[![中文](https://img.shields.io/badge/🇨🇳-中文-red)](README.md)
[![English](https://img.shields.io/badge/🇬🇧-English-blue)](README_EN.md)

> A public record of time-bound availability and latency observations. Results depend on model, account, route, region, and test time.
>
> **Explore:** [current dashboard](https://kkwang4444.github.io/api-status/) · [setup guide](https://github.com/KKWANG4444/ai-api-proxy-china-guide) · [compatible endpoint](https://www.aifast.club)

[![Live Status](https://img.shields.io/badge/Live%20Status-Online-brightgreen)](https://kkwang4444.github.io/api-status/)
[![Updated](https://img.shields.io/badge/Updated-2026--07--12-blue)](https://github.com/KKWANG4444/AI-API-Stability-Tracker)
[![Models](https://img.shields.io/badge/Models-current-FF6B35)](https://www.aifast.club)

> **A public collection of real-world API availability observations:** Claude Opus 4.8/4.7 · GPT-5.5 Pro · DeepSeek V4 Flash/Pro · Gemini 3.1 Pro · Grok 4.2
>
> Published observations are snapshots; model availability and latency vary by node, network, and time

## 🎯 Why This Project

Official API status pages often don't reflect real-world performance — especially from outside the US/EU. This project measures actual API stability from real developer usage:

- **Connection success rate** — How often does each model actually respond?
- **Latency** — Real response times, not synthetic pings
- **China accessibility** — Which models work from mainland China?
- **Provider reliability** — Which providers have the most uptime?

## 📊 Flagship Model Availability Snapshot

The repository publishes periodic observations rather than a guaranteed service-level report. Availability and latency vary by provider, model, test node, network, and time. For current conditions, run a request from your own environment and consult the [live status dashboard](https://kkwang4444.github.io/api-status/).

## 🔑 Key Findings

### 1. Official API vs. Gateway Performance

Without a proxy/gateway, most Western AI APIs are **unreachable** from China:
- OpenAI → direct availability may be limited on some mainland China networks
- Anthropic → availability may vary by region and network environment
- xAI → availability varies by region and account

With a gateway (e.g., [aifast.club](https://www.aifast.club)):
- The gateway provides a compatible route for models currently listed in its console
- 100-500ms additional latency (comparable to VPN)
- availability varies by model, route, account, and time

### 2. Provider and Gateway Variability

Provider and gateway performance varies by model, region, request size, node, and time. Fixed latency and failure-rate claims have been removed; benchmark from your own environment before production use.

## 🚀 Using This Data

If you're a developer integrating AI APIs for production use, this tracker helps you:

1. **Choose the right provider** — based on real uptime, not marketing
2. **Set up fallback models** — know which models to switch to when one fails
3. **Evaluate gateways** — compare performance data before choosing a proxy

## 🔗 Quick Setup with a Gateway

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://www.aifast.club/v1",
    api_key="sk-your-key"
)

# Use a compatible endpoint from your target network
response = client.chat.completions.create(
    model="gpt-5.5",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## 📈 Live Dashboard

![Status Dashboard](assets/img/api-status-screenshot.png)

👉 **[View Full Dashboard](https://kkwang4444.github.io/api-status/)**

## 🏗️ Related Projects

- **[API Status Monitor](https://github.com/KKWANG4444/api-status)** — Live marketplace model dashboard
- **[AI API Proxy Guide](https://github.com/KKWANG4444/ai-api-proxy-china-guide)** — Complete setup guide
- **[LLM API Proxy China](https://github.com/KKWANG4444/llm-api-proxy-china)** — Full model list
- **[Gateway: AIFast Club](https://www.aifast.club)** — One key for all models


## Project map

| Need | Resource |
|:---|:---|
| Copy working integration code | [AI API gateway guide](https://github.com/KKWANG4444/ai-api-proxy-china-guide) |
| Check current model conditions | [API status dashboard](https://github.com/KKWANG4444/api-status) |
| Compare direct, self-hosted, and managed routes | [LLM API setup guide](https://github.com/KKWANG4444/llm-api-proxy-china) |
| Review time-bound stability observations | [Stability tracker](https://github.com/KKWANG4444/AI-API-Stability-Tracker) |
| Test an OpenAI-compatible endpoint | [www.aifast.club](https://www.aifast.club) |

> If this saved you debugging time, star the repository so the guide is easier for the next developer to find.

## License

MIT

## International payment

International users can pay **only with cryptocurrency**. The current balance conversion is:

- **1 AIFast balance dollar ("1 刀") = 0.07 USDC or 0.07 USDT**

Fiat payment methods are not available to international users. Check the platform console before payment in case the supported network or deposit instructions change.
