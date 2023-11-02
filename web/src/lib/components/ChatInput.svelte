<script lang="ts">
	import { messages, loadingMessages } from '$lib/stores/chatInterface/chatInputStore';
	import type { ChatMessage } from '$lib/types/chatMessage';

	let inputSimple = '';

	async function handleSubmit(e: SubmitEvent) {
		e.preventDefault();
		const message: ChatMessage = {
			role: 'user',
			content: inputSimple,
			timestamp: new Date()
		};
		messages.update((existingMessages) => [...existingMessages, message]);
		inputSimple = '';
	}
</script>

<form on:submit={handleSubmit}>
	<div class="input-group input-group-divider chat-input-group">
		<input bind:value={inputSimple} class="input-field" placeholder="Say Something..." />
		<button
			class="variant-filled-secondary"
			type="submit"
			disabled={!inputSimple || $loadingMessages}>Send</button
		>
	</div>
</form>

<style lang="postcss">
	.chat-input-group {
		@apply grid-cols-[1fr_auto] w-3/4 mx-auto mb-5 rounded-container-token;
	}
</style>
