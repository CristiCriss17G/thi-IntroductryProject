<script lang="ts">
	import { answers } from '$lib/stores/answers';
	import { getAnswers } from '$lib/helpers/queryApi/answersQueries';
	import { onMount } from 'svelte';

	import Answers from '$lib/components/Answers.svelte';

	onMount(async () => {
		await getAnswers();
	});
</script>

<div>
	<Answers answers={$answers} />
</div>
