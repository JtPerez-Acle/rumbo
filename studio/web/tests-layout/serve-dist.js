/* Serve dist/ the way FastAPI serves it, in the foreground.
 *
 * Two reasons this exists instead of `astro preview`:
 *
 * 1. `astro preview` DAEMONIZES — it forks and the foreground process exits,
 *    which Playwright reads as "the web server died" and gives up before a
 *    single test runs.
 * 2. Production does not use it. FastAPI maps /cursos to cursos/index.html and
 *    mounts /assets; twenty lines that do exactly that are a better model of
 *    the thing being tested than a dev tool with its own routing.
 */
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DIST = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../dist');
const PORT = Number(process.env.PORT || 4321);

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.woff2': 'font/woff2',
};

http
  .createServer((req, res) => {
    const url = decodeURIComponent((req.url || '/').split('?')[0]);
    // Directory-style URLs, exactly as public_site.page() resolves them.
    const rel = url.endsWith('/') ? `${url}index.html` : url;
    let file = path.join(DIST, rel);
    // A path with no extension is a route, not a file: /cursos -> cursos/index.html
    if (!path.extname(file)) file = path.join(file, 'index.html');

    // Nothing outside dist/ is servable, whatever the URL claims.
    if (!file.startsWith(DIST)) {
      res.writeHead(403).end('forbidden');
      return;
    }
    fs.readFile(file, (err, body) => {
      if (err) {
        res.writeHead(404, { 'content-type': 'text/plain' }).end('not found');
        return;
      }
      res.writeHead(200, { 'content-type': TYPES[path.extname(file)] || 'application/octet-stream' });
      res.end(body);
    });
  })
  .listen(PORT, () => console.log(`serving ${DIST} on http://localhost:${PORT}`));
