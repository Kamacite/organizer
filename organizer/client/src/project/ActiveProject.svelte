<script>
    
    import { api_host, csrf_tok, flash_message, request } from '../app_store';
    import { active_project } from './project_store';
    import Section from './Section.svelte';
    import { dndzone } from 'svelte-dnd-action';
    import { flip } from 'svelte/animate';
    import ProjectSettings from './ProjectSettings.svelte';
    import { afterUpdate, tick } from 'svelte';

    // For adding new sections
    let newSectionName = "";
    let showForm = false;
    
    let showArchived = false;
    let showSettings = false;
    let allSectionsArchived = true;
    // Used for svelte dnd
    const flipDurationMs = 300;
    let dragging;
    $: dragDisabled = !dragging;

    let id = -1;
    let sectionContainer;
    let scrollElement = false;
    let mainDiv;

    $: if($active_project.id != id) {
        showArchived = false;
        showSettings = false;
        id = $active_project.id
    }

    // Check if all sections are archived
    $: if($active_project) {
        for(let i = 0; i < $active_project.sections.length; i++) {
            if($active_project.sections[i].active) {
                allSectionsArchived = false;
                break;
            }
        }
    }

    afterUpdate(()=>{
        if (scrollElement) {
            sectionContainer.scrollTo(sectionContainer.scrollHeight, 0);
            scrollElement = false;
        }
    });

    async function newSection() {
        let new_section = {
            name: newSectionName,
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
            scrollElement = true;
            $active_project.sections.push(await res.json());
            $active_project.sections = $active_project.sections.sort((a,b)=> a.position - b.position);
            newSectionName = "";
            $flash_message = ["success", "New section successfully added."];
        }
        else {
            $flash_message = ["failure", "Failed to add new section"];
        }
    }

    // Called after moving a section
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
        showArchived = false;
        showSettings = false;
        showForm = false;
    }

    // Used for svelte dnd
    function handleConsider(e) {
        $active_project.sections = e.detail.items
    }

    // Used for svelte dnd
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

    // Used for svelte dnd
    const startDrag = (e) => {
        e.preventDefault();
        dragging = true;
    };

    // Used for svelte dnd
    const stopDrag = () => {
        dragging = false;
    }

    async function toggleSettings() {
       showSettings = !showSettings;
       //Called on closing (note toggled showSettings first so page updates before scrolling.)
       if (!showSettings) {
            await tick();
            window.scrollTo(0,document.body.scrollHeight);
       }
    }

</script>

{#if $active_project}
<div class="container-fluid project p-0 justify-content-center" bind:this={mainDiv}>
    <div class="row m-1">
        <h2>{$active_project.name} |</h2>
        <div class="new-section m-1">
            {#if !showForm}
            <button class="btn-sm btn-outline-secondary m-1" hidden={showSettings} on:click={()=>showForm=!showForm}>Add Section</button>
            {:else}
            <form class="form-row p-1" on:submit|preventDefault={newSection}>
                <div class="col-auto">
                    <input class="form-control-sm" id="project-title" type="text" bind:value={newSectionName} placeholder="Section name...">
                </div>
                <div class="col-auto">
                    <button class="btn-sm btn-outline-primary" type="submit">
                        <!-- Plus icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg d-flex" viewBox="0 0 16 16">
                            <path d="M8 0a1 1 0 0 1 1 1v6h6a1 1 0 1 1 0 2H9v6a1 1 0 1 1-2 0V9H1a1 1 0 0 1 0-2h6V1a1 1 0 0 1 1-1z"/>
                        </svg>
                    </button>
                </div>
                <div class="col-auto">
                    <button class="btn-sm btn-outline-secondary" on:click={()=>showForm=!showForm}>
                        <!-- X icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg d-flex" viewBox="0 0 16 16">
                            <path d="M1.293 1.293a1 1 0 0 1 1.414 0L8 6.586l5.293-5.293a1 1 0 1 1 1.414 1.414L9.414 8l5.293 5.293a1 1 0 0 1-1.414 1.414L8 9.414l-5.293 5.293a1 1 0 0 1-1.414-1.414L6.586 8 1.293 2.707a1 1 0 0 1 0-1.414z"/>
                        </svg>
                    </button>  
                </div>
            </form>
            {/if}
        </div>
        <div class="p-0 pl-1" align="left">
            <button type="button" class="btn-sm btn-outline-secondary mt-2"
                    title={showArchived ? "Hide Archives": "Show Archives"}
                    hidden={showSettings}
                    style={ showArchived ? "background-color:dimgrey;color:white;": ""} 
                    on:click={()=>showArchived=!showArchived}>
                    <!-- Archive Icon -->
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive d-flex" viewBox="0 0 16 16">
                    <path d="M0 2a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1v7.5a2.5 2.5 0 0 1-2.5 2.5h-9A2.5 2.5 0 0 1 1 12.5V5a1 1 0 0 1-1-1V2zm2 3v7.5A1.5 1.5 0 0 0 3.5 14h9a1.5 1.5 0 0 0 1.5-1.5V5H2zm13-3H1v2h14V2zM5 7.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5z"/>
                    </svg>
            </button>
            <button type="button" class="btn-sm btn-outline-secondary mt-2"
                    title={showSettings? "Close Settings": "Show Settings"} 
                    style={ showSettings ? "background-color:dimgrey;color:white;": ""} 
                    on:click={toggleSettings}>
                    <!-- Gear Icon -->
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-gear d-flex" viewBox="0 0 16 16">
                    <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/>
                    <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"/>
                    </svg>
            </button>
            <button type="button" class="btn-sm btn-outline-danger mt-2"
                    title={showSettings ? "Close Settings" : "Close Project"}
                    on:click={()=>{showSettings? toggleSettings() : closeProject()}}>
                <!-- X Icon -->
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg text-danger d-flex" viewBox="0 0 16 16">
                    <path d="M1.293 1.293a1 1 0 0 1 1.414 0L8 6.586l5.293-5.293a1 1 0 1 1 1.414 1.414L9.414 8l5.293 5.293a1 1 0 0 1-1.414 1.414L8 9.414l-5.293 5.293a1 1 0 0 1-1.414-1.414L6.586 8 1.293 2.707a1 1 0 0 1 0-1.414z"/>
                </svg>
            </button>
        </div>
        
    
    </div>
    {#if showSettings}
    <ProjectSettings/>
    {:else}
    {#if $active_project.sections.length > 0 && (!allSectionsArchived || showArchived)}
    <div class="row sections m-auto" 
        use:dndzone={{items:$active_project.sections, dragDisabled, flipDurationMs, type:'section'}} 
        on:consider={handleConsider} 
        on:finalize={handleFinal}
        bind:this={sectionContainer}>
        {#each $active_project.sections as sect(sect.id)}
        <div class="section m-0" animate:flip="{{duration: flipDurationMs}}">
            {#if sect.active || showArchived}
            <div class="m-1">
                <div class="grip" on:mousedown={startDrag} on:touchstart={startDrag} on:mouseup={stopDrag} on:touchend={stopDrag}></div>
                <Section bind:section={sect} name={sect.name} sectionID={sect.id} items={sect.tasks.sort( (a,b) => a.position - b.position )}/>
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