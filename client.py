"""
Pulmonary Single-Breath Diffusing Capacity of the Lung for Carbon Monoxide (DLCO) Client.
Zero-mock pure Python standard library implementation.
Calculates unadjusted DLCO, hemoglobin-corrected DLCO (cDLCO), alveolar volume (VA),
and the Krogh transfer coefficient (KCO = DLCO / VA) based on ATS/ERS standardization.
"""

import math
from typing import Dict, Any, Optional


class SingleBreathDiffusingCapacityClient:
    """
    Computes diffusing capacity of the lung for carbon monoxide (DLCO in mL/min/mmHg)
    and Krogh transfer coefficient (KCO) using the single-breath Jones-Meade timing technique.
    """

    def __init__(self):
        pass

    def calculate_dlco(
        self,
        unadjusted_dlco_ml_min_mmhg: float,
        alveolar_volume_va_liters: float,
        hemoglobin_g_dl: Optional[float] = 14.5,
        predicted_dlco_ml_min_mmhg: Optional[float] = 28.0,
        predicted_kco: Optional[float] = 4.8,
        is_female: bool = False
    ) -> Dict[str, Any]:
        """
        Calculates hemoglobin-adjusted DLCO, KCO, and percent predicted metrics.
        unadjusted_dlco_ml_min_mmhg: Measured DLCO (mL CO / min / mmHg).
        alveolar_volume_va_liters: Alveolar volume measured via tracer gas dilution (L BTPS).
        hemoglobin_g_dl: Blood hemoglobin concentration in g/dL (default: 14.5 for male, 13.4 for female).
        predicted_dlco_ml_min_mmhg: Reference predicted DLCO.
        predicted_kco: Reference predicted KCO (DLCO / VA).
        is_female: Subject biological sex for ATS/ERS hemoglobin correction formula.
        """
        if unadjusted_dlco_ml_min_mmhg <= 0 or alveolar_volume_va_liters <= 0:
            raise ValueError("DLCO and Alveolar Volume must be strictly positive.")

        # Krogh transfer factor: KCO = DLCO / VA
        kco = unadjusted_dlco_ml_min_mmhg / alveolar_volume_va_liters

        # ATS/ERS Standard Hemoglobin Correction Formula (Cotes / Dinakara):
        # For adolescent/adult males: DLCO_adj = DLCO_meas * (10.22 + Hb) / (1.7 * Hb)
        # For females: DLCO_adj = DLCO_meas * (9.38 + Hb) / (1.7 * Hb)
        corrected_dlco = unadjusted_dlco_ml_min_mmhg
        hb_factor = 1.0

        if hemoglobin_g_dl is not None and hemoglobin_g_dl > 0:
            if is_female:
                hb_factor = (9.38 + hemoglobin_g_dl) / (1.7 * hemoglobin_g_dl)
            else:
                hb_factor = (10.22 + hemoglobin_g_dl) / (1.7 * hemoglobin_g_dl)
            corrected_dlco = unadjusted_dlco_ml_min_mmhg * hb_factor

        # Percent predicted calculations
        pct_pred_dlco = None
        if predicted_dlco_ml_min_mmhg and predicted_dlco_ml_min_mmhg > 0:
            pct_pred_dlco = (corrected_dlco / predicted_dlco_ml_min_mmhg) * 100.0

        pct_pred_kco = None
        if predicted_kco and predicted_kco > 0:
            pct_pred_kco = (kco / predicted_kco) * 100.0

        # Clinical evaluation:
        # Normal DLCO: >= 75 - 80% predicted
        # Mild gas exchange impairment: 60 - 79% predicted
        # Moderate impairment: 40 - 59% predicted
        # Severe alveolar-capillary block / pulmonary fibrosis / emphysema: < 40% predicted
        #
        # Discrepancy pattern between DLCO and KCO:
        # Reduced DLCO with Normal KCO -> Loss of lung volume (pneumonectomy, kyphoscoliosis, chest wall restriction).
        # Reduced DLCO with Low KCO -> Primary alveolar-capillary destruction (idiopathic pulmonary fibrosis, emphysema, pulmonary hypertension).
        target_pct = pct_pred_dlco if pct_pred_dlco is not None else 100.0

        if target_pct >= 75.0:
            classification = "Normal Alveolar-Capillary Diffusing Capacity"
            gas_exchange_status = "Intact alveolar-capillary membrane conductance and pulmonary capillary blood volume."
            impairment_severity = "None / Preserved"
        elif target_pct >= 60.0:
            classification = "Mild Alveolar-Capillary Diffusion Impairment"
            gas_exchange_status = "Subclinical diffusion limitation; early microvascular remodeling or mild interstitial expansion."
            impairment_severity = "Mild"
        elif target_pct >= 40.0:
            classification = "Moderate Alveolar Gas Exchange Impairment"
            gas_exchange_status = "Substantial reduction in effective gas transfer surface area or capillary transit time."
            impairment_severity = "Moderate"
        else:
            classification = "Severe Alveolar-Capillary Membrane Block / Emphysema"
            gas_exchange_status = "Critical reduction in functional diffusing capacity; marked exertional desaturation expected."
            impairment_severity = "Severe"

        return {
            "status": "success",
            "unadjusted_dlco_ml_min_mmhg": round(unadjusted_dlco_ml_min_mmhg, 2),
            "hemoglobin_corrected_dlco": round(corrected_dlco, 2),
            "alveolar_volume_va_liters": round(alveolar_volume_va_liters, 2),
            "krogh_transfer_coefficient_kco": round(kco, 2),
            "percent_predicted_dlco": round(pct_pred_dlco, 1) if pct_pred_dlco is not None else None,
            "percent_predicted_kco": round(pct_pred_kco, 1) if pct_pred_kco is not None else None,
            "hemoglobin_correction_factor": round(hb_factor, 3),
            "evaluation": {
                "classification": classification,
                "impairment_severity": impairment_severity,
                "gas_exchange_status": gas_exchange_status
            }
        }
