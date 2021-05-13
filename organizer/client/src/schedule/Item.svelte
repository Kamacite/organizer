<script>
    import { inputing, editing, new_edit, edit_data } from './schedule_store.js';

    export let mode = ""; //day,week,month...
    export let id = 0;
    export let date = "";
    export let time = "";
    export let title = "";
    export let details = "";

    function editClick() {
        window.scrollTo(0,document.body.scrollTop);
        if($editing) {
            $new_edit = true;
        }
        $inputing = false
        $edit_data = {
        'id':id,
        'date':date,
        'time': time,
        'title': title,
        'details': details
        };
        $editing = true;     
    };

</script>
{#if mode == "day"}
<div>
    <a href="/" on:click|preventDefault={editClick}>
        <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-pencil-square" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456l-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
            <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
        </svg>
    </a>
    {time} | {title}
    {#if details} 
        <span>-</span> 
    {/if}
    {details} 
</div>
{/if}
<style>

</style>