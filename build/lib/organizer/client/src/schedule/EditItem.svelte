<script>
   
    import { flash_message, api_host, csrf_tok, request } from '../app_store.js';
    import { day_date, editing, edit_data, new_edit, submit_day_check, submit_week_check, week_date,  } from './schedule_store.js';
    
    //title, date, time, and details cannot be empty
    let id = $edit_data['id'];
    let new_title = $edit_data['title'];
    let new_date = $edit_data['date'];
    let new_time = $edit_data['time'];
    let new_details = $edit_data['details'];
    
    $: if ($new_edit) {
        id = $edit_data['id'];
        new_title = $edit_data['title'];
        new_date = $edit_data['date'];
        new_time = $edit_data['time'];
        new_details = $edit_data['details'];
        $new_edit = false;
    }

    async function handleSubmit() {
        
        let data = {
            "title":new_title,
            "item_date":new_date,
            "item_time":new_time,
            "details":new_details,
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
            $flash_message = ["success",new_title + " was updated successfully."]
            $editing=false;
            //Trigger check to see if either day or week need to be reloaded
            submit_day_check.set(null)
            submit_day_check.set(new_date)
            submit_week_check.set(null)
            submit_week_check.set(new_date)
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
            $flash_message = ["success",new_title + " agenda item was deleted successfully."]
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
                <input class="form-control" id="edit_title" type="text" bind:value={new_title}>
                <input class="form-control" id="edit_item_date" type="date" bind:value={new_date}>
                <input class="form-control" id="edit_item_time" type="time" bind:value={new_time}>
                <label for="edit_item_details">Details:</label>
                <textarea class="form-control" id="edit_item_details" bind:value={new_details}></textarea>
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