/* Paths the suites share.
 *
 * This used to be a DOM shim: it read learn.html, pulled out its last <script>,
 * substituted the two DOM entry points and ran the whole SPA inside a fake
 * document so a render function could be called in isolation. It replaced four
 * near-identical copies of that trick and it worked.
 *
 * It is gone because its subject is. Every suite now drives a real component
 * under jsdom or reads the built HTML, which is both simpler and stricter — the
 * shim could pass while the page a visitor received was eleven characters of
 * "Cargando…", and it did.
 */
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
