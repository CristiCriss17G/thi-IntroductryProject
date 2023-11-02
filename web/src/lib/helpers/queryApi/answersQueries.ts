import { answers } from '$lib/stores/answers';

export async function getAnswers() {
	// const res = await fetch('/api/answers');
	const res = await fetch('http://localhost:8010/answers');
	const json = await res.json();
	const resAnswersShort = json.answers;
	answers.set(resAnswersShort);
	const query = `?limit=${json.total}`;
	const resAnswersLong = await fetch(`http://localhost:8010/answers${query}`);
	const jsonAnswersLong = await resAnswersLong.json();
	answers.set(jsonAnswersLong.answers);
}
