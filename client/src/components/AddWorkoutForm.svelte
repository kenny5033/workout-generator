<script lang="ts">
	import type { DefaultApi } from "$lib/gen/openapi";

	export let api: Pick<DefaultApi, "addWorkoutAddPost" | "workoutTypesWorkoutTypesGet">;
	export let onSuccess: () => Promise<void>;

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
			await api.addWorkoutAddPost({ workoutTypeId: typeId, name });
			workoutTypeId = '';
			name = '';
			successMsg = 'Exercise added to your routine.';
			await onSuccess();
		} catch (e) {
			console.error(e);
			error = 'Failed to add exercise. Please try again.';
		} finally {
			submitting = false;
		}
	}

	$: workoutTypes = api.workoutTypesWorkoutTypesGet();
</script>

<div class="section">
	<div class="section-header">
		<span class="section-label">ADD EXERCISE</span>
		<div class="section-line"></div>
	</div>

	<div class="form-card">
	{#await workoutTypes}
		<p>Loading...</p>
	{:then workoutTypes}
		<div class="form-grid">
			<div class="field">
				<label class="field-label" for="workout-type">WORKOUT TYPE ID</label>
				<select id="workout-type" class="field-input" placeholder="CORE" bind:value={workoutTypeId} disabled={submitting}>
					{#each workoutTypes as workoutType}
						<option value={workoutType.id} class="field-input">{workoutType.name.toUpperCase()}</option>
					{/each}
				</select>
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
				<span class="msg-prefix">ERR //</span>
				{error}
			</div>
		{/if}
		{#if successMsg}
			<div class="message success" role="status">
				<span class="msg-prefix">OK //</span>
				{successMsg}
			</div>
		{/if}

		<button class="submit-btn" on:click={handleAdd} disabled={submitting}>
			{#if submitting}
				<span class="btn-spinner"></span> ADDING…
			{:else}
				<span class="btn-plus">+</span> ADD TO ROUTINE
			{/if}
		</button>
	{/await}
	</div>
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
	.field-input[type='number']::-webkit-inner-spin-button,
	.field-input[type='number']::-webkit-outer-spin-button {
		-webkit-appearance: none;
	}
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
		to {
			transform: rotate(360deg);
		}
	}
</style>
