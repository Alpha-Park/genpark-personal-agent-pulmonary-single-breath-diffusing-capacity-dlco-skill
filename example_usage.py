"""
Example usage of Pulmonary Single-Breath Diffusing Capacity (DLCO) Skill.
Demonstrates normal gas exchange vs anemia-corrected diffusion vs severe alveolar-capillary block.
"""

import json
from client import SingleBreathDiffusingCapacityClient


def main():
    print("=== Testing Pulmonary Single-Breath Diffusing Capacity (DLCO) Skill ===")
    client = SingleBreathDiffusingCapacityClient()

    # 1. Normal healthy male (DLCO = 27.5, VA = 5.8 L, Hb = 15.0 g/dL, pred DLCO = 28.0)
    res_normal = client.calculate_dlco(
        unadjusted_dlco_ml_min_mmhg=27.5,
        alveolar_volume_va_liters=5.8,
        hemoglobin_g_dl=15.0,
        predicted_dlco_ml_min_mmhg=28.0,
        predicted_kco=4.8,
        is_female=False
    )
    print("\n[Case 1: Normal Alveolar-Capillary Diffusing Capacity]")
    print(json.dumps(res_normal, indent=2))

    # 2. Anemic patient (unadjusted DLCO is falsely low 18.0 due to Hb 9.0 g/dL; correction elevates cDLCO)
    res_anemia = client.calculate_dlco(
        unadjusted_dlco_ml_min_mmhg=18.0,
        alveolar_volume_va_liters=5.5,
        hemoglobin_g_dl=9.0,
        predicted_dlco_ml_min_mmhg=28.0,
        predicted_kco=4.8,
        is_female=False
    )
    print("\n[Case 2: Anemia-Corrected DLCO]")
    print(json.dumps(res_anemia, indent=2))

    # 3. Severe interstitial lung disease / emphysema (cDLCO = 9.5 mL/min/mmHg -> < 40% predicted)
    res_severe = client.calculate_dlco(
        unadjusted_dlco_ml_min_mmhg=9.5,
        alveolar_volume_va_liters=3.5,
        hemoglobin_g_dl=14.0,
        predicted_dlco_ml_min_mmhg=28.0,
        predicted_kco=4.8,
        is_female=False
    )
    print("\n[Case 3: Severe Alveolar-Capillary Block]")
    print(json.dumps(res_severe, indent=2))

    # Assertions
    assert res_normal["percent_predicted_dlco"] >= 75.0
    assert res_anemia["hemoglobin_corrected_dlco"] > res_anemia["unadjusted_dlco_ml_min_mmhg"]
    assert res_severe["percent_predicted_dlco"] < 40.0
    print("\n[SUCCESS] Diffusing Capacity (DLCO) tests passed!")


if __name__ == "__main__":
    main()
