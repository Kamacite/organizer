<script>
    
    import { api_host, csrf_tok, flash_message, request } from '../app_store';
    import { active_project } from './project_store';
    import Section from './Section.svelte';
    import { dndzone } from 'svelte-dnd-action';
    import { flip } from 'svelte/animate';
    import ProjectSettings from './ProjectSettings.svelte';
    import { afterUpdate, onDestroy } from 'svelte';

    let new_name = "";
    let show_form = false;
    let show_archived = false;
    let show_settings = false;
    let all_sections_archived = true;
    const flipDurationMs = 300;
    let dragging;
    $: dragDisabled = !dragging;
    let id = -1;
    let section_container;
    let scroll_element = false;

    $: if($active_project.id != id) {
        show_archived = false;
        show_settings = false;
        id = $active_project.id
    }

    $: if($active_project) {
        for(let i = 0; i < $active_project.sections.length; i++) {
            if($active_project.sections[i].active) {
                all_sections_archived = false;
                break;
            }
        }
    }

    afterUpdate(()=>{
        if (scroll_element) {
            section_container.scrollTo(section_container.scrollHeight, 0);
            scroll_element = false;
        }
    });

    async function newSection() {
        let new_section = {
            name: new_name,
            position: $active_project.sections.length ? $active_project.sections.length : 0
        };
        const res = await $request($api_host + "/project/" + $active_project.id, {
            credentials: "include",
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': $csrf_tok
            },
            body: JSON.stringify(new_section)
        });
        if(res.status === 200) {
            scroll_element = true;
            $active_project.sections.push(await res.json());
            $active_project.sections = $active_project.sections.sort((a,b)=> a.position - b.position);
            new_name = "";
            $flash_message = ["success", "New section successfully added."];
        }
        else {
            $flash_message = ["failure", "Failed to add new section"];
        }
    }

    async function patchSectionPosition(section_id,section_updates) {
        const res = await $request($api_host + "/section/" + section_id  , {
                credentials: "include",
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': $csrf_tok
                },
                body: JSON.stringify(section_updates)
            });
            if(res.status === 200) {
                $flash_message = ["success", ""];
            }
            else {
                $flash_message = ["failure", "Failed to update section positions."]
            }
    }

    function closeProject() {
        $active_project = false;
        show_archived = false;
        show_settings = false;
        show_form = false;
    }

    function handleConsider(e) {
        $active_project.sections = e.detail.items
    }

    function handleFinal(e) {
        $active_project.sections = e.detail.items
        dragging = false;
        let dragged_id = e.detail.info.id;
        let item_index = $active_project.sections.findIndex(i=>i.id === dragged_id);
        if($active_project.sections[item_index].position === item_index) {
            return;
        }
        let s_updates = { position: item_index};
        patchSectionPosition(dragged_id, s_updates)
        for(let i = 0; i < $active_project.sections.length; i ++) {
            $active_project.sections[i].position = i;
        }
    }

    const startDrag = (e) => {
        e.preventDefault();
        dragging = true;
    };

    const stopDrag = () => {
        dragging = false;
    }

</script>

{#if $active_project}
<div class="container-fluid project p-0 justify-content-center">
    <div class="row m-1">
        <h2>{$active_project.name} |</h2>
        <span class="new-section m-1">
            {#if !show_form}
            <button class="btn-sm btn-outline-secondary m-1" hidden={show_settings} on:click={()=>show_form=!show_form}>Add Section</button>
            {:else}
            <form class="form-row p-1" on:submit|preventDefault={newSection}>
                <div class="col-auto">
                    <input class="form-control-sm" id="project-title" type="text" bind:value={new_name} placeholder="Section name...">
                </div>
                <div class="col-auto">
                    <button class="btn-sm btn-outline-secondary" type="submit">Add</button>
                </div>
                <div class="col-auto">
                    <button class="btn-sm btn-outline-secondary" on:click={()=>show_form=!show_form}>Cancel</button>  
                </div>
            </form>
            {/if}
        </span>
        <div class="col" align="right">
            <button class="btn-sm btn-outline-secondary mt-2"
                    hidden={show_settings}
                    style={ show_archived ? "background-color:dimgrey;color:white;": ""} 
                    on:click={()=>show_archived=!show_archived}>
                    {!show_archived ? 'View' : 'Hide'} Archived
            </button>
            <button class="btn-sm btn-outline-secondary mt-2" 
                    style={ show_settings ? "background-color:dimgrey;color:white;": ""} 
                    on:click={()=>show_settings=!show_settings}>
                    {!show_settings ? '' : 'Close '}Settings
            </button>
            <button class="col-auto btn-sm btn-outline-danger m-2" on:click={closeProject}>Close Project</button>
        </div>
    </div>
    {#if show_settings}
    <ProjectSettings/>
    {:else}
    {#if $active_project.sections.length > 0 && (!all_sections_archived || show_archived)}
    <div class="row sections m-auto" 
        use:dndzone={{items:$active_project.sections, dragDisabled, flipDurationMs, type:'section'}} 
        on:consider={handleConsider} 
        on:finalize={handleFinal}
        bind:this={section_container}>
        {#each $active_project.sections as sect(sect.id)}
        <div class="section m-0" animate:flip="{{duration: flipDurationMs}}">
            {#if sect.active || show_archived}
            <div class="m-1">
                <div class="grip" on:mousedown={startDrag} on:touchstart={startDrag} on:mouseup={stopDrag} on:touchend={stopDrag}></div>
                <Section bind:section={sect} name={sect.name} sect_id={sect.id} items={sect.tasks.sort( (a,b) => a.position - b.position )}/>
            </div>
                
            {/if}
        </div>
        {/each}        
    </div>
    {/if}
    {/if}
</div>
{/if}

<style>
    
    .project {
        align-items: flex-start;
    }

    .new-section {
        text-align: center ;
        min-height: 2.5em;
    }

    .sections {
        overflow-x: auto;
        flex-wrap: nowrap;
    }

    @media (max-width: 768px) {
		.sections {
			max-width: none;
            flex-wrap: wrap;
		}
	}
    .grip {
        border-radius: 1em 1em 0em 0em;
        cursor: grab;
        height: 1em;
        background-color: lightgray;
    }
</style>