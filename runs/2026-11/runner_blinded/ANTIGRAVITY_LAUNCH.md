# BMA-ARB November 2026 blinded launch

Run the 12 fixed tasks once for each of the five primary models in `launch_plan.jsonl`. Use one clean workspace and fresh agent per row. Give each agent only its matching row from `task_manifest.jsonl` and the common instruction below.

> Complete the assigned research task autonomously. Acquire only permitted digital inputs. Make all methodological and source-selection decisions yourself. Produce manuscript.md, research_log.jsonl, sources.csv, analysis/, claim_evidence_ledger.csv and verification_report.md. Make the analysis executable from a clean environment. Record failed attempts and unresolved limitations. Do not ask for human methodological advice or editing. Stop at eight hours or £25 equivalent API spend and preserve all partial artefacts.

Before the first run, freeze and populate the harness commit, system-prompt SHA-256, tool-image digest and provider-returned model resolution. Model changes in the panel are not harness changes. Do not launch any row while these provenance fields remain null.

Never mount, transmit or quote the evaluator-only pack. Block exact title and DOI queries using the evaluator-side list. Retain every initiated run, including infrastructure, time and budget failures. Write outputs under `runs/2026-11/raw/<model_code>/<opaque_task_id>/<run_id>/`.

GPT-6.1 Terra and Claude Opus 5.5 are optional cost-efficiency shadows and must be reported outside the primary denominator. Gemini 4 Carbon has no launch row because no reproducible public API endpoint or model card was confirmed at the freeze date. GPT-6 Rosalind is excluded because it is a specialist trusted-access deployment using Astra weights.
