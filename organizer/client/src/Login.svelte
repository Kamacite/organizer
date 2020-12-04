<script>
import { flash_message, api_host, csrf_tok, current_user, remember_user, view } from './app_store.js';
import { setCookie, getCookie } from './cookie.js';

let username = "";
let password = "";
let confirmPassword = "";
let register_flag = false;

async function login() {
    if(username === "") {
        $flash_message = ["neutral", "Please enter a username."];
        return
    }
    if(password === "") {
        $flash_message = ["neutral", "Please enter a password."];
        return
    }
    let data = {
        "username":username,
        "password":password,
    };
    
	const res = await fetch($api_host +"/login", {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
	if (res.ok) {
        data = await res.json()
        try {
            $csrf_tok = getCookie('csrf_access_token');
        }
        catch {
            console.log('csrf not set');
        }
        setCookie("username", username, !$remember_user)
        setCookie("roles", data['roles'], !$remember_user)
        if($remember_user) {
            setCookie("remember_user",true,false);
        }
        else {
            setCookie("remember_user",false,true);
        }
        
        $current_user = {}
        $current_user.username = username;
        $current_user.roles = data['roles'].split(",");
        if (!$current_user.roles.includes("user")) {
            $view = "admin";
        }
        $flash_message = ["success","Login successful"];
	} else {
        $flash_message = ["failure","Failed to login."];
        throw new Error(res.message);
    }
    
}

async function register() {
    if(username === "") {
        $flash_message = ["neutral", "Please enter a username."];
        return
    }
    if(password === "") {
        $flash_message = ["neutral", "Please enter a password."];
        return
    }
    if(password != confirmPassword) {
        $flash_message = ["failure", "Passwords do no match."];
        return
    }
    let data = {
        "username":username,
        "password":password,
    };
    
	const res = await fetch($api_host +"/register", {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
	if (res.ok) {
        register_flag = false;
        $flash_message = ["success","Registration successful"];
	} else {
        $flash_message = ["failure","Failed to register."];
        throw new Error(res.message);
    }
    
}

</script>

<div class="form-block m-auto">
    <form on:submit|preventDefault>
    <img class="mr-3" src="/brain_icon.png" alt="Organizer">
        <div class="form-group">
            <label for="username">Username:</label>
            <input class="form-control" id="username" type="text" bind:value={username}>
            <label for="password">Password:</label>
            <input class="form-control" id="password" type="password" bind:value={password}>
            {#if register_flag}
            <label for="confirmPassword">Confirm Password:</label>
            <input class="form-control" id="confirmPassword" type="password" bind:value={confirmPassword}>
            <br>
            {:else}
            <br>
            <div class="form-group form-check">
                <input type="checkbox" class="form-check-input" id="remember" bind:checked={$remember_user}>
                <label class="form-check-label" for="remember">Remember me?</label>
            </div>
            {/if}
            {#if !register_flag}
            <button class="btn-outline-secondary" type="submit" on:click={()=>login()}>Login</button>
            {:else}
            <button class="btn-outline-secondary" on:click={()=>register()}>Register</button>
            {/if}
            <button class="btn-outline-secondary" on:click={()=>{username="";password="";confirmPassword="";register_flag=false}}>Cancel</button>
            <br><br>
            <div>
            {#if !register_flag}
                <a href="/" on:click|preventDefault={()=>register_flag=true}>Register</a>
            {:else}
                <a href="/" on:click|preventDefault={()=>register_flag=false}>Login</a>
            {/if}
            </div>  
        </div>
        </form>
</div>


<style>
.form-block {
    margin:auto;
    width:25%;
 }
 
 @media screen and (max-width: 576px) {
  .form-block {
    width: 100%;
  }
}
</style>