import { localStorageStore } from '@skeletonlabs/skeleton';
import { get } from 'svelte/store';
import type { UserSettings } from '$lib/types/userSettings';
import type { Writable } from 'svelte/store';

const defaultSettings: UserSettings = {
	theme: 'light',
	trainingBasic: {
		method: 'simple',
		batchSize: 100,
		maxThreads: 5
	}
};

export function checkOrUpdateUserSettings(userSettingsParam: UserSettings) {
	const settings = get(userSettings);
	if (settings.theme !== userSettingsParam.theme) {
		userSettings.update((settings) => ({ ...settings, theme: userSettingsParam.theme }));
	}
	if (settings.trainingBasic.method !== userSettingsParam.trainingBasic.method) {
		userSettings.update((settings) => ({
			...settings,
			trainingBasic: {
				...settings.trainingBasic,
				method: userSettingsParam.trainingBasic.method
			}
		}));
	}
	if (settings.trainingBasic.limit !== userSettingsParam.trainingBasic.limit) {
		userSettings.update((settings) => ({
			...settings,
			trainingBasic: { ...settings.trainingBasic, limit: userSettingsParam.trainingBasic.limit }
		}));
	}
	if (settings.trainingBasic.batchSize !== userSettingsParam.trainingBasic.batchSize) {
		userSettings.update((settings) => ({
			...settings,
			trainingBasic: {
				...settings.trainingBasic,
				batchSize: userSettingsParam.trainingBasic.batchSize
			}
		}));
	}
	if (settings.trainingBasic.maxThreads !== userSettingsParam.trainingBasic.maxThreads) {
		userSettings.update((settings) => ({
			...settings,
			trainingBasic: {
				...settings.trainingBasic,
				maxThreads: userSettingsParam.trainingBasic.maxThreads
			}
		}));
	}
}

export const userSettings: Writable<UserSettings> = localStorageStore<UserSettings>(
	'userSettings',
	defaultSettings
);
