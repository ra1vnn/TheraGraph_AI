import Link from "next/link";
import { DnaHelix } from "./DnaHelix";

export function Hero() {
  return (
    <section className="relative flex min-h-screen items-center justify-center overflow-hidden bg-bg px-6">
      <DnaHelix />

      {/* Readability vignette so the headline sits cleanly over the helix. */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse 58% 48% at 50% 48%, rgba(9,9,11,0.9) 0%, rgba(9,9,11,0.54) 54%, rgba(9,9,11,0.12) 100%)",
        }}
      />

      <div className="relative z-10 mx-auto flex max-w-3xl flex-col items-center text-center">
        <p className="micro-label mb-8 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-text-secondary backdrop-blur-sm">
          <span className="h-1.5 w-1.5 rounded-full bg-accent" />
          Clinical memory graph · powered by Cognee
        </p>

        <h1 className="text-balance text-5xl font-semibold tracking-tight text-text drop-shadow-[0_2px_30px_rgba(0,0,0,0.95)] sm:text-6xl lg:text-7xl">
          Medical AI that never
          <br />
          <span className="text-white/[0.72]">forgets a patient</span>
        </h1>

        <p className="mx-auto mt-6 max-w-xl text-base leading-relaxed text-text-secondary drop-shadow-[0_2px_18px_rgba(0,0,0,0.9)] sm:text-lg">
          A permanent, evolving memory for personalized medicine — genome to
          therapy, remembered across every visit.
        </p>

        <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row">
          <Link
            href="/signup"
            className="rounded-md bg-white px-6 py-3 text-sm font-medium text-bg transition-transform hover:-translate-y-0.5"
          >
            Get started
          </Link>
          <Link
            href="/login"
            className="rounded-md border border-white/20 bg-white/[0.08] px-6 py-3 text-sm font-medium text-text backdrop-blur-sm transition-colors hover:border-white/[0.45] hover:bg-white/[0.12]"
          >
            Sign in
          </Link>
        </div>

        <p className="mt-6 text-xs text-text-secondary/70">
          Live demo · <span className="text-text-secondary">demo@gmail.com</span>{" "}
          / <span className="text-text-secondary">Demo123</span>
        </p>
      </div>

      <div
        aria-hidden
        className="pointer-events-none absolute bottom-8 left-1/2 z-10 -translate-x-1/2 text-text-secondary/50"
      >
        <span className="text-xs tracking-widest">SCROLL</span>
      </div>
    </section>
  );
}
