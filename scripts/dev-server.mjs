// Static server that mimics GitHub Pages: unknown paths get 404.html with status 404.
// node scripts/dev-server.mjs [port]
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { join, extname, normalize } from "node:path";
const root = new URL("..", import.meta.url).pathname;
const port = Number(process.argv[2] || 8787);
const types = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml", ".ico": "image/x-icon", ".txt": "text/plain", ".xml": "application/xml" };
createServer(async (req, res) => {
  const url = new URL(req.url, "http://x");
  let p = normalize(decodeURIComponent(url.pathname)).replace(/^(\.\.[/\\])+/, "");
  let file = join(root, p);
  try {
    let s = await stat(file);
    if (s.isDirectory()) { file = join(file, "index.html"); s = await stat(file); }
    const ext = extname(file);
    res.writeHead(200, { "content-type": types[ext] || (ext === "" ? "application/json" : "application/octet-stream") });
    res.end(await readFile(file));
  } catch {
    res.writeHead(404, { "content-type": "text/html; charset=utf-8" });
    res.end(await readFile(join(root, "404.html")));
  }
}).listen(port, () => console.log(`landing on http://localhost:${port}`));
