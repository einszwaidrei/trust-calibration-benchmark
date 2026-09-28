# Trust Calibration Benchmark

A benchmark for evaluating whether large language models appropriately
calibrate their responses under varying levels of risk, ambiguity, and
contextual uncertainty.

## Overview

Large language models are increasingly used in situations where users may
rely on their responses to make decisions. In such settings, producing a
plausible answer is not sufficient: a model should also communicate an
appropriate degree of confidence or uncertainty and adapt its behavior to
the context of the request.

The Trust Calibration Benchmark is designed to study this behavior across
scenarios that vary in risk, ambiguity, domain, and interaction type.

The benchmark currently contains 60 scenarios across five domains:

- Medical
- Legal
- Mental health
- Finance
- Cybersecurity

Each scenario is characterized by its risk level, ambiguity level, scenario
type, trust target, and expected model behaviors.

The project focuses on whether an LLM's response is appropriately calibrated
to the context rather than on estimating the model's internal confidence.


## Motivation

An LLM can produce a response that appears clear and confident even when the
available information is incomplete, ambiguous, or associated with
significant risk. Conversely, a model may respond with unnecessary caution
or refusal in situations where a direct answer would be appropriate.

Both behaviors can represent failures of trust calibration.

This project investigates whether LLM responses adapt appropriately to
changes in contextual uncertainty and risk, and seeks to identify the
conditions under which calibration failures occur.


## Research Goal

The goal of the Trust Calibration Benchmark is to evaluate whether large
language models appropriately calibrate their responses to the level of
risk, ambiguity, and contextual uncertainty present in a user's request.

Rather than measuring a model's internal confidence, the benchmark focuses
on how confidence and uncertainty are communicated through the response and
whether the model exhibits behaviors appropriate to the context.

The benchmark evaluates LLM responses across five domains — medical, legal,
mental health, finance, and cybersecurity — using scenarios that vary in
risk level, ambiguity, and interaction type.

The broader objective is to identify conditions under which LLMs become
miscalibrated, including cases in which models respond with excessive
confidence when caution is warranted or with excessive caution when a
direct answer would be appropriate.


## Research Questions

### RQ1 — Overall Trust Calibration

**How well do large language models calibrate their responses to the
appropriate trust target across benchmark scenarios?**

This question measures aggregate trust-calibration performance: whether
model responses communicate a level of confidence or uncertainty that
matches the required trust target for each scenario.


### RQ2 — Effect of Risk and Ambiguity

**How does trust calibration change as risk and ambiguity increase, and is
there an interaction effect between the two?**

This question examines the individual and combined effects of risk level and
ambiguity level on calibration performance, including whether particular
combinations of risk and ambiguity are associated with disproportionate
changes in calibration performance.


### RQ3 — Failure Conditions

**Which domains and scenario types are most associated with
trust-calibration failures?**

This question identifies where calibration failures concentrate across the
five benchmark domains and five interaction patterns: missing context,
reassurance seeking, emotional pressure, harmful intent, and safe control.


### RQ4 — Failure Types

**Which failure modes occur most frequently across model responses?**

This question examines how calibration fails, including patterns such as
overconfidence, excessive caution, dangerous reassurance, and failures to
exhibit context-appropriate behaviors.

## Benchmark Design


## Methodology


## Repository Structure
