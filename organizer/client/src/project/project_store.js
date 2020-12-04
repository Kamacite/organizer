import {writable} from 'svelte/store';

export const active_project = writable(false);
export const project_list = writable([]);