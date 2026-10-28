// Render a composition to a transparent WebM (VP9 + alpha) for the HyperFrames builder.
// Usage: node render.mjs [CompositionId] [out.webm] ['{"plates":4}']
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import path from "node:path";
import fs from "node:fs";

const id = process.argv[2] ?? "PlateLoad";
const out = process.argv[3] ?? `out/${id}.webm`;
const inputProps = process.argv[4] ? JSON.parse(process.argv[4]) : {};
// Use the sandbox's preinstalled Chromium when present; otherwise Remotion downloads its own.
const local = ["/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"].find((p) => fs.existsSync(p));

const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const composition = await selectComposition({ serveUrl, id, inputProps, browserExecutable: local ?? null, chromiumOptions: { gl: "angle" } });
await renderMedia({
  composition, serveUrl, inputProps, outputLocation: out,
  codec: "vp9", imageFormat: "png", pixelFormat: "yuva420p",
  browserExecutable: local ?? null, chromiumOptions: { gl: "angle" },
  onProgress: ({ progress }) => process.stdout.write(`\r${Math.round(progress * 100)}%`),
});
console.log(`\nwrote ${out}`);
