<script>
import { api_host, csrf_tok, flash_message, request } from "../app_store";

export let user;
export let cancel;
let newUsername = user.username;
let curUsername = user.username;
let newPassword = "";
let confirmPassword = "";
let isUser = (user.roles.includes("user") ? true : false);
let isAdmin = (user.roles.includes("admin") ? true : false);
let curUser = isUser;
let curAdmin = isAdmin;
let unlockDelete = false;

async function updateUsername() {
    if(newUsername === "") {
        $flash_message = ["failure", "Username cannot be blank."];
        return
    }
    if(newUsername === curUsername) {
        $flash_message = ["neutral", "Username is the same as before."];
        return
    }
    let userData = {
        username: newUsername
    };
    const res = await $request($api_host + "/admin/users/" + user.id  , {
        credentials: "include",
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': $csrf_tok
        },
        body: JSON.stringify(userData)
    });
    if(res.status === 200) {      
        curUsername = newUsername;
        $flash_message = ["success", "Username updated successfully."];   
    }
    else {
        newUsername = curUsername;
        $flash_message = ["failure", "Username failed to update."];
    }
}

async function changePassword() {
    if(newPassword != confirmPassword) {
        $flash_message = ["failure", "Passwords do not match."];
        return
    }
    if (newPassword === "") {
        $flash_message = ["failure", "Password cannot be blank."];
        return
    }
    let userData = {
        password: newPassword
    };
    const res = await $request($api_host + "/admin/users/" + user.id  , {
        credentials: "include",
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': $csrf_tok
        },
        body: JSON.stringify(userData)
    });
    if(res.status === 200) {      
        newPassword = "";
        confirmPassword = "";
        $flash_message = ["success", "Password updated successfully."];
    }
    else {
        $flash_message = ["failure", "Password failed to update."];
    }
}

async function editRoles() {
    if(!isUser && !isAdmin) {
        $flash_message = ["failure", "User must have at least one role."];
        return
    }
    let roles = ""
    if(isUser && isAdmin) {
        roles = "user,admin";
    }
    if(isUser && !isAdmin) {
        roles = "user";
    }
    if (!isUser && isAdmin) {
        roles = "admin"
    }
    let userData = {
        roles: roles
    };
    const res = await $request($api_host + "/admin/users/" + user.id  , {
        credentials: "include",
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': $csrf_tok
        },
        body: JSON.stringify(userData)
    });
    if(res.status === 200) {      
        curUser= isUser;
        curAdmin= isAdmin;
        $flash_message = ["success", "Roles were updated successfully."]    ;
    }
    else {
        isUser = curUser;
        isAdmin = curAdmin;
        let data = await res.json()
        $flash_message = ["failure",(data.message ? data.message: "Roles failed to update.") ];
    }
}

async function deleteUser() {
    const res = await $request($api_host + "/admin/users/" + user.id  , {
        credentials: "include",
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': $csrf_tok
        }
    });
    if(res.status === 200) {      
        $flash_message = ["success", "User was successfully deleted."];
        cancel();
    }
    else {
        let data = await res.json()
        $flash_message = ["failure",(data.message ? data.message: "Failed to delete user.") ];
    }
}

</script>

<div class="conatiner-fluid">
    <h3 class="ml-4">Edit User:</h3>
    <div class="row m-0" >
        <div class="col">
            <!-- Username Change -->
            <div class="d-block d-md-flex justify-content-end">
                <div class="d-block d-md-flex align-items-start">
                    <label for="username">Username:</label>
                    <div class="w-100 d-block d-md-none"></div>
                    <input id="username" class="setting_input" bind:value={newUsername}>
                    <div class="w-100 d-block d-md-none"></div>
                    <button class="btn btn-outline-secondary" on:click={updateUsername}>Update</button>
                    <button class="btn btn-outline-secondary ml-1" on:click={()=>newUsername=curUsername}>Cancel</button>
                </div>
            </div>
            <br>
            <!-- Password Change -->
            <span class="d-block d-md-flex justify-content-end">
                <div class="d-block d-md-flex align-items-start">
                    <label for="password">Password:</label>
                    <div class="w-100 d-block d-md-none"></div>
                    <input type="password" id="password" class="setting_input" bind:value={newPassword}>
                    <input type="password" id="confirmPassword" class="setting_input" bind:value={confirmPassword}>
                    <div class="w-100 d-block d-md-none"></div>
                    <button class="btn btn-outline-secondary" on:click={changePassword}>Update</button>
                    <button class="btn btn-outline-secondary ml-1" on:click={()=>{newPassword="";confirmPassword="";}}>Cancel</button>
                </div>
            </span>
            <br>
            <!-- Roles Change -->
            <span class="d-block d-md-flex justify-content-end">
                <div class="d-block d-md-flex align-items-start">
                    <label for="defaultCheck1">Roles:&nbsp;</label>
                    <div class="w-100 d-block d-md-none"></div>
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="checkbox" id="inlineCheckbox1" bind:checked={isUser}>
                        <label class="form-check-label" for="inlineCheckbox1">user</label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="checkbox" id="inlineCheckbox2" bind:checked={isAdmin}>
                        <label class="form-check-label" for="inlineCheckbox2">admin</label>
                      </div>
                    <button class="btn btn-outline-secondary" on:click={editRoles}>Update</button>
                    <button class="btn btn-outline-secondary ml-1" on:click={()=>{isUser=curUser;isAdmin=curAdmin}}>Cancel</button>
                </div>
            </span>
            <br><br>
            <!-- Delete User -->
            <span class="d-block d-md-flex justify-content-end">
                <div class="d-block d-md-flex align-items-start">
                    <div class="w-100 d-block d-md-none"></div>
                    <div class="form-check form-check-inline">
                        <label class="form-check-label" for="inlineCheckbox1">Delete User:&nbsp;</label>
                        <input class="form-check-input" type="checkbox" id="deleteCheck" bind:checked={unlockDelete}>
                      </div>
                    <button class="btn btn-danger" disabled={!unlockDelete} on:click={deleteUser}>Delete</button>
                </div>
            </span>
        </div>
        <div class="col">
            <span class="row mr-2 justify-content-center">
                <div class="d-flex align-items-start">
                    <button class="btn btn-warning" on:click={()=>cancel()}>Back</button>
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
