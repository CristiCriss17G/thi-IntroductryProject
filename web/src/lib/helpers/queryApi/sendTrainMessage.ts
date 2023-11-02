import { userSettings } from '$lib/stores/userSettings';
import { get } from 'svelte/store';
import type { ToastStore, ToastSettings } from '@skeletonlabs/skeleton';

let toastStore: ToastStore;

export async function sendTrainMessage() {
	const currentUserSettings = get(userSettings);
	let queryString = `?method=${currentUserSettings.trainingBasic.method}&batch_size=${currentUserSettings.trainingBasic.batchSize}&max_threads=${currentUserSettings.trainingBasic.maxThreads}`;
	if (currentUserSettings.trainingBasic.limit) {
		queryString += `&limit=${currentUserSettings.trainingBasic.limit}`;
	}
	const query = `/api/train/simple${queryString}`;
	// const query = `http://localhost:8010/train/simple${queryString}`;
	try {
		const response = await fetch(query, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			}
		});
		const data = await response.text();
		const toastSettings: ToastSettings = {
			message: data,
			background: 'variant-filled-success',
			timeout: 2000
		};
		toastStore.trigger(toastSettings);
	} catch (error) {
		console.error(error);
		const toastSettings: ToastSettings = {
			message: 'Error: server not available - did you forget "python server.py" on server machine?',
			background: 'variant-filled-error',
			timeout: 2000
		};
		toastStore.trigger(toastSettings);
	}
}

export function init(toastStoreInit: ToastStore) {
	toastStore = toastStoreInit;
}
