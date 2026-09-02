/* The drawn icon set — single stroke, currentColor, no emoji in the chrome
 * (PRODUCT.md, Brand Commitments).
 *
 * Copied verbatim from learn.html's PATHS. It is data, not code: an inline SVG
 * path per name, so nothing here can drift into a second visual language the
 * way an icon font or a CDN set would.
 */
export const PATHS = {
  eye: 'M2 12s3.7-7 10-7 10 7 10 7-3.7 7-10 7-10-7-10-7ZM12 12m-3 0a3 3 0 1 0 6 0a3 3 0 1 0-6 0',
  play: 'M8 5.8v12.4c0 .8.9 1.3 1.6.9l10-6.2c.6-.4.6-1.4 0-1.8l-10-6.2c-.7-.4-1.6.1-1.6.9Z',
  book: 'M2 4h6a4 4 0 0 1 4 4v12a3 3 0 0 0-3-3H2zM22 4h-6a4 4 0 0 0-4 4v12a3 3 0 0 1 3-3h7z',
  tool: 'M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z',
  flame: 'M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z',
  flag: 'M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1zM4 22v-7',
  doc: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M16 13H8M16 17H8',
  mic: 'M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3ZM19 10v2a7 7 0 0 1-14 0v-2M12 19v3',
  target: 'M12 12m-10 0a10 10 0 1 0 20 0a10 10 0 1 0-20 0M12 12m-6 0a6 6 0 1 0 12 0a6 6 0 1 0-12 0M12 12m-2 0a2 2 0 1 0 4 0a2 2 0 1 0-4 0',
  redo: 'M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8M3 3v5h5',
  lock: 'M3 11h18v11H3zM7 11V7a5 5 0 0 1 10 0v4',
  check: 'M20 6 9 17l-5-5',
  arrow: 'm9 18 6-6-6-6',
  spark: 'M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 15l.9 2.6L22.5 18l-2.6.9L19 21.5l-.9-2.6L15.5 18l2.6-.9z',
  clock: 'M12 12m-10 0a10 10 0 1 0 20 0a10 10 0 1 0-20 0M12 6v6l4 2',
  send: 'm22 2-7 20-4-9-9-4ZM22 2 11 13',
  copy: 'M9 9h13v13H9zM5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1',
  pen: 'M12 20h9M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z',
  alert: 'M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0zM12 9v4M12 17h.01',
  sun: 'M12 12m-4 0a4 4 0 1 0 8 0a4 4 0 1 0-8 0M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4',
  user: 'M12 8m-4 0a4 4 0 1 0 8 0a4 4 0 1 0-8 0M20 21a8 8 0 0 0-16 0',
  down: 'M12 3v14m0 0 5-5m-5 5-5-5M5 21h14',
};

/** One icon per content area. A name with no entry falls back to the book. */
export const CAT_ICON = {
  'Marketing y contenido': 'pen',
  'Publicidad digital': 'target',
  'Analítica y automatización': 'spark',
  'Ciencias sociales': 'user',
  Deporte: 'flag',
  'Redes y creadores': 'send',
};

/** Markup for one icon. Used where a component builds an HTML string. */
export const icon = (name, cls = 'ic') =>
  `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="${PATHS[name] || ''}"/></svg>`;

/** Courses grouped by category, in first-seen order; unknowns bucket last. */
export function clusterize(courses) {
  const groups = new Map();
  for (const c of courses) {
    const key = c.category || 'Más cursos';
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(c);
  }
  return [...groups.entries()];
}
