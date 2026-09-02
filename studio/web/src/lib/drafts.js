/* What a learner typed, kept across a reload.
 *
 * An evaluation takes 25-35 seconds and this audience studies on a phone in
 * stolen time. A stalled request used to leave them with a spinning card whose
 * only escape was a reload, and the reload destroyed the work — nothing was
 * ever saved. Losing a submission to a backgrounded tab is the cheapest
 * possible way to lose the person who wrote it.
 *
 * Keyed per work item so two lessons never overwrite each other. Every access
 * is wrapped: a private window, disabled site data, or a full quota all throw,
 * and none of those is a reason to break the page.
 */

export const draftKey = (kind, id) => `aprende_draft_${kind}_${id}`;

export function loadDraft(kind, id) {
  try {
    return localStorage.getItem(draftKey(kind, id)) || '';
  } catch {
    return '';
  }
}

export function saveDraft(kind, id, value) {
  try {
    localStorage.setItem(draftKey(kind, id), value);
  } catch {
    /* private mode, or storage disabled */
  }
}

export function clearDraft(kind, id) {
  try {
    localStorage.removeItem(draftKey(kind, id));
  } catch {
    /* private mode, or storage disabled */
  }
}

/** A debounced saver for a textarea's `oninput`. 400ms, as before. */
export function draftSaver(kind, id) {
  let timer = null;
  return (value) => {
    clearTimeout(timer);
    timer = setTimeout(() => saveDraft(kind, id, value), 400);
  };
}
