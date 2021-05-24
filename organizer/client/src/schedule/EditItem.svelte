<script>
   
    import { flash_message, api_host, csrf_tok, request } from '../app_store.js';
    import { day_date, editing, edit_data, new_edit, submit_day_check, submit_week_check, week_date,  } from './schedule_store.js';
    import Editor from '../editor/Editor.svelte';
    //title, date, time, and details cannot be empty
    let id = $edit_data['id'];
    let newTitle = $edit_data['title'];
    let newDate = $edit_data['date'];
    let newTime = $edit_data['time'];
    let newDetails = $edit_data['details'];
    let editor;


    $: if ($new_edit) {
        id = $edit_data['id'];
        newTitle = $edit_data['title'];
        newDate = $edit_data['date'];
        newTime = $edit_data['time'];
        new_details = $edit_data['details'];
        $new_edit = false;
    }

    async function handleSubmit() {
        
        let data = {
            "title":newTitle,
            "item_date":newDate,
            "item_time":newTime,
            "details":editor.getSanitizedContent(),
            "active":true,
            "reoccuring": false
        };
        
        const res = await $request($api_host + "/item/" + id, {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': $csrf_tok
            },
            body: JSON.stringify(data)
        });
        if (res.ok) {
            $flash_message = ["success",newTitle + " was updated successfully."]
            $editing=false;
            //Trigger check to see if either day or week need to be reloaded
            submit_day_check.set(null)
            submit_day_check.set($day_date)
            submit_week_check.set(null)
            submit_week_check.set($week_date)
        } else {
            $flash_message = ["failure","Failed to update item."]
        }
        
    }


    async function deleteItem() {
        const res = await $request($api_host + "/item/" + id, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': $csrf_tok
            }
        });
        if (res.ok) {
            $flash_message = ["success",newTitle + " agenda item was deleted successfully."]
            $editing=false;
            //Trigger check to see if either day or week need to be reloaded
            submit_day_check.set(null);
            submit_day_check.set($day_date);
            submit_week_check.set(null);
            submit_week_check.set($week_date);
        } else {
            $flash_message = ["failure","Failed to delete item."];
        }
    }


    </script>
    
    <div class="form-block">
        <form on:submit|preventDefault={handleSubmit}>
            <div class="form-group">
                <label for="edit_title">Title:</label>
                <input class="form-control" id="edit_title" type="text" bind:value={newTitle}>
                <input class="form-control" id="edit_item_date" type="date" bind:value={newDate}>
                <input class="form-control" id="edit_item_time" type="time" bind:value={newTime}>
                <label for="edit_item_details">Details:</label>
                <Editor bind:this={editor} initialContent={newDetails} editable={true} autoFocus={false}/>
                <button type="submit" class="btn btn-outline-secondary mt-1">Update</button>
                <button class="btn btn-outline-secondary mt-1" on:click|preventDefault={()=>$editing=false}>Cancel</button>
                <button class="btn btn-danger mt-1 ml-2" on:click|preventDefault={deleteItem}>Delete</button>
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