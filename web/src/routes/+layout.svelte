<script lang="ts">
	import '../app.postcss';
	import {
		initializeStores,
		AppShell,
		AppBar,
		getDrawerStore,
		Modal,
		Drawer,
		Toast
	} from '@skeletonlabs/skeleton';

	import MainMenu from '$lib/components/MainMenu.svelte';
	import MediaQuery from '$lib/components/MediaQuery.svelte';
	import Bars3 from '$lib/components/icons/Bars3.svelte';
	import ChatInput from '$lib/components/ChatInput.svelte';

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	initializeStores();

	const drawerStore = getDrawerStore();

	function drawerOpen() {
		drawerStore.open();
	}
</script>

<Toast position="bl" max={4} padding="p-3" />

<Modal />

<Drawer position="right" width="w-1/2">
	<MainMenu isMobile={true} />
</Drawer>

<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar>
			<svelte:fragment slot="lead">
				<strong class="text-xl uppercase">Charlie</strong>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<MediaQuery query="(min-width: 768px)" let:matches>
					{#if matches}
						<MainMenu />
					{:else}
						<button class="md:hidden btn btn-sm mr-4" on:click={drawerOpen}>
							<Bars3 />
						</button>
					{/if}
				</MediaQuery>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<!-- Page Route Content -->
	<div class="container p-10 mx-auto">
		<slot />
	</div>
	<svelte:fragment slot="pageFooter"><ChatInput /></svelte:fragment>
</AppShell>
