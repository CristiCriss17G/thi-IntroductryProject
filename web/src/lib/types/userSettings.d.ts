export type UserSettings = {
	theme: 'light' | 'dark';
	trainingBasic: {
		method: string;
		limit?: number;
		batchSize: number;
		maxThreads: number;
	};
};
