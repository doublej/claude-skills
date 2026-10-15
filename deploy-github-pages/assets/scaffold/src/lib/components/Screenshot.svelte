<script lang="ts">
  import { base } from '$app/paths'

  // App screenshot in a window frame, the GUI counterpart of Terminal.
  // `file` is a name in static/screens/ (e.g. "today.webp"); the file must
  // exist before a production build, or the strict prerender fails on a 404.
  let {
    file,
    alt,
    title = '',
    maxWidth = '100%',
  }: {
    file: string
    alt: string
    title?: string
    maxWidth?: string
  } = $props()
</script>

<figure class="screenshot" style:max-width={maxWidth}>
  {#if title}<figcaption class="screenshot-bar">{title}</figcaption>{/if}
  <img src="{base}/screens/{file}" {alt} loading="lazy" decoding="async" />
</figure>

<style>
  .screenshot {
    margin: 0;
    width: 100%;
    border-radius: 6px;
    overflow: hidden;
    background: var(--term-bg);
    box-shadow:
      0 1px 0 color-mix(in oklch, var(--ink) 30%, transparent),
      0 24px 48px -24px color-mix(in oklch, var(--ink) 55%, transparent);
  }

  .screenshot-bar {
    padding: 10px 16px;
    background: var(--term-bar);
    color: var(--term-dim);
    font-family: var(--font-mono);
    font-stretch: 87.5%;
    font-size: 0.75rem;
  }

  img {
    display: block;
    width: 100%;
    height: auto;
  }
</style>
