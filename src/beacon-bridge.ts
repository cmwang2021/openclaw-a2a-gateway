import express from "express";
import { type GatewayConfig } from "./types.js";

export interface BeaconBridgeOptions {
  config: GatewayConfig;
  hubPort?: number;
}

/**
 * Registers the ShrimpClan Beacon and Agent verification bridge routes on the Express app.
 * Preserves exact path forwarding to local shrimp-hub (`http://127.0.0.1:3001`),
 * enforces Bearer token verification against `config.security.token / validTokens / BEACON_TOKEN`,
 * and prevents silent fail-open when `shrimp-hub` is unreachable.
 */
export function registerBeaconBridge(app: express.Express, options: BeaconBridgeOptions): void {
  const hubPort = options.hubPort ?? 3001;
  const config = options.config;

  app.post(["/api/beacon", "/api/agents/*"], express.json(), async (req, res) => {
    const serverToken = process.env.BEACON_TOKEN || config.security.token;
    if (!serverToken) {
      res.status(503).json({
        ok: false,
        error: "Service Unavailable: BEACON_TOKEN not configured on server (Fail-Closed)",
      });
      return;
    }

    const authHeader = req.headers.authorization;
    const header = Array.isArray(authHeader) ? authHeader[0] : authHeader;
    const providedToken = typeof header === "string" && header.startsWith("Bearer ")
      ? header.slice(7).trim()
      : "";

    if (!providedToken) {
      res.status(401).json({
        ok: false,
        error: "Unauthorized: Missing or invalid Bearer token",
      });
      return;
    }

    if (providedToken !== serverToken && !config.security.validTokens.has(providedToken)) {
      res.status(403).json({
        ok: false,
        error: "Forbidden: Invalid BEACON_TOKEN",
      });
      return;
    }

    try {
      const targetPath = req.originalUrl || req.url;
      const idempotencyKey = req.headers["idempotency-key"] || req.headers["Idempotency-Key"];
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${providedToken}`,
      };
      if (typeof idempotencyKey === "string") {
        headers["Idempotency-Key"] = idempotencyKey;
      }

      const hubResp = await fetch(`http://127.0.0.1:${hubPort}${targetPath}`, {
        method: "POST",
        headers,
        body: JSON.stringify(req.body),
      });

      const hubData = await hubResp.json().catch(() => ({}));
      res.status(hubResp.status).json(hubData);
    } catch (err: unknown) {
      // Fix Beacon Fail-Open (Master requirement 4):
      // If shrimp-hub is unreachable or offline, do NOT default to silent HTTP 200 OK.
      // Return explicit HTTP 503 (or HTTP 202 degraded if explicitly configured).
      const allowDegraded = config.beacon?.allowDegradedFallback === true;
      if (allowDegraded) {
        res.status(202).json({
          ok: true,
          degraded: true,
          hubForwarded: false,
          message: "Request verified by A2A Gateway (hub offline degraded fallback)",
          timestamp: new Date().toISOString(),
        });
      } else {
        const errMsg = err instanceof Error ? err.message : String(err);
        res.status(503).json({
          ok: false,
          hubForwarded: false,
          error: `Service Unavailable: shrimp-hub on port ${hubPort} is unreachable (${errMsg})`,
          timestamp: new Date().toISOString(),
        });
      }
    }
  });
}
