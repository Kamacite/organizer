<script>

import { onMount, tick } from 'svelte';
import { api_host, csrf_tok, request, view } from '../app_store';
import { active_project, project_list } from './project_store.js'

$: expanded = false;
$: showForm = false;

let newProjectName = "";
let newProjectDetails = "";
let div;
let showArchived = false;

//onMount get projects and populate projects list
onMount(()=> {
    getProjects();
})

$: if (!$active_project && $view === "project") {
    expanded = true;
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
        name: newProjectName,
        details: newProjectDetails
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
        newProjectName="";
        newProjectDetails="";
        showForm = false;
        $project_list = $project_list;   
    }    
}

async function expand() {
    expanded=!expanded;
    if(expanded && $view != 'project') {
        scrollSelect();
    }
}
async function scrollSelect(options={behavior:'smooth', block:'start'}) {
    await tick();
    div.scrollIntoView(options);
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
        $active_project.scroll = true;
        scrollSelect({behavior:'smooth', block:'start'});
        expanded = false;
    }
}

</script>

<div class="container-fluid projects p-1" bind:this={div}>
    <button id="show-projects-btn" class="btn-sm btn-light w-100" on:click={expand}>Projects</button>
    {#if expanded}
    <div class="row m-0 mt-1">
        <h2>My Projects |</h2>
        <button class="btn-sm btn-light m-1" 
                title={ showArchived ? "Hide Archives" : "Show Archives"}
                style={ showArchived ? "background-color:dimgrey;color:white;": ""} 
                on:click={()=>{showArchived=!showArchived;scrollSelect({behavior:'smooth', block:'end'})}}>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive d-flex" viewBox="0 0 16 16">
                <path d="M0 2a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1v7.5a2.5 2.5 0 0 1-2.5 2.5h-9A2.5 2.5 0 0 1 1 12.5V5a1 1 0 0 1-1-1V2zm2 3v7.5A1.5 1.5 0 0 0 3.5 14h9a1.5 1.5 0 0 0 1.5-1.5V5H2zm13-3H1v2h14V2zM5 7.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5z"/>
                </svg>
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
            {#if !showForm}
                <div on:click={()=>showForm=true}>
                    <svg width="10.5em" height="10.5em" viewBox="0 0 16 16" class="bi bi-plus" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                    </svg>
                </div>
            {:else}
            <form class="" on:submit|preventDefault={newProject}>
                <div class="form-group">
                    <input class="form-control mt-1" id="project-title" type="text" bind:value={newProjectName} placeholder="Project name...">
                    <textarea class="form-control mt-1 mb-1" id="project-details" bind:value={newProjectDetails} placeholder="Project details..."></textarea>
                    <button class="btn btn-light" type="submit">Create</button>
                    <button class="btn btn-light" on:click={()=>showForm=false}>Cancel</button>  
                </div>
            </form>
            {/if}
        </div>
    </div>
    <div class="row m-0 project-list">
        {#if showArchived}
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
    
    #show-projects-btn {
        border-radius: 1em 1em 1em 1em;
    }
    #show-projects-btn:focus {
        outline-width: 0px;
        box-shadow: 0px 0px 1px 1px black;
    }

    .projects{
        color: white;
        background-color: slategrey;
        border-radius: 1em 1em 1em 1em;
        scroll-margin-top: 4em;
    }

    @media screen and (max-width: 576px) {
        .project-list {
            justify-content: center;
        }
    }

    .project:hover {
        background-color: rgb(15, 32, 32);
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
        border-radius: 1em 1em 1em 1em;
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
        border-radius: 1em 1em 1em 1em;
    }
    .archived-project:hover {
        background-color: rgb(87, 0, 0);
    }
</style>