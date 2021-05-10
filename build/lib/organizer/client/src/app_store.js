import {writable, readable} from 'svelte/store';

export const flash_message = writable(0);
export const csrf_tok = writable(false);
export const api_host = writable("");
export const request = writable(false);
export const current_user = writable(false);
export const remember_user = writable(false);
export const view = writable("split");