import { day_date, week_date, submit_day_check, submit_week_check, edit_data, editing, inputing, new_edit } from './schedule_store.js';

export function scheduleCleanUp() {
    day_date.set(null);
    week_date.set(null);
    submit_day_check.set(null);
    submit_week_check.set(null);
    edit_data.set(false);
    editing.set(false);
    inputing.set(false);
    new_edit.set(false);
}