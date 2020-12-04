<script>
import { api_host, csrf_tok, flash_message, request } from "../app_store";

import { active_project, project_list } from "./project_store";



let new_name = "";
let new_details = "";
let backup_name = "";
let backup_details = "";
backup_name = $active_project.name;
backup_details = $active_project.details;
new_name = $active_project.name;
new_details = $active_project.details;

async function updateName() {
    let data = {
        name: new_name
    };
    const res = await $request($api_host + "/project/" + $active_project.id, {
            method: 'PATCH',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': $csrf_tok
            },
            body: JSON.stringify(data)
    });
    if (res.status === 200) {
        $active_project.name = new_name;
        backup_name = new_name;
        $active_project.selector.name = new_name
        $project_list = $project_list
        $flash_message = ["success", "Project name was updated successfully."]
    }   
    else {
        $flash_message = ["failure", "Project name failed to update."]
    }    
}

async function updateDetails() {
    let data = {
        details: new_details
    };
    const res = await $request($api_host + "/project/" + $active_project.id, {
            method: 'PATCH',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': $csrf_tok
            },
            body: JSON.stringify(data)
    });
    if (res.status === 200) {
        $active_project.details = new_details;
        backup_details = new_details;
        $active_project.selector.details = new_details
        $project_list = $project_list
        $flash_message = ["success", "Project details were updated successfully."]
    }   
    else {
        $flash_message = ["failure", "Project details failed to update."]
    }
}

async function archiveProject() {
    let data = {
        active: false
    };
    const res = await $request($api_host + "/project/" + $active_project.id, {
            method: 'PATCH',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': $csrf_tok
            },
            body: JSON.stringify(data)
    });
    if (res.status === 200) {
        let index = $project_list.findIndex(i=>i.id === $active_project.id);
        $project_list[index].active = false;
        $active_project = false;
        $project_list = $project_list;
        $flash_message = ["success", "Project has been archived."]
    }   
    else {
        $flash_message = ["failure", "Project did not archive."]
    }
}

async function unarchiveProject() {
    let data = {
        active: true
    };
    const res = await $request($api_host + "/project/" + $active_project.id, {
            method: 'PATCH',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': $csrf_tok
            },
            body: JSON.stringify(data)
    });
    if (res.status === 200) {
        let index = $project_list.findIndex(i=>i.id === $active_project.id);
        $project_list[index].active = true;
        $active_project.active = true;
        $project_list = $project_list;
        $flash_message = ["success", "Project has been unarchived."]
    }   
    else {
        $flash_message = ["failure", "Project failed to unarchived."]
    }
}

async function deleteProject() {
    const res = await $request($api_host + "/project/" + $active_project.id, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': $csrf_tok
            }
    });
    if (res.status === 200) {
        let index = $project_list.findIndex(i=>i.id === $active_project.id);
        $project_list.splice(index, 1);
        $active_project = false;
        $project_list = $project_list;
        $flash_message = ["success", "Project has been deleted."]
    }
    else {
        $flash_message = ["failure", "Project failed to delete."]
    }
}

</script>

<div class="conatiner-fluid">
    <h3 class="ml-4">Project Settings:</h3>
    <div class="row m-0" >
        <div class="col">
            <div class="d-block d-md-flex justify-content-end">
                <div class="d-block d-md-flex align-items-start">
                    <label for="name">Project Name:</label>
                    <div class="w-100 d-block d-md-none"></div>
                    <input id="name" class="setting_input" bind:value={new_name}>
                    <div class="w-100 d-block d-md-none"></div>
                    <button class="btn btn-outline-secondary" on:click={updateName}>Update</button>
                    <button class="btn btn-outline-secondary ml-1" on:click={()=>new_name=backup_name}>Cancel</button>
                </div>
            </div>
            <br>
            <span class="d-block d-md-flex justify-content-end">
                <div class="d-block d-md-flex align-items-start">
                    <label for="description">Project Description:</label>
                    <div class="w-100 d-block d-md-none"></div>
                    <textarea id="description" class="setting_input" bind:value={new_details}></textarea>
                    <div class="w-100 d-block d-md-none"></div>
                    <button class="btn btn-outline-secondary" on:click={updateDetails}>Update</button>
                    <button class="btn btn-outline-secondary ml-1" on:click={()=>new_details=backup_details}>Cancel</button>
                </div>
            </span>
            <br>
            
        </div>
        <div class="col">
            <span class="row mr-2 justify-content-center">
                <div class="d-flex align-items-start">
                    {#if $active_project.active}
                    <button class="btn btn-danger" on:click={archiveProject}>Archive</button>
                    {:else}
                    <button class="btn btn-outline-secondary" on:click={unarchiveProject}>Unarchive</button>
                    <button class="btn btn-danger ml-3" on:click={deleteProject}>Delete</button>
                    {/if}
                </div>
            </span>
        </div>
        
    </div>
</div>

<style>
    .setting_input {
        min-width: 250px;
        margin: 5px;
        margin-top: 0px;
    }
</style>