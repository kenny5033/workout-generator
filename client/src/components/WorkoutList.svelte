<script lang="ts">
	import { type Workout } from '$lib/gen/openapi/models';
	export let workouts: Workout[];
</script>

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

<style>
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
</style>
