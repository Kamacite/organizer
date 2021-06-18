<script>

import { api_host, csrf_tok, flash_message, request, view } from "../app_store";
import { submit_day_check, submit_week_check } from "../schedule/schedule_store";
import { active_project } from "./project_store";
import Editor from "../editor/Editor.svelte";

export let task = {};
export let startEdit = false;
export let cancelNewTask;
let hidden = false;
let newDate;
let newTime;
$: editable = startEdit;
$: scheduling= false;
let editor;

async function edit() {
    editable = true;
    editor.startEdit();
}

function cancel() {
    editable = false;
    editor.cancelEdit();
    if (task.startEdit) {
        //hidden = true;
        cancelNewTask(task.id);
    }
    
}

//This will also post task updates/create new ones
async function save() {
    if (task.id <= -1) {
        let new_task = {
            details: editor.getSanitizedContent(),
            position: task.position
        };
        const res = await $request($api_host + "/section/" + task.section_id  , {
            credentials: "include",
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': $csrf_tok
            },
            body: JSON.stringify(new_task)
        });
        if(res.status === 200) {
            let task_info = await res.json();
            task.id = task_info.id;
            task.details = new_task.details;
            task.startEdit = false;
            editable = false;
            editor.stopEdit();
            $flash_message = ["success",""]
        }
        else {
            $flash_message = ["failure",""]
        }
    }
    else {
        let task_updates = {
            details: editor.getSanitizedContent(),
            active: true
        };
        const res = await $request($api_host + "/task/" + task.id  , {
            credentials: "include",
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': $csrf_tok
            },
            body: JSON.stringify(task_updates)
        });
        if(res.status === 200) {
            task.details = task_updates.details;
            editable = false;
            editor.stopEdit()
            $flash_message = ["success",""]
        }
        else {
            $flash_message = ["failure",""]
        }
    }
}


async function scheduleTask() {
    let schedule_item = {
        title: $active_project.name,
        item_date:newDate,
        item_time:newTime,
        details: editor.getSanitizedContent(),
        active:true,
        reoccuring: false
    }
    let req_object = {
        method: 'PUT',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': $csrf_tok
        },
        body: JSON.stringify(schedule_item)
    }
    let url = $api_host +"/item"
    const res = await $request(url, req_object);
	if (res.ok) {
        
        $flash_message = ["success","New item was entered successfully."]
        scheduling=false;
        //Trigger check to see if either day or week need to be reloaded
        if($view != "project") {
            $submit_day_check = null
            $submit_week_check = null
            $submit_day_check = newDate
            $submit_week_check = newDate
        }
        
	} else {
        $flash_message = ["failure","Failed to enter new item."]
        throw new Error(res.message)
    }
}
</script>

{#if !hidden} 
<div class="task d-block p-0">
    <Editor bind:this={editor} editable={editable} initialContent={task.details ? task.details : ""}/>
    {#if scheduling}
        <div class="row m-1">
            <div class="col p-0" align="center">
                <input class="form-control-sm" id="item_date" type="date" bind:value={newDate}>
            </div>
            <div class="col p-0" align="right">
                <input class="form-control-sm w-100" id="item_time" type="time" bind:value={newTime}>
            </div>
        </div>
    {/if}
    <div class="row m-0">
        {#if !editable && !scheduling}
        <button class="col tl-button p-0" align="center"  on:click={edit}>Edit</button>
        <button class="col tr-button p-0" align="center"  on:click={()=>scheduling=true}>Schedule</button>
        {:else if scheduling}
        <button class="col tl-button p-0" align="center" on:click={scheduleTask}>Schedule</button>
        <button class="col tr-button p-0" align="center" on:click={()=>scheduling=false}>Cancel</button>
        {:else}
        <button class="col tl-button p-0" align="center" on:click={save}>Save</button>
        <button class="col tr-button p-0" align="center" on:click={cancel}>Cancel</button>
        {/if}
    </div>
    
</div>
{/if}
<style>
    .task {
        color: black;
        background-color: snow;
        border-radius: 0em 0em 1em 1em;
    }
    .tl-button {
        margin-right: 1px;
        background-color: snow;
        border-radius: 0em 0em 0em 1em;
    }
    .tr-button {
        margin-left: 1px;
        background-color: snow;
        border-radius: 0em 0em 1em 0em;
    }
    .tl-button:hover {
        background-color: lightgrey;
        
    }
    
    .tr-button:hover {
        background-color: lightgrey;
    }
    .tl-button:focus {
        outline-width: 0px;
        box-shadow: 0px 0px 0px 1px black;
    }
    .tr-button:focus {
        outline-width: 0px;
        box-shadow: 0px 0px 0px 1px black;
    }
</style>