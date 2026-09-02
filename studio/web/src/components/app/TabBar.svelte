<script>
  /* The four tabs. Real <button>s in a <nav>, which the string-built version
     also was — what it was not is announced: nothing said which tab was
     current, so a screen reader read four identical destinations. */
  import Icon from './Icon.svelte';
  import { route, nav } from '../../lib/router.svelte.js';

  const TABS = [
    ['hoy', 'Hoy', 'sun'],
    ['cursos', 'Cursos', 'book'],
    ['portafolio', 'Portafolio', 'doc'],
    ['perfil', 'Perfil', 'user'],
  ];
</script>

<nav class="tabbar" aria-label="Secciones">
  {#each TABS as [key, label, icon]}
    <button
      class={route.tab === key ? 'on' : ''}
      aria-current={route.tab === key ? 'page' : undefined}
      onclick={() => nav('#/' + key)}
    >
      <Icon name={icon} />{label}
    </button>
  {/each}
</nav>
