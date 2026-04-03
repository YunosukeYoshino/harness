import { cn } from "@repo/shared";
import type { ReactNode } from "react";

export function AppShell(props: { children: ReactNode; className?: string }) {
  return (
    <main
      className={cn(
        "mx-auto flex min-h-screen max-w-5xl flex-col gap-8 px-6 py-16",
        props.className,
      )}
    >
      {props.children}
    </main>
  );
}
