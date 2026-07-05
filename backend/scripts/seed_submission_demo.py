from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

import httpx


API_BASE = "http://localhost:8000"
SEED_MARKER = "SUBMISSION_DEMO_2026_07_05"


@dataclass(frozen=True)
class DemoPatient:
    name: str
    dob: str
    mrn: str
    dossier_filename: str
    dossier: str
    observations: tuple[str, ...]


PATIENTS: tuple[DemoPatient, ...] = (
    DemoPatient(
        name="Maya Okafor",
        dob="1991-03-14",
        mrn="MO-4471",
        dossier_filename="submission_maya_okafor_integrated_pgx_dossier.txt",
        dossier=f"""
{SEED_MARKER}
THERAGRAPH SUBMISSION DOSSIER - MAYA OKAFOR

Clinical demo lane:
  The painful prescribing failure case. The patient has rheumatoid arthritis and chronic
  inflammatory pain, but her graph explains why common opioid prodrugs do not work and why one
  familiar NSAID option is unsafe.

Patient:
  Name: Maya Okafor
  DOB: 1991-03-14
  MRN: MO-4471
  Primary condition: Seropositive rheumatoid arthritis with chronic inflammatory hand, wrist,
    and knee pain.
  Functional goal: Return to graphic-design work with better hand dexterity and no sedating
    ineffective opioid exposure.

Genomic and allergy evidence:
  GENE=CYP2D6 DIPLOTYPE=*4/*4 PHENOTYPE=Poor Metabolizer ACTIVITY_SCORE=0.0.
  CYP2D6 poor metabolizer implication: codeine and tramadol are prodrugs that require CYP2D6
    activation. In this patient, they produce poor analgesia and parent-drug side effects.
  GENE=COMT rs4680=Val/Val PHENOTYPE=High COMT activity. Evidence is emerging only, so it should
    be displayed as low-actionability context rather than a hard contraindication.
  Allergy: sulfonamide hypersensitivity after trimethoprim-sulfamethoxazole with rash and
    urticaria.
  Celecoxib contains a sulfonamide moiety and should be avoided for this prototype due to the
    documented sulfonamide allergy.

Prior therapy evidence:
  Codeine 30 mg q6h in 2024: no meaningful analgesia, nausea, dizziness. This is consistent with
    CYP2D6 poor metabolizer status.
  Ibuprofen 600 mg TID: partial relief, no GI bleed.
  Naproxen 500 mg BID: strong anti-inflammatory response, stopped because of insurance gap.
  No aspirin allergy. Baseline hepatic and renal function adequate for acetaminophen plus NSAID.

Most useful demo query:
  "Formulate chronic inflammatory pain."

Expected TheraGraph behavior:
  Recall should surface CYP2D6 poor metabolizer, codeine/tramadol non-response, sulfonamide
  allergy, and celecoxib avoidance.
  Formulation should exclude codeine, tramadol, and celecoxib; use real named generics such as
  acetaminophen and naproxen; show CPIC Level A evidence for CYP2D6/codeine; show allergy label
  evidence for sulfonamide/celecoxib; explain why the choice is not generic RAG but graph-linked
  causal prescribing.

Presentation sound bite:
  "TheraGraph remembered the failure mode: gene -> enzyme phenotype -> prodrug activation ->
  medication exclusion. The patient is not just a PDF in a vector index; her risk chain survives
  across visits."
""".strip(),
        observations=(
            f"{SEED_MARKER} Maya week-2 outcome: pain improved from 8/10 to 4/10 on the non-opioid plan; no nausea, no sedation, no urticaria. Continue avoiding codeine and tramadol.",
            f"{SEED_MARKER} Maya week-4 update: morning stiffness down from 70 minutes to 25 minutes; mild dyspepsia after naproxen, so add gastroprotection and keep renal/BP monitoring.",
        ),
    ),
    DemoPatient(
        name="Daniel Reyes",
        dob="1985-08-02",
        mrn="DR-2210",
        dossier_filename="submission_daniel_reyes_thiopurine_safety_dossier.txt",
        dossier=f"""
{SEED_MARKER}
THERAGRAPH SUBMISSION DOSSIER - DANIEL REYES

Clinical demo lane:
  The dose is the product. Daniel looks like a routine Crohn's disease immunomodulation case until
  the graph remembers TPMT poor metabolism and blocks a dangerous standard thiopurine dose.

Patient:
  Name: Daniel Reyes
  DOB: 1985-08-02
  MRN: DR-2210
  Primary condition: Crohn's disease, ileocolonic, moderate activity, steroid-dependent flares.
  Treatment goal: Oral immunomodulation with thiopurine-class therapy if pharmacogenomically safe.

Genomic evidence:
  GENE=TPMT DIPLOTYPE=*3A/*3A PHENOTYPE=Poor Metabolizer ACTIVITY=about 10 percent of normal.
  GENE=NUDT15 DIPLOTYPE=*1/*1 PHENOTYPE=Normal.
  TPMT poor metabolizer implication: azathioprine, mercaptopurine, and thioguanine metabolites can
    accumulate to toxic 6-TGN levels at standard dosing, causing severe myelosuppression.
  CPIC actionability: Level A prescribing action. Start about 10 percent of standard thiopurine
    target if used at all, and monitor CBC closely.

Clinical baseline:
  Baseline CBC: WBC 6.2 K/uL, hemoglobin 13.8 g/dL, platelets 245 K/uL.
  Baseline LFTs: ALT 28 U/L, albumin 3.9 g/dL.
  Fecal calprotectin: 420 mcg/g.
  Allergies: NKDA.

Most useful demo query:
  "Formulate Crohn's disease immunomodulation."

Expected TheraGraph behavior:
  Recall should surface TPMT *3A/*3A, poor metabolizer status, and the myelosuppression risk.
  Formulation can include azathioprine only at about 10 percent of standard with explicit CBC/LFT
  monitoring and a CPIC Level A risk card. Standard-dose azathioprine should be framed as unsafe.

Presentation sound bite:
  "This is where memory is more than recall. The same drug appears, but the dose changes because
  the graph preserved the genotype-to-toxicity relationship."
""".strip(),
        observations=(
            f"{SEED_MARKER} Daniel week-1 outcome: azathioprine micro-dose tolerated; WBC 5.9 K/uL, platelets 236 K/uL, ALT 31 U/L. Continue weekly CBC during titration.",
            f"{SEED_MARKER} Daniel week-3 outcome: mild leukopenia trend, WBC 4.1 K/uL. Hold further dose escalation; maintain 10 percent TPMT-adjusted dose and repeat CBC in 7 days.",
        ),
    ),
    DemoPatient(
        name="Aisha Karim",
        dob="1978-11-30",
        mrn="AK-9982",
        dossier_filename="submission_aisha_karim_anticoagulation_dossier.txt",
        dossier=f"""
{SEED_MARKER}
THERAGRAPH SUBMISSION DOSSIER - AISHA KARIM

Clinical demo lane:
  Anticoagulation selection where the graph connects two genes to one dose decision.

Patient:
  Name: Aisha Karim
  DOB: 1978-11-30
  MRN: AK-9982
  Primary condition: Persistent non-valvular atrial fibrillation.
  Stroke risk: CHA2DS2-VASc 4.
  Renal function: eGFR 72 mL/min; no mechanical valve.

Genomic evidence:
  GENE=CYP2C9 DIPLOTYPE=*2/*3 PHENOTYPE=Poor Metabolizer ACTIVITY=about 30 percent of normal.
  GENE=VKORC1 rs9923231=AA PHENOTYPE=High warfarin sensitivity.
  GENE=CYP4F2 rs2108622=*1/*3 PHENOTYPE=Slightly reduced vitamin K metabolism.
  Combined implication: standard warfarin 5 mg initiation risks supratherapeutic INR and bleeding;
    genotype-guided starting dose is roughly 2 mg/day with early INR checks, or consider a DOAC
    such as apixaban when clinically appropriate.

Clinical context:
  No severe renal impairment.
  No prior intracranial hemorrhage.
  Prior rivaroxaban stopped because of bruising, not because of a genotype contraindication.
  Current meds: lisinopril and metformin.

Most useful demo query:
  "Formulate atrial fibrillation anticoagulation."

Expected TheraGraph behavior:
  Recall should surface CYP2C9 poor metabolism and VKORC1 AA sensitivity.
  Formulation should reduce warfarin dose if warfarin is chosen, flag bleeding risk, discuss
  apixaban as CYP2C9/VKORC1-independent, and show INR monitoring logic.

Presentation sound bite:
  "The graph lets the agent see an interaction across genes, not just retrieve a paragraph about
  warfarin. CYP2C9 clearance plus VKORC1 sensitivity becomes a safer dose."
""".strip(),
        observations=(
            f"{SEED_MARKER} Aisha shared decision: patient prefers apixaban over genotype-guided warfarin after counseling; renal function supports fixed dosing.",
            f"{SEED_MARKER} Aisha follow-up: no bleeding, no neurologic symptoms, adherence good. Continue renal function checks and bleeding surveillance.",
        ),
    ),
    DemoPatient(
        name="Leo Martinez",
        dob="2021-05-09",
        mrn="LM-7788",
        dossier_filename="submission_leo_martinez_n_of_1_dossier.txt",
        dossier=f"""
{SEED_MARKER}
THERAGRAPH SUBMISSION DOSSIER - LEO MARTINEZ

Clinical demo lane:
  A true n-of-1 story. Leo is not a pharmacogenomic dosing case; he has a monogenic disease-causing
  splice defect where an individualized therapy design is plausible.

Patient:
  Name: Leo Martinez
  DOB: 2021-05-09
  MRN: LM-7788
  Primary disease: Neuronal ceroid lipofuscinosis type 7, CLN7 late-infantile Batten disease.
  Gene: MFSD8, also known as CLN7.
  Inheritance: Autosomal recessive, compound heterozygous.
  Target tissue: central nervous system, neurons.

Disease variant evidence:
  Allele 1: MFSD8 c.754+2T>A, canonical splice-donor loss, pathogenic null allele.
  Allele 2: MFSD8 c.863+2117A>G, deep-intronic variant that creates a cryptic splice site.
  Molecular consequence: cryptic pseudoexon inclusion of 87 nucleotides in MFSD8 mRNA, frameshift,
    premature stop, and loss of functional MFSD8 lysosomal membrane protein.
  Mechanism: loss-of-function through aberrant splicing.
  RNA evidence: patient-derived RNA confirms pseudoexon inclusion.

Clinical phenotype:
  Normal development until roughly 24 months.
  Progressive seizures, vision loss, language regression, ataxia, retinal degeneration, and MRI
  cerebral/cerebellar atrophy.
  Current meds: levetiracetam and valproate for seizure control only.
  No approved disease-modifying therapy for CLN7; CLN2 enzyme replacement does not apply because
  TPP1 enzyme testing is normal.

Most useful demo query:
  "Design an n-of-1 therapy to restore MFSD8 splicing and slow CLN7 neurodegeneration."

Expected TheraGraph behavior:
  Custom Rx should identify MFSD8, the deep-intronic c.863+2117A>G splice defect, CNS tissue, and
  splice-switching ASO as the best modality. It should present construct blocks, intrathecal
  delivery, safety risks, manufacturing steps, and the FDA plausible mechanism framework.

Presentation sound bite:
  "This is why Cognee matters. The patient story is not one note; it is a chain: variant -> RNA
  consequence -> disease mechanism -> modality -> delivery -> regulatory path."
""".strip(),
        observations=(
            f"{SEED_MARKER} Leo family meeting: goal is to preserve remaining vision and language; care team prioritizes intrathecal ASO feasibility and natural-history comparator data.",
            f"{SEED_MARKER} Leo lab update: fibroblast RNA assay confirms reduction of aberrant MFSD8 pseudoexon inclusion is the proposed target-engagement biomarker.",
        ),
    ),
)


def request_json(client: httpx.Client, method: str, path: str, **kwargs):
    response = client.request(method, f"{API_BASE}{path}", **kwargs)
    response.raise_for_status()
    return response.json()


def ensure_patient(client: httpx.Client, demo: DemoPatient) -> dict:
    patients = request_json(client, "GET", "/api/patients")
    for patient in patients:
        if patient["mrn"] == demo.mrn or patient["name"] == demo.name:
            return patient
    return request_json(
        client,
        "POST",
        "/api/patients",
        json={"name": demo.name, "dob": demo.dob, "mrn": demo.mrn},
    )


def already_seeded(client: httpx.Client, patient_id: str) -> bool:
    timeline = request_json(client, "GET", f"/api/patients/{patient_id}/timeline")
    return any(SEED_MARKER in entry.get("observation", "") for entry in timeline)


def ingest_dossier(client: httpx.Client, patient_id: str, demo: DemoPatient) -> None:
    files = {
        "files": (
            demo.dossier_filename,
            demo.dossier.encode("utf-8"),
            "text/plain",
        )
    }
    request_json(client, "POST", f"/api/patients/{patient_id}/ingest", files=files)


def add_observations(client: httpx.Client, patient_id: str, demo: DemoPatient) -> None:
    for observation in demo.observations:
        request_json(
            client,
            "POST",
            f"/api/patients/{patient_id}/feedback",
            json={"observation": observation},
        )


def verify_patient(client: httpx.Client, patient_id: str, name: str) -> None:
    graph = request_json(client, "GET", f"/api/patients/{patient_id}/graph")
    timeline = request_json(client, "GET", f"/api/patients/{patient_id}/timeline")
    print(
        f"verified {name}: graph_nodes={len(graph.get('nodes', []))} "
        f"graph_edges={len(graph.get('edges', []))} timeline={len(timeline)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-existing", action="store_true", default=True)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    with httpx.Client(timeout=240.0) as client:
        health = request_json(client, "GET", "/health")
        if health.get("status") != "ok":
            raise RuntimeError("backend health check failed")

        seeded_ids: list[tuple[str, str]] = []
        for demo in PATIENTS:
            patient = ensure_patient(client, demo)
            patient_id = patient["id"]
            if args.skip_existing and already_seeded(client, patient_id):
                print(f"skip {demo.name}: submission seed marker already present")
                seeded_ids.append((patient_id, demo.name))
                continue
            print(f"seed {demo.name}: ingesting dossier and outcome observations")
            ingest_dossier(client, patient_id, demo)
            add_observations(client, patient_id, demo)
            seeded_ids.append((patient_id, demo.name))

        if args.verify:
            for patient_id, name in seeded_ids:
                verify_patient(client, patient_id, name)

    print("submission demo seed complete")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except httpx.HTTPError as exc:
        print(f"seed failed: {exc}", file=sys.stderr)
        raise
