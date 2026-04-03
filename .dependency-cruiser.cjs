// @ts-check

/**
 * Architecture boundaries from config/architecture-boundaries.json
 *
 * Each key lists the packages it is allowed to import from.
 *   web:          [ui, shared, schema, domain]
 *   api:          [app, domain, shared, schema, data, integrations]
 *   domain:       [shared, schema]
 *   app:          [domain, shared, schema]
 *   data:         [domain, shared, schema]
 *   integrations: [domain, shared, schema]
 *   ui:           [shared, schema]
 *   shared:       []
 *   schema:       []
 */

const ALLOWED_DEPS = {
  web: ["ui", "shared", "schema", "domain"],
  api: ["app", "domain", "shared", "schema", "data", "integrations"],
  domain: ["shared", "schema"],
  app: ["domain", "shared", "schema"],
  data: ["domain", "shared", "schema"],
  integrations: ["domain", "shared", "schema"],
  ui: ["shared", "schema"],
  shared: [],
  schema: [],
};

const ALL_PACKAGES = Object.keys(ALLOWED_DEPS);

/**
 * Build forbidden rules that block imports from disallowed @repo/* packages.
 *
 * For each package we compute the set of @repo/* targets it must NOT reach,
 * then emit one rule per source package.
 */
function buildBoundaryRules() {
  const rules = [];

  for (const source of ALL_PACKAGES) {
    const allowed = new Set(ALLOWED_DEPS[source]);
    const forbidden = ALL_PACKAGES.filter(
      (pkg) => pkg !== source && !allowed.has(pkg),
    );

    if (forbidden.length === 0) {
      continue;
    }

    const sourceDir = ["web", "api"].includes(source)
      ? `apps/${source}`
      : `packages/${source}`;

    const forbiddenPattern = forbidden
      .map((pkg) => {
        const dir = ["web", "api"].includes(pkg)
          ? `apps/${pkg}`
          : `packages/${pkg}`;
        return dir;
      })
      .join("|");

    rules.push({
      name: `${source}-boundary`,
      comment: `${source} may only depend on: [${ALLOWED_DEPS[source].join(", ") || "(nothing)"}]`,
      severity: "error",
      from: { path: `^${sourceDir}/` },
      to: { path: `^(${forbiddenPattern})/` },
    });
  }

  return rules;
}

/** @type {import('dependency-cruiser').IConfiguration} */
module.exports = {
  forbidden: [
    // -- Circular dependency ban --
    {
      name: "no-circular",
      comment: "Circular dependencies are forbidden",
      severity: "error",
      from: {},
      to: { circular: true },
    },

    // -- Layer boundary rules derived from architecture-boundaries.json --
    ...buildBoundaryRules(),
  ],

  options: {
    doNotFollow: {
      path: "node_modules",
    },

    exclude: {
      path: "(dist|build|\\.react-router)/",
    },

    tsPreCompilationDeps: true,

    tsConfig: {
      fileName: "tsconfig.base.json",
    },

    enhancedResolveOptions: {
      exportsFields: ["exports"],
      conditionNames: ["import", "require", "node", "default"],
      mainFields: ["module", "main", "types", "typings"],
    },

    reporterOptions: {
      text: {
        highlightFocused: true,
      },
    },
  },
};
