/// <reference types="vite/client" />
/// <reference types="@cloudflare/workers-types" />

import "react-router";

declare global {
  type Env = Record<string, never>;
}

declare module "react-router" {
  interface AppLoadContext {
    cloudflare: {
      env: Env;
      ctx: ExecutionContext;
    };
  }
}

declare module "*.css?url" {
  const url: string;
  export default url;
}
