# Market Analyst — review and deployment preparation

Reviewed baseline: `a2472243ccd5f4a1098988d2e5890d44c1ebb49f`.

## Findings addressed

| Severity | Original location | Finding and correction |
|---|---|---|
| P1 | `mcp_server/finance_api.py:get_technical_data` | RSI losses were negative, producing invalid indicator values. Losses now use positive magnitudes, with explicit neutral handling for flat prices. Tests cover rising, falling, flat, and mixed series. |
| P1 | `graph/workflow.py:data_ingestion_node` | Invalid-ticker errors flowed into LLMs as if they were market data. Ingestion now aborts before analysis. |
| P1 | `api/routes.py:approve_research` | Rejection reported success without cancelling the pending checkpoint, allowing later approval. Rejection now ends the graph; approval checks the pending node and state mutations are serialized. |
| P2 | `frontend.py` | Reused thread IDs mixed successive ticker runs; memos disappeared on reruns. Each run gets a fresh ID and results remain in session state. |
| P2 | `api/schemas.py` | Arbitrary action strings and unbounded ticker/session values were accepted. Added UUIDs, bounded ticker validation, and explicit approve/reject actions. |
| P2 | API/UI deployment | Hardcoded localhost and separate manual startup made hosting incomplete. Added a supervised combined service; the backend remains loopback-only. |

## Required configuration

`OPENAI_API_KEY` is required. `OPENAI_MODEL` is configurable and keeps the original `gpt-3.5-turbo` default; verify model access before launch. Render uses root directory `New_Project`, `pip install -r requirements.txt`, and `python serve.py`.

## Remaining limitations

Checkpoint memory is process-local and resets on service restart. This deployment intentionally uses one API worker. It does not place trades. Yahoo Finance data is not exchange-certified real-time data. The RSI calculation uses the project's existing rolling-average method, not Wilder's recursive smoothing, so it can differ from a trading platform's RSI. AI-generated interpretation and execution levels require independent review. No real market/LLM integration result was verified in this session.

## Deployment configuration

`render.yaml` defines one Python web service. `serve.py` runs Streamlit on Render's `PORT`; where applicable, FastAPI runs only on `127.0.0.1:8000`. The launcher stops both processes if either exits. The Streamlit UI requires `APP_PASSWORD` on Render; the blueprint generates it. Retrieve that password from the service's Environment page. This is an owner/demo password gate, not enterprise identity or tenant isolation.

Secrets are declared with `sync: false`; enter real values in Render's Environment settings, never in Git or chat. The blueprint explicitly selects the free compute plan and disables automatic deployment. No paid service or database was provisioned by this change. Free instances have limited memory and can suspend; if a real build or runtime exceeds these limits, choose a suitable plan before deployment. See [Render blueprint fields](https://render.com/docs/blueprint-spec).

## Validation and limitations

The local review ran Python syntax checks, parsed the YAML, and ran focused regression tests against actual source functions with external dependencies controlled. Runtime integration tests are also included and run in GitHub Actions after installing the serving dependencies. Local dependency installation was blocked by a timeout downloading packages from files.pythonhosted.org. Therefore, a passing local isolated test does not establish that the complete deployed application starts.

No real provider requests or production data tests were performed: API credentials were not available. Model names remain configurable and preserve the existing defaults; verify access to those models in your provider account. Requirements constrain compatible major versions but are not a fully resolved lockfile. `uv.lock` and `pyproject.toml` are legacy development manifests; Render installs the explicitly named requirements file instead.

The review covered the main application, configuration, dependency, UI, and deployment paths. It is not a penetration test or proof of enterprise readiness. No obvious API-key patterns were found in the downloaded text source; Git history and binary data were not scanned.
