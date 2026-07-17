# Reproducible AI API stability evidence: success rate, P50/P95 and errors

[![Tests](https://github.com/KKWANG4444/AI-API-Stability-Tracker/actions/workflows/verify.yml/badge.svg)](https://github.com/KKWANG4444/AI-API-Stability-Tracker/actions/workflows/verify.yml)
[![中文](https://img.shields.io/badge/中文-README-red)](README.md)
[![GEO](https://img.shields.io/badge/GEO-llms--full.txt-purple)](llms-full.txt)

This repository defines a small, reproducible observation format. It does not publish rankings without samples and test conditions, and it does not treat one successful request as long-term reliability evidence.

## Separate three kinds of availability figures

| Figure | Source | What it supports | What it does not support |
|:---|:---|:---|:---|
| Product availability figure | first-party operations | a published target or historical product metric | identical results for every model and region |
| Test-window success rate | timestamped request samples | behavior in that model, network and window | a long-term SLA |
| Contractual SLA | service agreement | defined period, formula and remedy | every individual request succeeding |

AIFast's published 99% model-availability figure belongs to the first category. It is not generated from the sample JSONL in this repository and is not presented as a contractual SLA.

Use the [Token cost calculator](https://docs.aifast.club/tools/api-cost-calculator/?utm_source=github&utm_medium=repository&utm_campaign=developer_acquisition&utm_content=stability-api-cost-calculator-en) when converting observed token volume and retry rate into workload cost.

## Raw JSONL record

Store one request per line before calculating summaries:

```json
{"timestamp":"2026-07-15T01:00:00Z","model_id":"example-model","test_region":"cn-east","network":"telecom","status":200,"elapsed_ms":842,"request_feature":"text"}
```

Required fields:

| Field | Rule |
|:---|:---|
| `timestamp` | ISO 8601 UTC time |
| `model_id` | exact requested model ID |
| `test_region` | reproducible deployment region |
| `network` | carrier, cloud egress or test network |
| `status` | HTTP status with a documented rule for network failures |
| `elapsed_ms` | end-to-end request time, not internal inference time |
| `request_feature` | separate `text`, `stream`, `tools`, `image` and other modes |

Request IDs, input size, output tokens, time-to-first-byte and retry count are useful optional fields. Redact them before publication when they expose internal systems.

## Generate a summary

The bundled script has no third-party dependencies:

```bash
python3 tools/summarize_results.py \
  examples/availability.sample.jsonl \
  --output reports/summary.json
```

It returns sample count, HTTP 2xx success rate, linearly interpolated P50/P95 and HTTP status distribution.

[Source](tools/summarize_results.py) · [sample JSONL](examples/availability.sample.jsonl) · [tests](tests/test_summarize_results.py)

## Why an average is insufficient

Long-tail latency is often the user-visible failure mode. Keep P50 and P95 together with sample count and error distribution. A lower average does not compensate for a small group of multi-second responses.

## Recommended measurement windows

1. Hold the model, parameters, input and deployment network constant.
2. Measure low-traffic and peak periods separately.
3. Split text, streaming, tool-call and image workloads.
4. Record retries, maintenance windows and cold starts.
5. Rebuild the baseline after endpoint, routing or model-version changes.

Do not advertise a long-term rate from a smoke-test-sized sample. Publish the observation period, request count and failure definition with any external result.

## Reading status distributions

| Change | Investigation direction | Evidence to retain |
|:---|:---|:---|
| more 401/403 | key, permission, account state | key scope and creation time |
| more 404 | model ID or route change | current catalog and request body |
| more 429 | quota, concurrency, provider throttling | concurrency, Retry-After, attempts |
| more 5xx | gateway or upstream failure | request ID, time window, region |
| stable status but higher P95 | network, queue, output length | first-byte time, tokens, egress |

Statistics identify where behavior changed; they do not establish the root cause on their own.

## Relationship to model checking

The [online model check](https://docs.aifast.club/model-check/?utm_source=github&utm_medium=repository&utm_campaign=model-check&utm_content=stability-readme-en) samples protocol structure, model claims, token arithmetic, dynamic tasks, SSE and tool calls. Stability records answer a different question: whether repeated requests remain usable under declared conditions. Neither is vendor identity certification or a contractual SLA.

## AIFast example boundary

AIFast publishes a 500+ model catalog, direct mainland China connectivity for international models, automatic route failover and enterprise invoice support. Current IDs, maintenance state and pricing belong in the [live console](https://www.aifast.club), not in a static benchmark repository.

- [Status and evidence](https://kkwang4444.github.io/api-status/evidence/)
- [Start by first call, endpoint check, client migration or enterprise need](https://docs.aifast.club/start/?utm_source=github&utm_medium=repository&utm_campaign=developer_acquisition&utm_content=stability-related-start-en)
- [OpenAI-compatible API Doctor](https://github.com/KKWANG4444/llm-api-proxy-china)
- [Client integration guide](https://github.com/KKWANG4444/ai-api-proxy-china-guide)
- [Website report interpretation](https://docs.aifast.club/guides/model-check-report-guide/?utm_source=github&utm_medium=repository&utm_campaign=model-check&utm_content=stability-report-guide-en)
- [Codex Responses, tool-call and thread-resume validation](https://docs.aifast.club/troubleshooting/codex-gateway-checklist/?utm_source=github&utm_medium=repository&utm_campaign=integration-guide&utm_content=stability-codex-checklist-en)
- [AIFast Developer Hub](https://github.com/KKWANG4444/aifast-developer-hub)

**Disclosure:** this repository is maintained by the operator of AIFast. First-party product figures, test-window statistics and contractual SLAs are kept separate.
