<script>
    import Task from './Task.svelte';
    import { dndzone } from 'svelte-dnd-action';
    import { flip } from 'svelte/animate';
    import { api_host, csrf_tok, flash_message, request } from '../app_store';
    import { active_project } from './project_store';
    import { afterUpdate } from 'svelte';

    export let section;
    export let name = "";
    export let sectionID = "";
    export let items = [];
    let newTaskID = -1;
    let editing = false;
    let newSectionName = name;
    let sectionElement;
    let scrollSection = false;
    let scrollWindow = false;
    let unlockDelete = false;

    const flipDurationMs = 300;
    let dragging;
    $: dragDisabled = !dragging;


    afterUpdate(()=>{
        if (scrollWindow) {
            window.scrollTo(0,document.body.scrollHeight);
            scrollWindow = false;
        }
        if (scrollSection) {
            sectionElement.scrollTo(0, sectionElement.scrollHeight);
            scrollSection = false;
        }
    });

    function addTask() {
        scrollWindow = true;
        scrollSection = true;
        items.push({ id:newTaskID, startEdit:true, details: "", section_id: sectionID, position: items.length });
        items = items;
        newTaskID--;
    }

    async function renameSection() {
        let section_updates = {
            name: newSectionName,
            active: true
        };
        const res = await $request($api_host + "/section/" + sectionID  , {
                credentials: "include",
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': $csrf_tok
                },
                body: JSON.stringify(section_updates)
            });
            if(res.status === 200) {          
                name=newSectionName;
                editing = false;
                $flash_message = ["success", "Renamed section."]
            }
            else {
                $flash_message = ["failure", "Failed to rename section."]
            };
    }

    async function updateArchive(active) {
        let section_updates = {
           // position: position,
            active: active
        };
        const res = await $request($api_host + "/section/" + sectionID  , {
                credentials: "include",
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': $csrf_tok
                },
                body: JSON.stringify(section_updates)
            });
            if(res.status === 200) {    
                //section.position = position;
                section.active = active;      
                editing = false;
            };
    }

    async function patchTaskPosition(task_id,task_updates) {
        const res = await $request($api_host + "/task/" + task_id  , {
                credentials: "include",
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': $csrf_tok
                },
                body: JSON.stringify(task_updates)
            });
            if(res.status === 200) {
                $flash_message = ["success",""]
            }
            else {
                $flash_message = ["failure", "Failed to update task positions."]
            }
    }

    async function deleteSection() {
        let data = {
            position: $active_project.sections.length - 1
        }
        const res = await $request($api_host + "/section/" + sectionID  , {
                credentials: "include",
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': $csrf_tok
                },
                body: JSON.stringify(data)
            });
            if(res.status === 200) {
                let index = $active_project.sections.findIndex(i=>i.id === sectionID);
                $active_project.sections.splice(index, 1)
                for(let i = 0; i < $active_project.sections.length; i ++) {
                    $active_project.sections[i].position = i;
                }
                $active_project.sections = $active_project.sections
                $flash_message = ["success", "Section was successfully deleted."]
            }
            else {
                $flash_message = ["failure", "Failed to delete section."]
            }
    }

    function cancelNewTask(task_id) {
        let index = items.findIndex(i=>i.id === task_id)
        items.splice(index, 1);
        items = items;
    }

    // Used for svelte dnd
    function handleConsider(e) {
        items = e.detail.items
    }
    // Used for svelte dnd
    async function handleFinal(e) {
        items = e.detail.items;
        dragging = false;
        let dragged_id = e.detail.info.id;
        let item_index = items.findIndex(i=>i.id === dragged_id)
        if( item_index != -1) {
            if (items[item_index].section_id === sectionID && items[item_index].position === item_index) {
                // Task has not moved so don't patch
                return;
            }
            items[item_index].section_id = sectionID;
            let task_updates = {
                section_id: sectionID,
                position: item_index,
                active: true,
            };
            patchTaskPosition(items[item_index].id, task_updates);
        }
        for(let i = 0; i < items.length; i++) {
            items[i].position = i;
        }
        //keep order when moving section
        section.tasks = items;
    }

    // Used for svelte dnd
    const startDrag = (e) => {
        e.preventDefault();
        dragging = true;
    };

    // Used for svelte dnd
    const stopDrag = () => {
        dragging = false;
    }
</script>
<div style="background-color:{section.active ? 'slategrey' : 'crimson'};color:white;border-radius: 0em 0em 1em 1em;">
    <div class="row ml-1">
        {#if section.active}
        {#if !editing} 
            <h4 class="ml-1 mb-1">
                {name}
                <span type="button" on:click={()=>editing=true}>
                    <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-pencil-square" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                        <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456l-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                        <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                    </svg>
                </span>

            </h4>
            <div class="col" align="right">
                <button type="button" class="btn-sm btn-light m-1" on:click={addTask}>New Item</button>
            </div>
        {/if}
        {#if editing}
            <div class="col m-0 p-0">
                <input type="text" size="20" class="form-control-sm ml-1"bind:value={newSectionName}>
                <button type="button" class="btn-sm btn-light mt-1" on:click={renameSection}>Rename</button>
                <button type="button" class="btn-sm btn-light mr-1" on:click={()=>editing=false}>Cancel</button>
                <div>
                    <button type="button" class="btn-sm btn-danger m-1" on:click={()=>updateArchive(false)}>Archive</button>
                </div> 
            </div>
        {/if}
        {:else}
        <h4 class="ml-1 mb-1"> {name}</h4>
        <div class="col" align="right">
            <button type="button" class="btn-sm btn-light m-1" on:click={()=>updateArchive(true)}>Unarchive</button>
        </div>
        {/if}
    </div>
    <section class="section col p-1" style="background-color: {section.active ? 'slategrey' : 'crimson'}"
        use:dndzone={{items, dragDisabled, flipDurationMs}} 
        on:consider={handleConsider} 
        on:finalize={handleFinal}
        bind:this={sectionElement}>
        {#each items as task(task.id)}
        <div animate:flip="{{duration: flipDurationMs}}">
            <div class="grip mt-1" on:mousedown={startDrag} on:touchstart={startDrag} on:mouseup={stopDrag} on:touchend={stopDrag}></div>
            <Task task={task} startEdit={task.startEdit} cancelNewTask={cancelNewTask}/>
        </div>
        {/each}
        
    </section>
    {#if !section.active}
    <div class="p-1" style="background-color: rgb(115, 6, 25);border-radius: 0em 0em 1em 1em;" align="center">
    <div class="form-check form-check-inline">
        <label class="form-check-label" for="inlineCheckbox1">Delete Section:&nbsp;</label>
        <input class="form-check-input" type="checkbox" id="deleteCheck" bind:checked={unlockDelete}>
    </div>
    <button class="btn-sm btn-danger" hidden={!unlockDelete} on:click={deleteSection}>Delete Section</button>
    </div>
    {/if}
</div>

<style>

    .grip {
        border-radius: 1em 1em 0em 0em;
        cursor: grab;
        width: 100%;
        height: 1em;
        background-color: lightgray;
    }
    .section {
        max-width: 20em;
        min-width: 20em;
        min-height: 4em;
        max-height: calc(100vh - 225px);
        overflow-y: auto;
        /*background-color: {section.active ? 'slategrey' : 'crimson'};*/
        color: white;
        align-self: flex-start;
        border-radius: 0em 0em 1em 1em;
        
    }
</style>