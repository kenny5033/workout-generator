<script lang="ts">
	export let workoutCount: number;
</script>

<div class="hero">
	<p class="eyebrow">TODAY'S SESSION</p>
	<h1 class="headline">
		YOUR<br /><span class="accent-text">ROUTINE</span>
	</h1>
	<p class="workout-count">
		<span class="count-num">{workoutCount}</span>
		{workoutCount === 1 ? 'EXERCISE' : 'EXERCISES'} LOADED
	</p>
</div>

<style>
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
</style>
