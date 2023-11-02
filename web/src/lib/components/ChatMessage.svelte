<script lang="ts">
	import type { ChatMessage } from '$lib/types/chatMessage';
	import Markdown from '@magidoc/plugin-svelte-marked';
	export let message: ChatMessage;

	let isHovered = false;
	const toggleVisibility = () => (isHovered = !isHovered);
</script>

<!-- Render user input and chatbot responses -->
<div
	class="card card-hover chat-message {message.role === 'user' ? 'user-message' : 'bot-message'}"
	on:mouseover={toggleVisibility}
	on:mouseout={toggleVisibility}
	on:focus={toggleVisibility}
	on:blur={toggleVisibility}
	role="presentation"
	aria-labelledby="card-title"
>
	<header>
		{#if message.role === 'user'}
			<small class={!isHovered ? 'opacity-0' : 'opacity-50'}
				><em>{message.timestamp.toLocaleTimeString()}</em></small
			>
			<p class="font-bold">You</p>
		{:else}
			<p class="font-bold">Charlie</p>
			<small class={!isHovered ? 'opacity-0' : 'opacity-50'}
				><em>{message.timestamp.toLocaleTimeString()}</em></small
			>
		{/if}
	</header>
	<span class="message-content">
		{#if message.role === 'user'}
			{message.content}
		{:else}
			<Markdown source={message.content} />
		{/if}
	</span>
</div>

<style lang="postcss">
	.chat-message {
		@apply flex flex-col gap-2 w-full md:w-3/5 p-4 mb-3;
		header {
			@apply w-full flex justify-between items-center;
		}
	}
	.user-message {
		@apply items-end ml-auto;
	}
	.bot-message {
		@apply items-start mr-auto;
	}
</style>
