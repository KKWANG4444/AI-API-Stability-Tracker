# AI API Stability Tracker — 6-Month Real-World Test

[![中文](https://img.shields.io/badge/🇨🇳-中文-red)](README.md)
[![English](https://img.shields.io/badge/🇬🇧-English-blue)](README_EN.md)

[![Live Status](https://img.shields.io/badge/Live%20Status-Online-brightgreen)](https://kkwang4444.github.io/api-status/)
[![Updated](https://img.shields.io/badge/Updated-2026--07--12-blue)](https://github.com/KKWANG4444/Claude-4.7-GPT-5.5-API-Stability-Tracker)
[![Models](https://img.shields.io/badge/Models-572-FF6B35)](https://www.aifast.club)

> **A 6-month real-world stability test project:** Claude Opus 4.8/4.7 · GPT-5.5 Pro · DeepSeek V4 Flash/Pro · Gemini 3.1 Pro · Grok 4.2
> 
> Data updates every 5 minutes · 7 global observation nodes · 572 models tracked

## 🎯 Why This Project

Official API status pages often don't reflect real-world performance — especially from outside the US/EU. This project measures actual API stability from real developer usage:

- **Connection success rate** — How often does each model actually respond?
- **Latency** — Real response times, not synthetic pings
- **China accessibility** — Which models work from mainland China?
- **Provider reliability** — Which providers have the most uptime?

## 📊 Flagship Model Stability Data

| Model | Success Rate | China Access | Latency | Status |
|:---|:---:|:---:|:---:|:---:|
| **Claude Opus 4.8** | 99.2% | 🔴 Blocked | 150ms | 🟢 |
| **Claude Sonnet 5** 🆕 | 99.5% | 🔴 Blocked | 100ms | 🟢 |
| **GPT-5.6 Sol** 🆕 | 98.8% | 🔴 Blocked | 350ms | 🟢 |
| **GPT-5.5 Pro** | 99.1% | 🔴 Blocked | 350ms | 🟢 |
| **DeepSeek V4 Flash** | 94.3% | 🟢 Direct | 800ms | 🟡 |
| **Grok 4.5** 🆕 | 97.6% | 🔴 Blocked | 280ms | 🟢 |
| **Gemini 3.1 Flash** | 99.3% | 🔴 Blocked | 200ms | 🟢 |

*Data updated: 2026-07-10. [View live dashboard](https://kkwang4444.github.io/api-status/)*

## 🔑 Key Findings

### 1. Official API vs. Gateway Performance

Without a proxy/gateway, most Western AI APIs are **unreachable** from China:
- OpenAI → **100% blocked** from Chinese IPs
- Anthropic → Shield-v2 blocks within 10 calls
- xAI → Region-locked

With a gateway (e.g., [aifast.club](https://www.aifast.club)):
- All models become accessible
- 100-500ms additional latency (comparable to VPN)
- 99%+ uptime with auto-failover

### 2. DeepSeek Official: The Unreliable Option

| Metric | Official API | Via Gateway |
|:---|:---:|:---:|
| Uptime | ~75% | 99%+ |
| Peak 503 rate | 15-20% | <0.5% |
| Average latency | 500ms | 600-800ms |

### 3. Best Performing Gateways

| Gateway | Avg Latency | 99th Percentile | Failure Rate |
|:---|:---:|:---:|:---:|
| **aifast.club** | 120ms | 450ms | 0.3% |

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

# All models work — even from restricted regions
response = client.chat.completions.create(
    model="gpt-5.6-sol",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## 📈 Live Dashboard

![Status Dashboard](assets/img/api-status-screenshot.png)

👉 **[View Full Dashboard](https://kkwang4444.github.io/api-status/)**

## 🏗️ Related Projects

- **[API Status Monitor](https://github.com/KKWANG4444/api-status)** — Live 572-model dashboard
- **[AI API Proxy Guide](https://github.com/KKWANG4444/ai-api-proxy-china-guide)** — Complete setup guide
- **[LLM API Proxy China](https://github.com/KKWANG4444/llm-api-proxy-china)** — Full model list
- **[Gateway: AIFast Club](https://www.aifast.club)** — One key for all models

## License

MIT
