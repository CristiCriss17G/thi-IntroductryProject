import { messages, loadingMessages } from '$lib/stores/chatInterface/chatInputStore';
import type { ChatMessage } from '$lib/types/chatMessage';
import type { ToastStore, ToastSettings } from '@skeletonlabs/skeleton';

let toastStore: ToastStore;

export async function sendMessage(message: string) {
	const query = `/api/chat?question=${message}`;
	// const query = `http://localhost:8010/chat?question=${message}`;
	try {
		loadingMessages.set(true);
		const response = await fetch(query);
		const data = await response.text();
		const newMessage: ChatMessage = {
			content: data,
			timestamp: new Date(),
			role: 'bot'
		};
		messages.update((messages) => [...messages, newMessage]);
		loadingMessages.set(false);
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
	// Subscribe to the store and if the last message is from the user, send it to the API
	messages.subscribe((messages) => {
		if (messages.length === 0) {
			return;
		}
		const lastMessage = messages[messages.length - 1];
		if (lastMessage.role === 'user') {
			sendMessage(lastMessage.content);
		}
	});
}
