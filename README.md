# Pulmonary Single-Breath Diffusing Capacity (DLCO) Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Single-Breath Carbon Monoxide Diffusing Capacity ($DL_{CO}$) and Krogh Transfer Factor ($K_{CO}$) Analyzer based on ATS/ERS respiratory standards.

```mermaid
flowchart TD
    A[Measured DLCO & Alveolar Volume VA] --> B[Compute Krogh Factor: KCO = DLCO / VA]
    C[Blood Hemoglobin & Sex] --> D[ATS/ERS Hemoglobin Correction cDLCO]
    B & D --> E[Compare Against Predicted Reference Values]
    E --> F[Alveolar-Capillary Membrane vs Volume Restriction Differential]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **ATS/ERS Compliance**: Exact Cotes/Dinakara equations for male and female hemoglobin adjustment.
- **Krogh Factor Discrimination**: Separates primary microvascular obliteration from mechanical restriction.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
