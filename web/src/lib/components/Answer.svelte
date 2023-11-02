<script lang="ts">
	import type { Answer } from '$lib/types/answer';
	export let answer: Answer;
</script>

<div class="card card-hover mb-3 p-3" role="presentation" aria-labelledby="card-title">
	<header><h3 class="text-xl font-bold">Answer</h3></header>
	<p>ID: {answer.id}</p>
	<p>Tags: {answer.tags}</p>
	<p>
		Answer: {answer.answer}
	</p>
	<p>Already trained: {answer.already_trained}</p>
</div>
