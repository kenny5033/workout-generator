<script lang="ts">
  import type { PageData } from './$types';
  import { addWorkout, ApiError } from '$lib/api';
  import { invalidateAll } from '$app/navigation';
  import type { Workout } from '$lib/types';

  export let data: PageData;

  let workoutTypeId = '';
  let name = '';
  let submitting = false;
  let error = '';
  let successMsg = '';

  async function handleAdd() {
    error = '';
    successMsg = '';

    const typeId = parseInt(workoutTypeId, 10);
    if (!workoutTypeId || isNaN(typeId)) {
      error = 'Workout Type ID must be a valid integer.';
      return;
    }
    if (!name.trim()) {
      error = 'Name is required.';
      return;
    }

    submitting = true;
    try {
      await addWorkout(fetch, { workout_type_id: typeId, name: name.trim() });
      successMsg = `"${name.trim()}" added to your routine.`;
      workoutTypeId = '';
      name = '';
      await invalidateAll();
    } catch (e) {
      if (e instanceof ApiError) {
        error =
          typeof e.detail === 'string'
            ? e.detail
            : (e.detail.detail?.[0]?.msg ?? `Error ${e.status}`);
      } else {
        error = 'Unexpected error. Check the console.';
        console.error(e);
      }
    } finally {
      submitting = false;
    }
  }

  $: workouts = data.routine.workouts;
</script>

<svelte:head>
  <title>Routine</title>
</svelte:head>

<section class="page">

  <!-- Hero heading -->
  <div class="hero">
    <p class="eyebrow">TODAY'S SESSION</p>
    <h1 class="headline">
      YOUR<br /><span class="accent-text">ROUTINE</span>
    </h1>
    <p class="workout-count">
      <span class="count-num">{workouts.length}</span>
      {workouts.length === 1 ? 'EXERCISE' : 'EXERCISES'} LOADED
    </p>
  </div>

  <!-- Workout list -->
  <div class="section">
    <div class="section-header">
      <span class="section-label">EXERCISE LIST</span>
      <div class="section-line"></div>
    </div>

    {#if workouts.length === 0}
      <div class="empty-state">
        <span class="empty-icon">—</span>
        <p>No exercises in your routine yet.</p>
        <p class="empty-hint">Add one below to get started.</p>
      </div>
    {:else}
      <ol class="workout-list">
        {#each workouts as workout, i (workout.id ?? i)}
          <li class="workout-row">
            <span class="row-index">{String(i + 1).padStart(2, '0')}</span>
            <span class="row-exercise">{workout.exercise}</span>
            <span class="row-meta">
              TYPE <span class="meta-val">{workout.workout_type_id}</span>
            </span>
            {#if workout.id != null}
              <span class="row-id">#{workout.id}</span>
            {/if}
          </li>
        {/each}
      </ol>
    {/if}
  </div>

  <!-- Add workout form -->
  <div class="section">
    <div class="section-header">
      <span class="section-label">ADD EXERCISE</span>
      <div class="section-line"></div>
    </div>

    <div class="form-card">
      <div class="form-grid">
        <div class="field">
          <label class="field-label" for="workout-type">WORKOUT TYPE ID</label>
          <input
            id="workout-type"
            class="field-input"
            type="number"
            min="1"
            placeholder="e.g. 3"
            bind:value={workoutTypeId}
            disabled={submitting}
          />
        </div>

        <div class="field">
          <label class="field-label" for="workout-name">EXERCISE NAME</label>
          <input
            id="workout-name"
            class="field-input"
            type="text"
            placeholder="e.g. Deadlift"
            bind:value={name}
            disabled={submitting}
            on:keydown={(e) => e.key === 'Enter' && handleAdd()}
          />
        </div>
      </div>

      {#if error}
        <div class="message error" role="alert">
          <span class="msg-prefix">ERR //</span> {error}
        </div>
      {/if}

      {#if successMsg}
        <div class="message success" role="status">
          <span class="msg-prefix">OK //</span> {successMsg}
        </div>
      {/if}

      <button class="submit-btn" on:click={handleAdd} disabled={submitting}>
        {#if submitting}
          <span class="btn-spinner"></span> ADDING…
        {:else}
          <span class="btn-plus">+</span> ADD TO ROUTINE
        {/if}
      </button>
    </div>
  </div>

</section>

<style>
  .page {
    display: flex;
    flex-direction: column;
    gap: 3.5rem;
  }

  /* Hero */
  .hero {
    border-left: 3px solid var(--accent);
    padding-left: 1.5rem;
  }

  .eyebrow {
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
  }

  .headline {
    font-family: var(--font-display);
    font-size: clamp(4rem, 10vw, 7rem);
    font-weight: 900;
    line-height: 0.9;
    letter-spacing: -0.01em;
    text-transform: uppercase;
    color: var(--text);
    margin-bottom: 1rem;
  }

  .accent-text {
    color: var(--accent);
    -webkit-text-stroke: 0;
  }

  .workout-count {
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    color: var(--text-dim);
  }

  .count-num {
    font-family: var(--font-display);
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent);
    vertical-align: middle;
    margin-right: 0.25rem;
  }

  /* Section */
  .section {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .section-label {
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    color: var(--text-muted);
    white-space: nowrap;
  }

  .section-line {
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  /* Workout list */
  .empty-state {
    padding: 2.5rem;
    border: 1px dashed var(--border);
    text-align: center;
    color: var(--text-muted);
    font-size: 0.8rem;
    letter-spacing: 0.1em;
  }

  .empty-icon {
    display: block;
    font-size: 2rem;
    margin-bottom: 0.75rem;
    color: var(--border);
  }

  .empty-hint {
    margin-top: 0.25rem;
    font-size: 0.7rem;
    color: var(--text-muted);
    opacity: 0.6;
  }

  .workout-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 0;
  }

  .workout-row {
    display: grid;
    grid-template-columns: 2.5rem 1fr auto auto;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.25rem;
    border: 1px solid var(--border);
    border-bottom: none;
    background: var(--surface);
    transition: background 0.15s;
  }

  .workout-row:last-child {
    border-bottom: 1px solid var(--border);
  }

  .workout-row:hover {
    background: var(--surface-2);
  }

  .row-index {
    font-size: 0.7rem;
    color: var(--accent);
    letter-spacing: 0.05em;
    font-weight: 500;
  }

  .row-exercise {
    font-family: var(--font-display);
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--text);
  }

  .row-meta {
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: var(--text-muted);
  }

  .meta-val {
    color: var(--text-dim);
    font-weight: 500;
  }

  .row-id {
    font-size: 0.65rem;
    color: var(--text-muted);
    opacity: 0.5;
  }

  /* Form */
  .form-card {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 1.75rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 1rem;
  }

  @media (max-width: 560px) {
    .form-grid {
      grid-template-columns: 1fr;
    }
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .field-label {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: var(--text-muted);
  }

  .field-input {
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 0.9rem;
    padding: 0.65rem 0.85rem;
    outline: none;
    transition: border-color 0.15s;
    width: 100%;
  }

  .field-input::placeholder {
    color: var(--text-muted);
    opacity: 0.5;
  }

  .field-input:focus {
    border-color: var(--accent);
  }

  .field-input:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  /* Remove number input spinners */
  .field-input[type='number']::-webkit-inner-spin-button,
  .field-input[type='number']::-webkit-outer-spin-button {
    -webkit-appearance: none;
  }

  /* Messages */
  .message {
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    padding: 0.6rem 0.85rem;
    border-left: 3px solid;
  }

  .message.error {
    border-color: var(--danger);
    color: var(--danger);
    background: rgba(255, 69, 69, 0.06);
  }

  .message.success {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--accent-dim);
  }

  .msg-prefix {
    font-weight: 500;
    opacity: 0.7;
    margin-right: 0.25rem;
  }

  /* Submit button */
  .submit-btn {
    align-self: flex-start;
    background: var(--accent);
    color: var(--bg);
    border: none;
    font-family: var(--font-display);
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.75rem 2rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: opacity 0.15s, transform 0.1s;
  }

  .submit-btn:hover:not(:disabled) {
    opacity: 0.88;
  }

  .submit-btn:active:not(:disabled) {
    transform: scale(0.98);
  }

  .submit-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .btn-plus {
    font-size: 1.2rem;
    line-height: 1;
  }

  .btn-spinner {
    width: 0.8rem;
    height: 0.8rem;
    border: 2px solid var(--bg);
    border-top-color: transparent;
    border-radius: 50%;
    display: inline-block;
    animation: spin 0.7s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
</style>
