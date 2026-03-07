<script lang="ts">
	import type { PageData } from './$types';
	import { invalidateAll } from '$app/navigation';
	import RoutineHero from '$components/RoutineHero.svelte';
	import WorkoutList from "$components/WorkoutList.svelte";
	import AddWorkoutForm from '$components/AddWorkoutForm.svelte';

	export let data: PageData;

	$: workouts = data.routine.workouts;
</script>

<svelte:head>
	<title>Routine</title>
</svelte:head>

<section class="page">
	<RoutineHero workoutCount={workouts.length} />
	<WorkoutList {workouts} />
	<AddWorkoutForm api={data.api} onSuccess={invalidateAll} />
</section>

<style>
	.page {
		display: flex;
		flex-direction: column;
		gap: 3.5rem;
	}
</style>
