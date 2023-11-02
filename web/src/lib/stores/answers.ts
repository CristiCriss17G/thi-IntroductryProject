import { writable } from 'svelte/store';
import type { Answer } from '$lib/types/answer';
import type { Writable } from 'svelte/store';

export const answers: Writable<Answer[]> = writable([]);
