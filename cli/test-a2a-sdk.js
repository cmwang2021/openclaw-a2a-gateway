import { createClient } from "./src/lib/client-factory.js";

const url = "http://100.123.6.86:18800";
const token = "57cd604bf91e1d73a0584353bb09b8be1fabbea85b6bdfa4";

console.log("Probing createClient with url:", url);
try {
  const client = await createClient(url, { token });
  console.log("Success! Client created:", client);
} catch (err) {
  console.error("Failed to create client:");
  console.error(err);
  if (err instanceof Error && err.cause) {
    console.error("Cause:", err.cause);
  }
}
