#!/usr/bin/env node
/**
 * Thin npm launcher for the canonical Python CLI.
 *
 * The Python package owns command parsing, configuration, validation and
 * diagnostics. This file only selects a compatible interpreter and streams
 * the complete argument vector and stdio to `python -m fttp`.
 */

const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

function sourceRepoRoot() {
  // Discover a source checkout from this wrapper's installation path. Never
  // infer a framework package from the consumer's current directory.
  let dir = path.resolve(__dirname);
  for (let i = 0; i < 5; i += 1) {
    if (
      fs.existsSync(path.join(dir, "pyproject.toml")) &&
      fs.existsSync(path.join(dir, "python", "fttp", "__main__.py"))
    ) {
      return dir;
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

function resolvePython(repoRoot) {
  const fromEnv = process.env.FTTP_PYTHON?.trim();
  if (fromEnv) return fromEnv;
  if (repoRoot) {
    const venvPython = path.join(repoRoot, ".venv", "bin", "python");
    if (fs.existsSync(venvPython)) return venvPython;
    const venvWin = path.join(repoRoot, ".venv", "Scripts", "python.exe");
    if (fs.existsSync(venvWin)) return venvWin;
  }
  return process.env.PYTHON?.trim() || "python3";
}

function inheritedEnvironment(repoRoot) {
  const env = { ...process.env };
  if (repoRoot) {
    const packageRoot = path.join(repoRoot, "python");
    env.PYTHONPATH = [packageRoot, process.env.PYTHONPATH || ""]
      .filter(Boolean)
      .join(path.delimiter);
  }
  return env;
}

function normalizeExit(code, signal) {
  if (typeof code === "number") return code >= 0 ? code : 1;
  if (signal) {
    const signals = { SIGINT: 2, SIGTERM: 15, SIGHUP: 1 };
    return 128 + (signals[signal] || 1);
  }
  return 1;
}

function main() {
  const argv = process.argv.slice(2);
  if (argv.length === 1 && (argv[0] === "--version" || argv[0] === "-V")) {
    const pkg = require(path.join(__dirname, "..", "package.json"));
    console.log(`from-thesis-to-paper ${pkg.version}`);
    return;
  }

  const repoRoot = sourceRepoRoot();
  const python = resolvePython(repoRoot);
  const child = spawn(python, ["-m", "fttp", ...argv], {
    cwd: process.cwd(),
    env: inheritedEnvironment(repoRoot),
    stdio: "inherit",
  });

  let forwarding = false;
  for (const signal of ["SIGINT", "SIGTERM", "SIGHUP"]) {
    process.on(signal, () => {
      forwarding = true;
      if (!child.killed) child.kill(signal);
    });
  }

  child.once("error", (error) => {
    if (forwarding) return;
    console.error(`fttp: cannot start ${python}: ${error.message}`);
    process.exitCode = 1;
  });
  child.once("close", (code, signal) => {
    process.exitCode = normalizeExit(code, signal);
  });
}

main();
