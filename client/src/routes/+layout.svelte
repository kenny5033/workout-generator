<script lang="ts">
  import { page } from '$app/stores';
</script>

<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
  <link
    href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;900&family=IBM+Plex+Mono:wght@400;500&display=swap"
    rel="stylesheet"
  />
</svelte:head>

<div class="app">
  <header>
    <div class="header-inner">
      <span class="logo">
        <span class="logo-bracket">[</span>
        ROUTINE
        <span class="logo-bracket">]</span>
      </span>
      <span class="status-pill">LIVE</span>
    </div>
    <div class="header-rule"></div>
  </header>

  <main>
    <slot />
  </main>

  <footer>
    <span class="footer-text">WORKOUT TRACKER — {new Date().getFullYear()}</span>
  </footer>
</div>

<style>
  :global(*, *::before, *::after) {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  :global(:root) {
    --bg: #0c0c0c;
    --surface: #141414;
    --surface-2: #1e1e1e;
    --border: #2a2a2a;
    --accent: #e8ff47;
    --accent-dim: rgba(232, 255, 71, 0.12);
    --danger: #ff4545;
    --text: #f0f0f0;
    --text-muted: #666;
    --text-dim: #999;
    --font-display: 'Barlow Condensed', sans-serif;
    --font-mono: 'IBM Plex Mono', monospace;
  }

  :global(body) {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-mono);
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
  }

  :global(::selection) {
    background: var(--accent);
    color: var(--bg);
  }

  .app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  header {
    padding: 0 2rem;
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--bg);
  }

  .header-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem 0;
  }

  .logo {
    font-family: var(--font-display);
    font-size: 1.5rem;
    font-weight: 900;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text);
  }

  .logo-bracket {
    color: var(--accent);
  }

  .status-pill {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: var(--accent);
    border: 1px solid var(--accent);
    padding: 0.25rem 0.6rem;
    position: relative;
  }

  .status-pill::before {
    content: '';
    display: inline-block;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--accent);
    margin-right: 0.5rem;
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
  }

  .header-rule {
    height: 1px;
    background: linear-gradient(90deg, var(--accent) 0%, transparent 60%);
  }

  main {
    flex: 1;
    padding: 3rem 2rem;
    max-width: 900px;
    width: 100%;
    margin: 0 auto;
  }

  footer {
    padding: 1.5rem 2rem;
    border-top: 1px solid var(--border);
  }

  .footer-text {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--text-muted);
  }
</style>
