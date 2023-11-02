<script lang="ts">
	import { LightSwitch, getModalStore } from '@skeletonlabs/skeleton';
	import { modal } from '$lib/helpers/userSettingsModal';
	import Cog6Tooth from './icons/Cog6Tooth.svelte';

	export let isMobile = false;

	const modalStore = getModalStore();

	const openSettingsMenu = () => {
		modalStore.trigger(modal);
	};
</script>

{#if isMobile}
	<div class="container p-10 flex flex-col place-items-center gap-4 h-full place-content-center">
		<LightSwitch />
		<button
			class="btn hover:rotate-45"
			on:click={openSettingsMenu}
			aria-label="Settings"
			title="Settings"
		>
			<Cog6Tooth />
		</button>
		<a
			class="btn variant-ghost-surface"
			href="https://github.com/CristiCriss17G/Base64Bender"
			target="_blank"
			rel="noreferrer"
		>
			GitHub
		</a>
	</div>
{:else}
	<LightSwitch />
	<button
		class="btn hover:rotate-45"
		on:click={openSettingsMenu}
		aria-label="Settings"
		title="Settings"
	>
		<Cog6Tooth />
	</button>
{/if}
