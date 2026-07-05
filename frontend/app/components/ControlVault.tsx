"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { createPatient } from "@/app/lib/api";
import { formatDate } from "@/app/lib/format";
import type { Patient } from "@/app/lib/types";
import { Badge } from "@/app/components/ui/Badge";
import { Button } from "@/app/components/ui/Button";
import { Card } from "@/app/components/ui/Card";
import { CommandBar } from "@/app/components/ui/CommandBar";
import { SignOutButton } from "@/app/components/auth/SignOutButton";

interface ControlVaultProps {
  initialPatients: Patient[];
  backendOnline: boolean;
  dataUnavailableMessage?: string | null;
}

const demoLaneByMrn: Record<
  string,
  { lane: string; title: string; summary: string }
> = {
  "MO-4471": {
    lane: "PGx pain safety",
    title: "CYP2D6 prodrug failure + sulfonamide allergy",
    summary: "Avoids codeine, tramadol, and celecoxib; builds a non-opioid regimen.",
  },
  "DR-2210": {
    lane: "Dose genetics",
    title: "TPMT poor metabolizer",
    summary: "Converts a dangerous standard thiopurine plan into a micro-dose workflow.",
  },
  "AK-9982": {
    lane: "Anticoagulation",
    title: "CYP2C9 + VKORC1 warfarin sensitivity",
    summary: "Connects two genes to safer stroke-prevention dosing and monitoring.",
  },
  "LM-7788": {
    lane: "Custom Rx",
    title: "MFSD8 CLN7 splice defect",
    summary: "Designs a splice-switching ASO path for an n-of-1 Batten disease case.",
  },
};

export function ControlVault({
  initialPatients,
  backendOnline,
  dataUnavailableMessage,
}: ControlVaultProps) {
  const router = useRouter();
  const [patients, setPatients] = useState(initialPatients);
  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [dob, setDob] = useState("");
  const [mrn, setMrn] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);

  const filtered = useMemo(
    () =>
      patients.filter(
        (p) =>
          p.name.toLowerCase().includes(search.toLowerCase()) ||
          (p.mrn ?? "").toLowerCase().includes(search.toLowerCase()),
      ),
    [patients, search],
  );

  const recent = useMemo(
    () =>
      [...patients]
        .sort(
          (a, b) =>
            new Date(b.created_at ?? 0).getTime() -
            new Date(a.created_at ?? 0).getTime(),
        )
        .slice(0, 5),
    [patients],
  );
  const canEditPatients = backendOnline && !dataUnavailableMessage;

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !canEditPatients) return;
    setCreating(true);
    setError(null);
    try {
      const patient = await createPatient({
        name: name.trim(),
        dob: dob || null,
        mrn: mrn || null,
      });
      setPatients((prev) => [patient, ...prev]);
      router.push(`/patients/${patient.id}/intake`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create patient");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="theme-clinical min-h-screen bg-bg">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col gap-6 p-6">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="micro-label text-accent">TheraGraph AI</p>
          <h1 className="text-xl font-medium">Control Vault</h1>
        </div>
        <div className="flex items-center gap-3">
          <SignOutButton />
          <CommandBar
            patients={patients}
            onNewPatient={canEditPatients ? () => setShowForm(true) : undefined}
          />
        </div>
      </header>

      {!backendOnline && (
        <Card className="border-danger/30 bg-danger/5 text-sm text-danger">
          Backend offline — start FastAPI on port 8000 to load patients.
        </Card>
      )}
      {backendOnline && dataUnavailableMessage && (
        <Card className="border-amber-300 bg-amber-50 text-sm text-amber-900">
          Patient data is not available yet. Add{" "}
          <code className="rounded bg-amber-100 px-1">SUPABASE_URL</code> and{" "}
          <code className="rounded bg-amber-100 px-1">SUPABASE_KEY</code> to{" "}
          <code className="rounded bg-amber-100 px-1">backend/.env</code>, then
          restart FastAPI.
        </Card>
      )}

      <div className="grid flex-1 gap-6 lg:grid-cols-2">
        <Card className="flex flex-col">
          <div className="mb-4 flex items-center justify-between gap-2">
            <p className="micro-label text-text-secondary">Patients</p>
            <Button
              variant="secondary"
              disabled={!canEditPatients}
              onClick={() => setShowForm((v) => !v)}
            >
              New Patient
            </Button>
          </div>
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by name or MRN…"
            className="mb-4 rounded border border-border bg-bg px-3 py-2 text-sm outline-none focus:border-accent/50"
          />
          <ul className="flex-1 space-y-1 overflow-y-auto">
            {filtered.length === 0 ? (
              <li className="py-8 text-center text-sm text-text-secondary">
                {dataUnavailableMessage
                  ? "Connect Supabase to load seeded demo patients."
                  : patients.length === 0
                  ? "No patients yet. Create one to begin intake."
                  : "No matches."}
              </li>
            ) : (
              filtered.map((p) => (
                <li key={p.id} className="border-b border-border/60 last:border-0">
                  <Link
                    href={`/patients/${p.id}/intake`}
                    className="block rounded px-3 py-3 transition-colors hover:bg-bg"
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <div className="flex flex-wrap items-center gap-2">
                          <p className="font-medium">{p.name}</p>
                          {p.mrn && demoLaneByMrn[p.mrn] && (
                            <Badge tone="accent">{demoLaneByMrn[p.mrn].lane}</Badge>
                          )}
                        </div>
                        {p.mrn && (
                          <p className="mt-0.5 text-xs text-text-secondary">{p.mrn}</p>
                        )}
                      </div>
                      <Badge tone="accent">Open</Badge>
                    </div>
                    {p.mrn && demoLaneByMrn[p.mrn] && (
                      <div className="mt-3 rounded border border-border/60 bg-bg/70 px-3 py-2">
                        <p className="text-sm font-medium">
                          {demoLaneByMrn[p.mrn].title}
                        </p>
                        <p className="mt-1 text-xs leading-relaxed text-text-secondary">
                          {demoLaneByMrn[p.mrn].summary}
                        </p>
                      </div>
                    )}
                    {p.mrn && !demoLaneByMrn[p.mrn] && (
                      <p className="mt-2 text-xs text-text-secondary">
                        Standard patient workspace
                      </p>
                    )}
                  </Link>
                </li>
              ))
            )}
          </ul>
        </Card>

        <Card>
          <p className="micro-label text-text-secondary">Recent Activity</p>
          {recent.length === 0 ? (
            <div className="mt-8 text-center">
              <p className="text-sm text-text-secondary">
                {dataUnavailableMessage
                  ? "Connect Supabase to restore patient history and seeded demo records."
                  : "Upload genomic data to build a per-patient Cognee memory graph."}
              </p>
              <Button
                className="mt-4"
                disabled={!canEditPatients}
                onClick={() => setShowForm(true)}
              >
                Create first patient
              </Button>
            </div>
          ) : (
            <ul className="mt-4 space-y-3">
              {recent.map((p) => (
                <li
                  key={p.id}
                  className="border-b border-border/50 pb-3 text-sm last:border-0"
                >
                  <div className="flex items-center justify-between gap-3">
                    <span className="font-medium">{p.name}</span>
                    <time className="text-xs text-text-secondary">
                      {formatDate(p.created_at)}
                    </time>
                  </div>
                  {p.mrn && demoLaneByMrn[p.mrn] && (
                    <p className="mt-1 text-xs text-text-secondary">
                      {demoLaneByMrn[p.mrn].title}
                    </p>
                  )}
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>

      {showForm && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4 backdrop-blur-sm"
          onClick={() => setShowForm(false)}
        >
          <Card
            className="w-full max-w-md"
            onClick={(e) => e.stopPropagation()}
          >
            <p className="micro-label text-text-secondary">New Patient</p>
            <form onSubmit={(e) => void handleCreate(e)} className="mt-4 space-y-3">
              <label className="block text-sm">
                <span className="micro-label text-text-secondary">Name</span>
                <input
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="mt-1 w-full rounded border border-border bg-bg px-3 py-2 outline-none focus:border-accent/50"
                />
              </label>
              <label className="block text-sm">
                <span className="micro-label text-text-secondary">DOB</span>
                <input
                  type="date"
                  value={dob}
                  onChange={(e) => setDob(e.target.value)}
                  className="mt-1 w-full rounded border border-border bg-bg px-3 py-2 outline-none focus:border-accent/50"
                />
              </label>
              <label className="block text-sm">
                <span className="micro-label text-text-secondary">MRN</span>
                <input
                  value={mrn}
                  onChange={(e) => setMrn(e.target.value)}
                  className="mt-1 w-full rounded border border-border bg-bg px-3 py-2 outline-none focus:border-accent/50"
                />
              </label>
              {error && <p className="text-xs text-danger">{error}</p>}
              <div className="flex gap-2 pt-2">
                <Button type="submit" disabled={creating}>
                  {creating ? "Creating…" : "Create & Intake"}
                </Button>
                <Button
                  type="button"
                  variant="ghost"
                  onClick={() => setShowForm(false)}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </Card>
        </div>
      )}
      </div>
    </div>
  );
}
