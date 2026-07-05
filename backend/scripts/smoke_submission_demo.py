from __future__ import annotations

import httpx


API_BASE = "http://localhost:8000"


DEMO_CALLS = {
    "Maya Okafor": ("formulate", "chronic inflammatory pain"),
    "Daniel Reyes": ("formulate", "Crohn's disease immunomodulation"),
    "Aisha Karim": ("formulate", "atrial fibrillation anticoagulation"),
    "Leo Martinez": (
        "custom",
        "restore MFSD8 splicing and slow CLN7 neurodegeneration",
    ),
}


def request_json(client: httpx.Client, method: str, path: str, **kwargs):
    response = client.request(method, f"{API_BASE}{path}", **kwargs)
    response.raise_for_status()
    return response.json()


def main() -> int:
    with httpx.Client(timeout=240.0) as client:
        health = request_json(client, "GET", "/health")
        print(f"health={health.get('status')}")

        patients = request_json(client, "GET", "/api/patients")
        by_name = {patient["name"]: patient for patient in patients}
        print(f"patients={len(patients)}")

        for name, (kind, prompt) in DEMO_CALLS.items():
            patient = by_name[name]
            patient_id = patient["id"]
            graph = request_json(client, "GET", f"/api/patients/{patient_id}/graph")
            timeline = request_json(
                client,
                "GET",
                f"/api/patients/{patient_id}/timeline",
            )
            print(
                f"{name}: graph_nodes={len(graph.get('nodes', []))} "
                f"graph_edges={len(graph.get('edges', []))} timeline={len(timeline)}"
            )

            if kind == "formulate":
                payload = request_json(
                    client,
                    "POST",
                    f"/api/patients/{patient_id}/formulate",
                    json={"indication": prompt},
                )
                risks = ", ".join(r["gene"] for r in payload.get("genetic_risks", []))
                modules = ", ".join(m["ingredient"] for m in payload.get("modules", []))
                print(
                    f"  formulation={payload['formulation_id']} "
                    f"modules=[{modules}] risks=[{risks}] "
                    f"contra={payload.get('contraindications_flagged', [])}"
                )
            else:
                payload = request_json(
                    client,
                    "POST",
                    f"/api/patients/{patient_id}/custom-therapy",
                    json={"goal": prompt, "target_hint": "MFSD8 CLN7 splice defect"},
                )
                target = payload.get("target", {})
                print(
                    f"  custom={payload['design_id']} target={target.get('gene')} "
                    f"modality={payload.get('modality_name')} "
                    f"criteria={len(payload.get('regulatory_criteria', []))}"
                )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
