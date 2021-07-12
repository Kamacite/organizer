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

async function deleteTask() {
    let task_details = {
        position: Number.MAX_SAFE_INTEGER
    }
    const res = await $request($api_host + "/task/" + task.id, {
        credentials: "include",
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': $csrf_tok
        },
        body: JSON.stringify(task_details)
    });
    if(res.status === 200) {
        //Get current section task is in index
        let sectionIndex = $active_project.sections.findIndex(i=>i.id === task.section_id);
        //Get task index in section
        let taskIndex = $active_project.sections[sectionIndex].tasks.findIndex(i=>i.id === task.id);
        //Remove task from that section
        $active_project.sections[sectionIndex].tasks.splice(taskIndex, 1);
        for( let i = 0; i<$active_project.sections[sectionIndex].tasks.length; i++) {
            $active_project.sections[sectionIndex].tasks[i].position = i;
        }
        $active_project.sections[sectionIndex].tasks = $active_project.sections[sectionIndex].tasks;
        $flash_message = ["success", "Task was successfully deleted."]
    }
    else {
        $flash_message = ["failure", "Failed to delete task."]
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
        <button class="col tl-button p-0" align="center" title="Edit" on:click={edit}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
            <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
            <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
            </svg>
        </button>
        <button class="col tr-button p-0" align="center" title="Schedule" on:click={()=>scheduling=true}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar-plus" viewBox="0 0 16 16">
            <path d="M8 7a.5.5 0 0 1 .5.5V9H10a.5.5 0 0 1 0 1H8.5v1.5a.5.5 0 0 1-1 0V10H6a.5.5 0 0 1 0-1h1.5V7.5A.5.5 0 0 1 8 7z"/>
            <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
              </svg>
        </button>
        {:else if scheduling}
        <button class="col tl-button p-0" align="center" title="Confirm Scheduling" on:click={scheduleTask}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar-check" viewBox="0 0 16 16">
            <path d="M10.854 7.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
            <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
            </svg>
        </button>
        <button class="col tr-button p-0" align="center" title="Cancel Scheduling" on:click={()=>scheduling=false}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
            <path d="M1.293 1.293a1 1 0 0 1 1.414 0L8 6.586l5.293-5.293a1 1 0 1 1 1.414 1.414L9.414 8l5.293 5.293a1 1 0 0 1-1.414 1.414L8 9.414l-5.293 5.293a1 1 0 0 1-1.414-1.414L6.586 8 1.293 2.707a1 1 0 0 1 0-1.414z"/>
            </svg>
        </button>
        {:else} <!-- Editing task details -->
        <button class="col tl-button p-0" align="center" title="Save" on:click={save}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-save" viewBox="0 0 16 16">
            <path d="M2 1a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H9.5a1 1 0 0 0-1 1v7.293l2.646-2.647a.5.5 0 0 1 .708.708l-3.5 3.5a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L7.5 9.293V2a2 2 0 0 1 2-2H14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h2.5a.5.5 0 0 1 0 1H2z"/>
            </svg>
        </button>
        <button class="col t-button p-0" align="center" title="Cancel" on:click={cancel}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
            <path d="M1.293 1.293a1 1 0 0 1 1.414 0L8 6.586l5.293-5.293a1 1 0 1 1 1.414 1.414L9.414 8l5.293 5.293a1 1 0 0 1-1.414 1.414L8 9.414l-5.293 5.293a1 1 0 0 1-1.414-1.414L6.586 8 1.293 2.707a1 1 0 0 1 0-1.414z"/>
            </svg>
        </button>
        <button class="tr-button p-0 pl-2 pr-2" align="center" style="color:red" title="Delete" on:click={deleteTask}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
            <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
            </svg>
        </button>
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
    .t-button {
        background-color: snow;
    }
    .t-button:hover {
        background-color: lightgrey;
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