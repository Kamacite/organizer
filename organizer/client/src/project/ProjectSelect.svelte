<script>

import { onMount } from 'svelte';
import { api_host, csrf_tok, request, view } from '../app_store';
import { active_project, project_list } from './project_store.js'

$: expand = false;
$: show_form = false;

let new_name = "";
let new_details = "";

let show_archived = false;

//onMount get projects and populate projects list
onMount(()=> {
    getProjects();
})

$: if (!$active_project && $view === "project") {
    expand = true;
}
else {
    expand = false;
}

async function getProjects() {
    const res = await $request($api_host + "/projects", {
            credentials: "include",
            headers: {
                'X-CSRF-TOKEN': $csrf_tok
            }
        });
    if(res.ok) {
        $project_list = await res.json();
    }
}

$: if($project_list != []) {
    $project_list = $project_list.sort((a,b)=> {
            if(a.name > b.name) {
                return 1
            }
            if(a.name < b.name) {
                return -1
            }
            else {
                return 0
            }
        });
}

async function newProject() {
    let new_proj = {
        name: new_name,
        details: new_details
    }
    let req_object = {
            credentials: "include",
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': $csrf_tok
            },
            body: JSON.stringify(new_proj)
        };
    //Get ID from post res and add to project object to store in dev
    const res = await $request($api_host + "/projects", req_object);
    if(res.status === 200) {
        let res_data = await res.json()
        $project_list.push({
            id: res_data.id,
            name:res_data.name,
            details: res_data.details,
            active: true
        });
        new_name="";
        new_details="";
        show_form = false;
        $project_list = $project_list;
        
    }
    
}

async function selectProject(project) {
    //update some active_project store
    const res = await $request($api_host + "/project/" + project.id, {
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': $csrf_tok
            }
    });
    if(res.status === 200 ) {
        $active_project = await res.json();
        $active_project.sections = $active_project.sections.sort((a,b)=> a.position - b.position);
        $active_project.selector = project;
        expand = false;
    }
}

</script>

<div class="container-fluid projects p-1">
    <button class="btn-sm btn-light w-100" on:click={()=>expand=!expand}>Projects</button>
    {#if expand}
    <div class="row m-0 mt-1">
        <h2>My Projects |</h2>
        <button class="btn-sm btn-light m-1" 
                style={ show_archived ? "background-color:dimgrey;color:white;": ""} 
                on:click={()=>show_archived=!show_archived}>
            {!show_archived ? 'View' : 'Hide'} Archived
        </button>
    </div>
    
    <div class="row m-0 project-list">
        {#each $project_list as proj }
            {#if proj.active}
            <div class="col project mr-2 mt-2" on:click={()=>selectProject(proj)}>
                <h4>{proj.name}</h4>
                <p>{proj.details}</p>
            </div>
            {/if}
        {/each}
        <div class="col project mr-2 mt-2">
            {#if !show_form}
                <div on:click={()=>show_form=true}>
                    <svg width="10.5em" height="10.5em" viewBox="0 0 16 16" class="bi bi-plus" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                    </svg>
                </div>
            {:else}
            <form class="" on:submit|preventDefault={newProject}>
                <div class="form-group">
                    <input class="form-control mt-1" id="project-title" type="text" bind:value={new_name} placeholder="Project name...">
                    <textarea class="form-control mt-1 mb-1" id="project-details" bind:value={new_details} placeholder="Project details..."></textarea>
                    <button class="btn btn-light" type="submit">Create</button>
                    <button class="btn btn-light" on:click={()=>show_form=false}>Cancel</button>  
                </div>
            </form>
            {/if}
        </div>
    </div>
    <div class="row m-0">
        {#if show_archived}
        {#each $project_list as proj }
            {#if !proj.active}
            <div class="col archived-project mr-2 mt-2" on:click={()=>selectProject(proj)}>
                <h4>{proj.name}</h4>
                <p>{proj.details}</p>
            </div>
            {/if}
        {/each}
        {/if}
    </div>
    {/if}
</div>


<style>
    .projects{
        color: white;
        background-color: slategrey;
        
    }

    @media screen and (max-width: 576px) {
        .project-list {
            justify-content: center;
        }
    }

    .project:hover {
        background-color: steelblue;
    }

    .project{
        cursor: pointer;
        text-align: center;
        justify-content: center;
        color: white;
        background-color:  darkslategray;
        min-width: 15em;
        max-width: 15em;
        min-height: 10.5em;
        max-height: 10.5em;
    }
    .archived-project{
        cursor: pointer;
        text-align: center;
        justify-content: center;
        color: white;
        background-color:  darkred;
        min-width: 15em;
        max-width: 15em;
        min-height: 10.5em;
        max-height: 10.5em;
    }
    .archived-project:hover {
        background-color: crimson;
    }
</style>