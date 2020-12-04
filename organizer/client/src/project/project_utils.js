import { active_project, project_list } from './project_store.js';

export function projectCleanUp() {
    active_project.set(false);
    project_list.set([]);
}