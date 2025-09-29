/*
 * Tokenization tests for SQF.tmLanguage using vscode-textmate + vscode-oniguruma.
 * - Compatible with Node ESM + CommonJS packages via createRequire.
 * - No named ESM imports from CJS modules.
 * - No `await` inside onigLib factory functions.
 */

import assert from "node:assert/strict";
import { test } from "node:test";
import fs from "node:fs/promises";
import path from "node:path";
import plist from "plist";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);

// Load vscode-textmate (CJS on some installs) via require
const vsctm = require("vscode-textmate");
// Extract Registry & INITIAL from the CJS object
const { Registry, INITIAL } = vsctm;

// Load vscode-oniguruma (CJS) via dynamic import then normalize
async function initOnigLib() {
  const wasmPath = path.resolve(
    process.cwd(),
    "node_modules",
    "vscode-oniguruma",
    "release",
    "onig.wasm"
  );
  const wasmBin = await fs.readFile(wasmPath);

  const onigMod = await import("vscode-oniguruma");
  const onig = onigMod.default ?? onigMod;
  const { loadWASM, OnigScanner, OnigString } = onig;

  await loadWASM(wasmBin.buffer);

  return {
    createOnigScanner(patterns) {
      return new OnigScanner(patterns);
    },
    createOnigString(s) {
      return new OnigString(s);
    }
  };
}

async function loadGrammar(grammarPath) {
  const xml = await fs.readFile(grammarPath, "utf8");
  const json = plist.parse(xml);
  assert.ok(json.scopeName, "Grammar must have a scopeName");

  const onigLib = await initOnigLib();

  const registry = new Registry({
    onigLib,
    loadGrammar: async (scopeName) => {
      if (scopeName === json.scopeName) return json;
      return null;
    }
  });

  const grammar = await registry.loadGrammar(json.scopeName);
  assert.ok(grammar, "Failed to load grammar for scopeName: " + json.scopeName);
  return { grammar, scopeName: json.scopeName };
}

function scopesContain(scopes, needle) {
  return scopes.some((s) => s.includes(needle));
}

test("SQF.tmLanguage is well-formed plist with required keys", async () => {
  const grammarPath = path.resolve(process.cwd(), "..", "..", "SQF.tmLanguage");
  const xml = await fs.readFile(grammarPath, "utf8");
  const json = plist.parse(xml);
  assert.ok(json.name, "Grammar must have a name");
  assert.ok(json.scopeName, "Grammar must have a scopeName");
  assert.ok(Array.isArray(json.patterns), "Grammar must have patterns array");
});

test("Tokenization basic: comments/strings/numbers/keywords recognized", async () => {
  const grammarPath = path.resolve(process.cwd(), "..", "..", "SQF.tmLanguage");
  const { grammar } = await loadGrammar(grammarPath);

  const sample = await fs.readFile(
    path.resolve(process.cwd(), "fixtures", "basic.sqf"),
    "utf8"
  );

  let ruleStack = INITIAL;
  const lines = sample.split(/\r?\n/);

  const found = {
    comment: false,
    string: false,
    number: false,
    keyword: false
  };

  for (const line of lines) {
    const { tokens, ruleStack: next } = grammar.tokenizeLine(line, ruleStack);
    ruleStack = next;

    for (const t of tokens) {
      const scopes = t.scopes;
      if (scopesContain(scopes, "comment")) found.comment = true;
      if (scopesContain(scopes, "string")) found.string = true;
      if (scopesContain(scopes, "constant.numeric")) found.number = true;
      if (scopesContain(scopes, "keyword")) found.keyword = true;
    }
  }

  assert.ok(found.comment, "Expected to find comment token(s)");
  assert.ok(found.string, "Expected to find string token(s)");
  assert.ok(found.number, "Expected to find numeric constant token(s)");
  assert.ok(found.keyword, "Expected to find keyword token(s)");
});

test("Control flow & operators produce keyword/operator-like scopes", async () => {
  const grammarPath = path.resolve(process.cwd(), "..", "..", "SQF.tmLanguage");
  const { grammar } = await loadGrammar(grammarPath);
  const text = await fs.readFile(
    path.resolve(process.cwd(), "fixtures", "control_flow.sqf"),
    "utf8"
  );

  let ruleStack = INITIAL;
  const lines = text.split(/\r?\n/);
  let sawControl = false;
  let sawOperator = false;

  for (const line of lines) {
    const { tokens, ruleStack: next } = grammar.tokenizeLine(line, ruleStack);
    ruleStack = next;

    for (const tok of tokens) {
      if (scopesContain(tok.scopes, "keyword.control")) sawControl = true;
      if (scopesContain(tok.scopes, "keyword.operator") || scopesContain(tok.scopes, "operator"))
        sawOperator = true;
    }
  }

  assert.ok(sawControl, "Expected control-flow keyword scopes");
  assert.ok(sawOperator, "Expected operator scopes");
});

test("Common SQF commands/functions emit function-like or support scopes", async () => {
  const grammarPath = path.resolve(process.cwd(), "..", "..", "SQF.tmLanguage");
  const { grammar } = await loadGrammar(grammarPath);
  const text = await fs.readFile(
    path.resolve(process.cwd(), "fixtures", "commands.sqf"),
    "utf8"
  );

  let ruleStack = INITIAL;
  const lines = text.split(/\r?\n/);
  let sawSupportFunction = false;

  for (const line of lines) {
    const { tokens, ruleStack: next } = grammar.tokenizeLine(line, ruleStack);
    ruleStack = next;

    for (const tok of tokens) {
      if (
        scopesContain(tok.scopes, "support.function") ||
        scopesContain(tok.scopes, "entity.name.function") ||
        scopesContain(tok.scopes, "meta.function-call")
      ) {
        sawSupportFunction = true;
      }
    }
  }

  assert.ok(sawSupportFunction, "Expected SQF commands to be scoped as functions/support");
});
