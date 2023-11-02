<script lang="ts">
	import { messages } from '$lib/stores/chatInterface/chatInputStore';
	import ChatMessages from '$lib/components/ChatMessages.svelte';
</script>

<svelte:head>
	<meta name="description" content="Charlie - THI ChatBot" />
	<meta name="keywords" content="charlie, THI, Ingolstadt, university, chatbot" />
	<meta name="author" content="CAI1 Students" />
	<meta name="robots" content="index, follow" />
</svelte:head>

<div class="card p-4 mb-5 {$messages.length > 0 ? 'hidden' : ''}">
	<h1 class="text-3xl font-bold mb-4">Charlie</h1>
	<p class="mb-4">Welcome to Charlie, the THI ChatBot</p>
</div>
<ChatMessages messages={$messages} />
