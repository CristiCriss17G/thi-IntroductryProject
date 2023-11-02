import type { ModalSettings, ModalComponent } from '@skeletonlabs/skeleton';
import UserSettingsMenu from '$lib/components/UserSettingsMenu.svelte';

export const modalComponent: ModalComponent = {
	// Pass a reference to your custom component
	ref: UserSettingsMenu
};

export const modal: ModalSettings = {
	type: 'component',
	title: 'User Settings',
	// Pass the component directly:
	component: modalComponent
};
