import { ControlVault } from "@/app/components/ControlVault";
import type { Patient } from "@/app/lib/types";

export default async function VaultPage() {
  let patients: Patient[] = [];
  let backendOnline = true;
  let dataUnavailableMessage: string | null = null;

  try {
    const base =
      process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ||
      "http://localhost:8000";
    const health = await fetch(`${base}/health`, {
      cache: "no-store",
    }).catch(() => null);
    backendOnline = health?.ok ?? false;
    if (backendOnline) {
      const patientResponse = await fetch(`${base}/api/patients`, {
        cache: "no-store",
      });
      if (patientResponse.ok) {
        patients = (await patientResponse.json()) as Patient[];
      } else {
        const detail = await patientResponse
          .json()
          .then((body: { detail?: string }) => body.detail)
          .catch(() => null);
        dataUnavailableMessage =
          detail ||
          `Patient store unavailable (${patientResponse.status}). Check Supabase configuration.`;
      }
    }
  } catch {
    backendOnline = false;
  }

  return (
    <ControlVault
      initialPatients={patients}
      backendOnline={backendOnline}
      dataUnavailableMessage={dataUnavailableMessage}
    />
  );
}
