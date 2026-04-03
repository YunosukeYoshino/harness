import type { ReactNode } from "react";

export function StatusCard(props: { title: string; children: ReactNode }) {
  return (
    <article className="rounded-2xl border border-neutral-800 bg-neutral-900/60 p-5">
      <h2 className="text-sm font-medium text-neutral-200">{props.title}</h2>
      <div className="mt-2 text-sm text-neutral-400">{props.children}</div>
    </article>
  );
}
