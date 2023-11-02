export type ChatMessage = {
	content: string;
	timestamp: Date;
	role: 'user' | 'bot';
};
