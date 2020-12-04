<script>
import { onMount } from "svelte";
import { api_host, csrf_tok, flash_message, request } from "../app_store";
import EditUser from "./EditUser.svelte";


let userList = [];
let editUser = false;

onMount(()=> {
    getUsers();
})

async function getUsers() {
    const res = await $request($api_host + "/admin/users", {
            credentials: "include",
            headers: {
                'X-CSRF-TOKEN': $csrf_tok
            }
        });
    if(res.ok) {
        userList = await res.json();
    }
    else {
        $flash_message = ["failure", "Failed to get list of users."]
    }
}

function stopEditing() {
    editUser = false;
    getUsers();
}

</script>
{#if editUser === false}
<!--- User List --->
<h4>Users:</h4>
<table class="table">
    <thead>
        <tr>
            <th scope="col">ID</th>
            <th scope="col">Username</th>
            <th scope="col">Role(s)</th>
            <th scope="col"></th>
        </tr>
    </thead>
    <tbody>
        {#each userList as user}
        <tr>
            <td>{user.id}</td> 
            <td>{user.username}</td>
            <td>{user.roles}</td>
            <td>
                <a href="/" on:click|preventDefault={()=>{editUser=user}}>
                <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-pencil-square" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456l-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                    <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                </svg>
                </a>
            </td>
        </tr>
        {/each}
    </tbody>
</table>
{:else}
<EditUser user={editUser} cancel={stopEditing}/>
{/if}
<style>

</style>