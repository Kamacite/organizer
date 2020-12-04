import {writable, readable} from 'svelte/store';

export const day_date = writable(0);
export const week_date = writable(0);
export const submit_day_check = writable(0);
export const submit_week_check = writable(0);
export const edit_data = writable(0);
export const editing = writable(false);
export const inputing = writable(false);
export const new_edit = writable(false);


