<script>

import { flash_message, api_host, csrf_tok, request } from '../app_store.js'
import { day_date, inputing, submit_day_check, submit_week_check } from './schedule_store.js';


let d = new Date();
//title, date, time, and details cannot be empty
let new_title = "";
let new_date;
// the form date defaults to current selected day in day component
$: new_date = $day_date;
let new_time = "";
let new_details = "";

async function handleSubmit() {
    let data = {
        "title":new_title,
        "item_date":new_date,
        "item_time":new_time,
        "details":new_details,
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
        $flash_message = ["success","New item, " + new_title + ", was entered successfully."]
        new_title="";
        new_details="";
        //Trigger check to see if either day or week need to be reloaded
        submit_day_check.set(null)
        submit_day_check.set(new_date)
        submit_week_check.set(null)
        submit_week_check.set(new_date)
	} else {
        $flash_message = ["failure","Failed to enter new item."]
    }
    
}

</script>

<div class="form-block">
    <form on:submit|preventDefault={handleSubmit}>
        <div class="form-group">
            <label for="title">Title:</label>
            <input class="form-control" id="title" type="text" bind:value={new_title}>
            <input class="form-control" id="item_date" type="date" bind:value={new_date}>
            <input class="form-control" id="item_time" type="time" bind:value={new_time}>
            <label for="item_details">Details:</label>
            <textarea class="form-control" id="item_details" bind:value={new_details}></textarea>
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