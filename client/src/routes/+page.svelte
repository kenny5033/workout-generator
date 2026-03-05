<script lang="ts">
  import type { PageProps } from "./$types";
  const { data }: PageProps = $props();
</script>

{#each data.workouts as workout}
  <h2>{workout.type.name}</h2>
  <p>{workout.exercise}</p>
{/each}

