<script lang="ts">
	// Props
	/** Exposes parent props to this component. */
	import type { ModalProps } from '@skeletonlabs/skeleton/dist/utilities/Modal/Modal.svelte';
	export let parent: ModalProps;

	// Types
	import type { UserSettings } from '$lib/types/userSettings';

	import { get } from 'svelte/store';

	// Stores
	import {
		SlideToggle,
		getModalStore,
		TabGroup,
		Tab,
		TabAnchor,
		RadioGroup,
		RadioItem,
		RangeSlider,
		getToastStore
	} from '@skeletonlabs/skeleton';
	import { userSettings } from '$lib/stores/userSettings';
	import { sendTrainMessage, init as trainInit } from '$lib/helpers/queryApi/sendTrainMessage';
	import { onMount } from 'svelte';

	const modalStore = getModalStore();

	const toastStore = getToastStore();

	// Form Data
	const formData: UserSettings = get(userSettings);

	onMount(() => {
		trainInit(toastStore);
	});

	// We've created a custom submit function to pass the response and close the modal.
	function onFormSubmit(): void {
		if ($modalStore[0].response) $modalStore[0].response(formData);
		userSettings.set(formData);
		modalStore.close();
	}

	function onFormSubmitTrain(): void {
		if ($modalStore[0].response) $modalStore[0].response(formData);
		userSettings.set(formData);
		sendTrainMessage();
	}

	// Base Classes
	const cBase = 'card p-4 w-modal shadow-xl space-y-4';
	const cHeader = 'text-2xl font-bold';
	const cForm = 'border border-surface-500 p-4 space-y-4 rounded-container-token';
	let tabSet: number = 0;
	const maxBatchSize: number = 500;
	const minBatchSize: number = 10;
	const maxMaxThreads: number = 10;
	const minMaxThreads: number = 1;
</script>

<!-- @component This example creates a simple form modal. -->

{#if $modalStore[0]}
	<div class="modal-example-form {cBase}">
		<header class={cHeader}>{$modalStore[0].title ?? '(title missing)'}</header>
		<!-- <article>{$modalStore[0].body ?? '(body missing)'}</article> -->
		<!-- Enable for debugging: -->
		<form class="modal-form {cForm}">
			<TabGroup>
				<Tab bind:group={tabSet} name="Simple Training" value={0}><span>Basic Training</span></Tab>
				<Tab bind:group={tabSet} name="Other" value={1}><span>Other</span></Tab>
				<!-- <Tab bind:group={tabSet} name="tab3" value={2}><span></span></Tab> -->
				<!-- Tab Panels --->
				<svelte:fragment slot="panel">
					{#if tabSet === 0}
						<label for="trainingMethod" class="label">
							<span>Training method</span>
							<RadioGroup>
								<RadioItem
									bind:group={formData.trainingBasic.method}
									name="simpleTrainingSimple"
									value={'simple'}><span>Simple Training</span></RadioItem
								>
								<RadioItem
									bind:group={formData.trainingBasic.method}
									name="simpleTrainingCombination"
									value={'combination'}><span>Combinations Training</span></RadioItem
								>
								<RadioItem
									bind:group={formData.trainingBasic.method}
									name="simpleTrainingPermutation"
									value={'permutation'}><span>Permutations Training</span></RadioItem
								>
							</RadioGroup>
						</label>
						<div class="mt-3">
							<RangeSlider
								name="batchSize"
								bind:value={formData.trainingBasic.batchSize}
								max={maxBatchSize}
								min={minBatchSize}
								step={10}
								ticked
							>
								<div class="flex justify-between items-center">
									<div class="font-bold">Batch size</div>
									<div class="text-xs">{formData.trainingBasic.batchSize} / {maxBatchSize}</div>
								</div>
							</RangeSlider>
						</div>
						<div class="mt-3">
							<RangeSlider
								name="maxThreads"
								bind:value={formData.trainingBasic.maxThreads}
								max={maxMaxThreads}
								min={minMaxThreads}
								step={1}
								ticked
							>
								<div class="flex justify-between items-center">
									<div class="font-bold">Max threads</div>
									<div class="text-xs">{formData.trainingBasic.maxThreads} / {maxMaxThreads}</div>
								</div>
							</RangeSlider>
						</div>
						<div class="mt-3">
							<button class="btn {parent.buttonPositive}" on:click={onFormSubmitTrain}>Train</button
							>
						</div>
					{:else if tabSet === 1}
						(tab panel 2 contents)
						<!-- {:else if tabSet === 2}
						(tab panel 3 contents) -->
					{/if}
				</svelte:fragment>
			</TabGroup>
			<!-- <aside class="alert">
				<div class="alert-message">
					<p>Right click to paste</p>
				</div>
				<div class="alert-actions">
					<SlideToggle name="rightClickPaste" bind:checked={formData.rightClickPaste} />
				</div>
			</aside> -->
		</form>

		<slot />

		<footer class="modal-footer {parent.regionFooter}">
			<button class="btn {parent.buttonNeutral}" on:click={parent.onClose}
				>{parent.buttonTextCancel}</button
			>
			<button class="btn {parent.buttonPositive}" on:click={onFormSubmit}>Save</button>
		</footer>
	</div>
{/if}
