<script>

import { flash_message, api_host, csrf_tok, request } from '../app_store.js'
import { day_date, inputing, submit_day_check, submit_week_check } from './schedule_store.js';
import Editor from '../editor/Editor.svelte';

let d = new Date();
//title, date, time, and details cannot be empty
let newTitle = "";
let newDate;
// the form date defaults to current selected day in day component
$: newDate = $day_date;
let newTime = "";
let editor;

async function handleSubmit() {
    let data = {
        "title":newTitle,
        "item_date":newDate,
        "item_time":newTime,
        "details":editor.getSanitizedContent(),
        "active":true,
        "reoccuring": false
    };
	const res = await $request($api_host +"/item", {
        method: 'PUT',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': $csrf_tok
        },
        body: JSON.stringify(data)
    });
	if (res.ok) {
        $flash_message = ["success","New item, " + newTitle + ", was entered successfully."]
        newTitle="";
        editor.clearContent();
        //Trigger check to see if either day or week need to be reloaded
        submit_day_check.set(null)
        submit_day_check.set(newDate)
        submit_week_check.set(null)
        submit_week_check.set(newDate)
	} else {
        $flash_message = ["failure","Failed to enter new item."]
    }
    
}

</script>

<div class="form-block">
    <form on:submit|preventDefault={handleSubmit}>
        <div class="form-group">
            <label for="title">Title:</label>
            <input class="form-control" id="title" type="text" bind:value={newTitle}>
            <input class="form-control" id="item_date" type="date" bind:value={newDate}>
            <input class="form-control" id="item_time" type="time" bind:value={newTime}>
            <label for="item_details">Details:</label>
            <Editor bind:this={editor} initialContent={""} editable={true} autoFocus={false}/>
            <button type="submit">Submit</button>
            <button type="reset">Reset</button>
            <button on:click={()=>$inputing=false}>Cancel</button>
        </div>
    </form>
</div>


<style>
 .form-block {
    margin:auto;
    width:50%;
 }
 
 @media screen and (max-width: 576px) {
  .form-block {
    width: 100%;
  }
}
  
</style>