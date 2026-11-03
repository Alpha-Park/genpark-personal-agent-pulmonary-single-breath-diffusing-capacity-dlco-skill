---
name: genpark-personal-agent-pulmonary-single-breath-diffusing-capacity-dlco-skill
description: Single-Breath Carbon Monoxide Diffusing Capacity (DLCO) and Krogh transfer coefficient (KCO = DLCO / VA) analyzer. Evaluates alveolar gas transfer efficiency and hemoglobin-adjusted diffusion capacity.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - pulmonary
  - dlco
  - gas-exchange
  - alveolar-capillary
  - openclaw
  - genpark
  - mcp
---

# Pulmonary Single-Breath Diffusing Capacity (DLCO) Skill

## Overview
This skill computes carbon monoxide uptake kinetics across the alveolar-capillary membrane:
- **Diffusion Physiology**: $DL_{CO}$ quantifies the rate of gas transfer from alveolar spaces into red blood cells, reflecting the product of membrane conductance ($D_M$) and pulmonary capillary blood volume ($\theta \cdot V_c$).
- **Hemoglobin Correction**: Blood hemoglobin binding capacity alters carbon monoxide sink kinetics. ATS/ERS standardization corrects measured $DL_{CO}$ to standard reference hemoglobin levels ($14.5\text{ g/dL}$ for males, $13.4\text{ g/dL}$ for females).
- **Krogh Transfer Factor ($K_{CO}$)**: Normalizing $DL_{CO}$ by alveolar volume ($V_A$) separates volume loss (e.g. pneumonectomy) from primary intrinsic alveolar-capillary membrane destruction (e.g. pulmonary fibrosis, emphysema).

## Mathematical Formulation
1. **Krogh Transfer Coefficient**:
   $$K_{CO} = \frac{DL_{CO}}{V_A}$$
2. **ATS/ERS Male Hemoglobin Correction**:
   $$cDL_{CO} = DL_{CO} \times \frac{10.22 + \text{Hb}}{1.7 \times \text{Hb}}$$
3. **ATS/ERS Female Hemoglobin Correction**:
   $$cDL_{CO} = DL_{CO} \times \frac{9.38 + \text{Hb}}{1.7 \times \text{Hb}}$$

## Usage
```python
from client import SingleBreathDiffusingCapacityClient

client = SingleBreathDiffusingCapacityClient()
res = client.calculate_dlco(
    unadjusted_dlco_ml_min_mmhg=26.5,
    alveolar_volume_va_liters=5.5,
    hemoglobin_g_dl=14.2
)
print(res["evaluation"]["classification"])
```
