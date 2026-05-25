#!/usr/bin/env node
/**
 * from-thesis-to-paper npm CLI — spawns `python -m fttp` for pipeline subcommands.
 * `doctor` runs locally: Python import, config discovery, key path checks.
 */

const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const CONFIG_NAMES = ["fttp.config.json", "workspace.config.json", "fttp.config.example.json"];
const PYTHON_SUBCOMMANDS = new Set([
  "tables",
  "evidence",
  "figures",
  "compile",
  "pipeline",
]);

function findRepoRoot(startDir) {
  let dir = path.resolve(startDir);
  for (let i = 0; i < 12; i += 1) {
    if (
      fs.existsSync(path.join(dir, "pyproject.toml")) &&
      fs.existsSync(path.join(dir, "python", "fttp"))
    ) {
      return dir;
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return path.resolve(startDir);
}

function resolvePython(repoRoot) {
  const fromEnv = process.env.FTTP_PYTHON?.trim();
  if (fromEnv) return fromEnv;

  const venvPython = path.join(repoRoot, ".venv", "bin", "python");
  if (fs.existsSync(venvPython)) return venvPython;

  const venvWin = path.join(repoRoot, ".venv", "Scripts", "python.exe");
  if (fs.existsSync(venvWin)) return venvWin;

  return process.env.PYTHON || "python3";
}

function resolveConfigPath(repoRoot, cwd) {
  const envPath = process.env.FTTP_CONFIG?.trim();
  if (envPath) {
    const abs = path.resolve(envPath);
    return fs.existsSync(abs) ? abs : null;
  }

  for (const dir of [cwd, repoRoot]) {
    for (const name of CONFIG_NAMES) {
      const candidate = path.join(dir, name);
      if (fs.existsSync(candidate)) return candidate;
    }
  }
  return null;
}

function loadConfigJson(configPath) {
  const raw = fs.readFileSync(configPath, "utf8");
  return JSON.parse(raw);
}

function validateConfigShape(cfg, configPath) {
  const errors = [];
  for (const key of ["workspaceName", "repoRoot", "paper"]) {
    if (!(key in cfg)) errors.push(`missing required field: ${key}`);
  }
  const paper = cfg.paper;
  if (paper && typeof paper === "object") {
    for (const field of ["dir", "mainTex"]) {
      if (!(field in paper)) errors.push(`missing paper.${field}`);
    }
  } else if (paper !== undefined) {
    errors.push("paper must be an object");
  }
  if (errors.length) {
    throw new Error(`${configPath}: ${errors.join("; ")}`);
  }
}

function checkPath(label, absPath, required = true) {
  const ok = fs.existsSync(absPath);
  if (ok) {
    console.log(`  ok  ${label}: ${absPath}`);
    return true;
  }
  const prefix = required ? "FAIL" : "warn";
  console.log(`  ${prefix}  ${label}: ${absPath} (not found)`);
  return !required;
}

function runPython(python, args, options = {}) {
  const repoRoot = options.repoRoot || process.cwd();
  const env = {
    ...process.env,
    PYTHONPATH: [
      path.join(repoRoot, "python"),
      process.env.PYTHONPATH || "",
    ]
      .filter(Boolean)
      .join(path.delimiter),
  };
  if (options.fttpConfig) {
    env.FTTP_CONFIG = options.fttpConfig;
  }
  return spawnSync(python, args, {
    cwd: options.cwd || repoRoot,
    env,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  });
}

function cmdDoctor(repoRoot) {
  const cwd = process.cwd();
  console.log("fttp doctor");
  console.log(`  repo root: ${repoRoot}`);

  const python = resolvePython(repoRoot);
  console.log(`  python:    ${python}`);

  const versionRun = runPython(
    python,
    ["-c", "import fttp; print(fttp.__version__)"],
    { repoRoot },
  );
  if (versionRun.status !== 0) {
    console.error("  FAIL  cannot import fttp package");
    if (versionRun.stderr) process.stderr.write(versionRun.stderr);
    if (versionRun.stdout) process.stdout.write(versionRun.stdout);
    console.error(
      "  hint: pip install -e . from repo root, or use .venv/bin/python",
    );
    return 1;
  }
  const version = (versionRun.stdout || "").trim();
  console.log(`  ok  fttp ${version}`);

  const configPath = resolveConfigPath(repoRoot, cwd);
  if (!configPath) {
    console.error(
      "  FAIL  no config found (fttp.config.json, workspace.config.json, or fttp.config.example.json)",
    );
    console.error(
      "  hint: copy fttp.config.example.json → fttp.config.json and set repoRoot",
    );
    return 1;
  }
  console.log(`  ok  config: ${configPath}`);

  let cfg;
  try {
    cfg = loadConfigJson(configPath);
    validateConfigShape(cfg, configPath);
  } catch (err) {
    console.error(`  FAIL  ${err.message}`);
    return 1;
  }

  const root = path.resolve(cfg.repoRoot);
  if (!fs.existsSync(root)) {
    console.error(`  FAIL  repoRoot does not exist: ${root}`);
    return 1;
  }
  console.log(`  ok  workspace: ${cfg.workspaceName}`);

  let allOk = true;
  const paperDir = path.join(root, cfg.paper.dir);
  const mainTex = path.join(paperDir, cfg.paper.mainTex);
  allOk = checkPath("paper.mainTex", mainTex) && allOk;
  allOk = checkPath("paper/main.pdf", `${mainTex.slice(0, -4)}.pdf`, false) && allOk;
  allOk = checkPath("paper/figures/", path.join(paperDir, "figures"), false) && allOk;

  const evidence = cfg.evidence || {};
  if (evidence.catalog) {
    allOk =
      checkPath("evidence.catalog", path.join(root, evidence.catalog)) && allOk;
  }
  if (evidence.lineageCsv) {
    allOk =
      checkPath("evidence.lineageCsv", path.join(root, evidence.lineageCsv)) &&
      allOk;
  }

  const style = path.join(root, "experimentos", "fixtures", "figure_style.json");
  allOk = checkPath("figure_style.json", style, false) && allOk;

  const readOnly = cfg.readOnlyRoots || [];
  for (const ro of readOnly) {
    checkPath("readOnlyRoot", path.resolve(ro), false);
  }

  if (!allOk) {
    console.error("  FAIL  one or more required paths are missing");
    return 1;
  }

  console.log("  doctor: all checks passed");
  return 0;
}

function cmdPythonSubcommand(command, repoRoot) {
  const python = resolvePython(repoRoot);
  const configPath = resolveConfigPath(repoRoot, process.cwd());
  const run = runPython(python, ["-m", "fttp", command], {
    repoRoot,
    cwd: repoRoot,
    fttpConfig: configPath || undefined,
  });
  if (run.stdout) process.stdout.write(run.stdout);
  if (run.stderr) process.stderr.write(run.stderr);
  return run.status ?? 1;
}

function printUsage() {
  console.log(`Usage: fttp <command>

Commands:
  doctor     Check Python fttp, config, and key workspace paths
  tables     Export LaTeX table fragments (python -m fttp tables)
  evidence   Build evidence bundle stub (python -m fttp evidence)
  figures    Refresh figure assets stub (python -m fttp figures)
  compile    Verify paper PDF paths (python -m fttp compile)
  pipeline   Run tables → evidence → figures → compile (python -m fttp pipeline)

Environment:
  FTTP_PYTHON   Python executable (default: .venv/bin/python, then python3)
  FTTP_CONFIG   Absolute path to workspace JSON config
  PYTHON        Fallback Python if FTTP_PYTHON unset
`);
}

function main() {
  const argv = process.argv.slice(2);
  const command = argv[0];

  if (!command || command === "-h" || command === "--help") {
    printUsage();
    process.exit(command ? 0 : 1);
  }

  if (command === "--version" || command === "-V") {
    const pkg = require(path.join(__dirname, "..", "package.json"));
    console.log(`from-thesis-to-paper ${pkg.version}`);
    process.exit(0);
  }

  const repoRoot = findRepoRoot(process.cwd());

  if (command === "doctor") {
    process.exit(cmdDoctor(repoRoot));
  }

  if (PYTHON_SUBCOMMANDS.has(command)) {
    process.exit(cmdPythonSubcommand(command, repoRoot));
  }

  console.error(`Unknown command: ${command}`);
  printUsage();
  process.exit(1);
}

main();
