import { serve } from "@hono/node-server";
import { Hono } from "hono";

const app = new Hono();

app.get("/health", (c) => c.json({ service: "api", status: "ok" }));

app.get("/api/todos", (c) => c.json({ items: [] }));

const port = Number(process.env.PORT ?? 8787);
const hostname = process.env.HOST ?? "127.0.0.1";

serve({
  fetch: app.fetch,
  hostname,
  port,
});

console.log(`API listening on http://${hostname}:${port}`);
