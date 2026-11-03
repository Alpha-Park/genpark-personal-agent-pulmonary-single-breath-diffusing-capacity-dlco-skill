"""
MCP Server for Single-Breath Diffusing Capacity (DLCO) Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import SingleBreathDiffusingCapacityClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-pulmonary-single-breath-diffusing-capacity-dlco-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "calculate_dlco",
                        "description": "Calculate unadjusted and hemoglobin-corrected DLCO, Krogh factor KCO, and percent predicted diffusing capacity.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "unadjusted_dlco_ml_min_mmhg": {"type": "number", "description": "Measured DLCO (mL/min/mmHg)."},
                                "alveolar_volume_va_liters": {"type": "number", "description": "Alveolar volume VA in liters."},
                                "hemoglobin_g_dl": {"type": "number", "description": "Blood hemoglobin in g/dL (default: 14.5)."},
                                "predicted_dlco_ml_min_mmhg": {"type": "number", "description": "Predicted DLCO (default: 28.0)."},
                                "predicted_kco": {"type": "number", "description": "Predicted KCO (default: 4.8)."},
                                "is_female": {"type": "boolean", "description": "Whether subject is female (default: false)."}
                            },
                            "required": ["unadjusted_dlco_ml_min_mmhg", "alveolar_volume_va_liters"]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "calculate_dlco":
            client = SingleBreathDiffusingCapacityClient()
            try:
                res = client.calculate_dlco(
                    unadjusted_dlco_ml_min_mmhg=float(args["unadjusted_dlco_ml_min_mmhg"]),
                    alveolar_volume_va_liters=float(args["alveolar_volume_va_liters"]),
                    hemoglobin_g_dl=float(args.get("hemoglobin_g_dl", 14.5)),
                    predicted_dlco_ml_min_mmhg=float(args.get("predicted_dlco_ml_min_mmhg", 28.0)),
                    predicted_kco=float(args.get("predicted_kco", 4.8)),
                    is_female=bool(args.get("is_female", False))
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
