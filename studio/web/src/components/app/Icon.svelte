<script>
  /* One drawn icon, for the app. Decorative by default: these sit beside their
     own label everywhere they appear, so announcing them reads the label twice. */
  import { PATHS } from '../../lib/icons.js';
  let { name, class: cls = 'ic' } = $props();
</script>

<svg class={cls} viewBox="0 0 24 24" aria-hidden="true"><path d={PATHS[name] || ''} /></svg>
