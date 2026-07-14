import test from "node:test";
import assert from "node:assert/strict";
import express from "express";
import http from "node:http";
import { registerBeaconBridge } from "../src/beacon-bridge.js";
import { type GatewayConfig } from "../src/types.js";

function makeMockConfig(token: string): GatewayConfig {
  return {
    agentCard: { name: "test", skills: [] },
    server: { host: "127.0.0.1", port: 18800 },
    storage: { tasksDir: "/tmp", taskTtlHours: 1, cleanupIntervalMinutes: 1 },
    peers: [],
    security: {
      inboundAuth: "bearer",
      token,
      tokens: [],
      validTokens: new Set([token]),
      allowedMimeTypes: [],
      maxFileSizeBytes: 100,
      maxInlineFileSizeBytes: 100,
      fileUriAllowlist: [],
    },
    routing: { defaultAgentId: "main", rules: [] },
    limits: { maxConcurrentTasks: 1, maxQueuedTasks: 1 },
    observability: {
      structuredLogs: false,
      exposeMetricsEndpoint: false,
      metricsPath: "/metrics",
      metricsAuth: "none",
      auditLogPath: "/tmp/audit.jsonl",
    },
    resilience: {
      healthCheck: { enabled: false, intervalMs: 1000, timeoutMs: 1000 },
      retry: { maxRetries: 0, baseDelayMs: 10, maxDelayMs: 10 },
      circuitBreaker: { failureThreshold: 1, resetTimeoutMs: 1000 },
    },
    discovery: { enabled: false, serviceName: "", refreshIntervalMs: 1000, mergeWithStatic: false },
    advertise: { enabled: false, serviceName: "", announceIntervalMs: 1000 },
  } as GatewayConfig;
}

test("Beacon Bridge: Fail-Closed when token missing in request", async () => {
  const app = express();
  const config = makeMockConfig("secret-beacon-token-123");
  registerBeaconBridge(app, { config, hubPort: 39999 });

  const server = http.createServer(app);
  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address() as import("node:net").AddressInfo;
  const url = `http://127.0.0.1:${address.port}/api/beacon`;

  try {
    const resp = await fetch(url, { method: "POST" });
    assert.equal(resp.status, 401);
    const body = await resp.json();
    assert.match(body.error, /Missing or invalid Bearer token/);
  } finally {
    server.close();
  }
});

test("Beacon Bridge: 403 Forbidden when token mismatch", async () => {
  const app = express();
  const config = makeMockConfig("secret-beacon-token-123");
  registerBeaconBridge(app, { config, hubPort: 39999 });

  const server = http.createServer(app);
  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address() as import("node:net").AddressInfo;
  const url = `http://127.0.0.1:${address.port}/api/beacon`;

  try {
    const resp = await fetch(url, {
      method: "POST",
      headers: { Authorization: "Bearer wrong-token" },
    });
    assert.equal(resp.status, 403);
    const body = await resp.json();
    assert.match(body.error, /Invalid BEACON_TOKEN/);
  } finally {
    server.close();
  }
});

test("Beacon Bridge: 503 Fail-Closed when shrimp-hub unreachable", async () => {
  const app = express();
  const config = makeMockConfig("secret-beacon-token-123");
  // Port 39999 is intentionally unreachable
  registerBeaconBridge(app, { config, hubPort: 39999 });

  const server = http.createServer(app);
  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address() as import("node:net").AddressInfo;
  const url = `http://127.0.0.1:${address.port}/api/beacon`;

  try {
    const resp = await fetch(url, {
      method: "POST",
      headers: { Authorization: "Bearer secret-beacon-token-123" },
    });
    assert.equal(resp.status, 503);
    const body = await resp.json();
    assert.equal(body.ok, false);
    assert.equal(body.hubForwarded, false);
    assert.match(body.error, /shrimp-hub on port 39999 is unreachable/);
  } finally {
    server.close();
  }
});

test("Beacon Bridge: forwards cleanly to hub when hub is up", async () => {
  // Start a mock shrimp-hub on port 0
  const hubApp = express();
  hubApp.use(express.json());
  hubApp.post("/api/beacon", (req, res) => {
    res.status(200).json({ ok: true, hubReceived: req.body });
  });
  const hubServer = http.createServer(hubApp);
  await new Promise<void>((resolve) => hubServer.listen(0, "127.0.0.1", resolve));
  const hubPort = (hubServer.address() as import("node:net").AddressInfo).port;

  const app = express();
  const config = makeMockConfig("secret-beacon-token-123");
  registerBeaconBridge(app, { config, hubPort });

  const server = http.createServer(app);
  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address() as import("node:net").AddressInfo;
  const url = `http://127.0.0.1:${address.port}/api/beacon`;

  try {
    const resp = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: "Bearer secret-beacon-token-123",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ping: "pong" }),
    });
    assert.equal(resp.status, 200);
    const body = await resp.json();
    assert.equal(body.ok, true);
    assert.deepEqual(body.hubReceived, { ping: "pong" });
  } finally {
    hubServer.close();
    server.close();
  }
});

test("Beacon Bridge: 202 Degraded when allowDegradedFallback=true and shrimp-hub unreachable", async () => {
  const app = express();
  const config = makeMockConfig("secret-beacon-token-123");
  config.beacon = { enabled: true, allowDegradedFallback: true };
  // Port 39999 is intentionally unreachable
  registerBeaconBridge(app, { config, hubPort: 39999 });

  const server = http.createServer(app);
  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address() as import("node:net").AddressInfo;
  const url = `http://127.0.0.1:${address.port}/api/beacon`;

  try {
    const resp = await fetch(url, {
      method: "POST",
      headers: { Authorization: "Bearer secret-beacon-token-123" },
    });
    assert.equal(resp.status, 202);
    const body = await resp.json();
    assert.equal(body.ok, true);
    assert.equal(body.hubForwarded, false);
    assert.match(body.message, /degraded fallback/);
  } finally {
    server.close();
  }
});

