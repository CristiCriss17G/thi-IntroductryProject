<script lang="ts">
	import Answer from '$lib/components/Answer.svelte';
	import type { Answer as AnswerType } from '$lib/types/answer';
	import { afterUpdate, onMount } from 'svelte';
	export let answers: AnswerType[] = [];

	let showAlreadyTrained = false;
	let visibleAnswers: AnswerType[] = [];

	afterUpdate(() => {
		console.log('afterUpdate');
		visibleAnswers = answers.filter((answer: AnswerType) => {
			if (showAlreadyTrained) {
				return true;
			} else {
				return !answer.already_trained;
			}
		});
	});
	onMount(() => {
		console.log('onMount');
		visibleAnswers = answers.filter((answer: AnswerType) => {
			if (showAlreadyTrained) {
				return true;
			} else {
				return !answer.already_trained;
			}
		});
	});
</script>

<div class="grid items-center grid-cols-[auto_auto] gap-4 mb-4">
	<h1>Available answers:</h1>
	<div class="flex items-center gap-2">
		<label for="showAlreadyTrained">Show already trained</label>
		<input
			class="checkbox"
			type="checkbox"
			id="showAlreadyTrained"
			bind:checked={showAlreadyTrained}
		/>
	</div>
</div>

<div class="answers">
	{#each visibleAnswers as answer}
		<Answer {answer} />
	{/each}
</div>
