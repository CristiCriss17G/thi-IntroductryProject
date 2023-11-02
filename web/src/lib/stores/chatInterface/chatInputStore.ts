import { writable } from 'svelte/store';
import type { ChatMessage } from '$lib/types/chatMessage';

export const messages = writable<ChatMessage[]>([]);
export const loadingMessages = writable<boolean>(false);
