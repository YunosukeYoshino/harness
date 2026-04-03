export default function Home() {
  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col gap-8 px-6 py-16">
      <header className="space-y-3">
        <p className="text-sm uppercase tracking-[0.2em] text-neutral-400">
          agent harness starter
        </p>
        <h1 className="text-4xl font-semibold tracking-tight">
          Agent Harness Starter
        </h1>
        <p className="max-w-2xl text-neutral-300">
          React Router v7 framework mode と Hono API を前提にした runtime-first
          テンプレートです。
        </p>
      </header>

      <section
        className="grid gap-4 md:grid-cols-3"
        aria-label="harness-status"
      >
        <article className="rounded-2xl border border-neutral-800 bg-neutral-900/60 p-5">
          <h2 className="text-sm font-medium text-neutral-200">Runtime gate</h2>
          <p className="mt-2 text-sm text-neutral-400">
            `pnpm check` は static checks に加えて runtime smoke と Playwright
            smoke を通します。
          </p>
        </article>
        <article className="rounded-2xl border border-neutral-800 bg-neutral-900/60 p-5">
          <h2 className="text-sm font-medium text-neutral-200">
            Work artifacts
          </h2>
          <p className="mt-2 text-sm text-neutral-400">
            plan / sprint / review / QA / progress / handoff は `work/`
            に集約します。
          </p>
        </article>
        <article className="rounded-2xl border border-neutral-800 bg-neutral-900/60 p-5">
          <h2 className="text-sm font-medium text-neutral-200">PR review</h2>
          <p className="mt-2 text-sm text-neutral-400">
            人間 review の代わりに Codex PR review を completion gate にします。
          </p>
        </article>
      </section>

      <section className="rounded-2xl border border-neutral-800 bg-neutral-900/40 p-6">
        <h2 className="text-lg font-medium">Next step</h2>
        <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm text-neutral-300">
          <li>`pnpm new:work-item todo-app` で artifact を作成する</li>
          <li>
            `bash tools/install-upstream-skills.sh` で必要な skills を追加する
          </li>
          <li>`pnpm check` で runtime gate を確認する</li>
        </ol>
      </section>
    </main>
  );
}
