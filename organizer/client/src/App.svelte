<script>
    import { onMount } from 'svelte';

    import { api_host, csrf_tok, current_user, flash_message, remember_user, request, view } from './app_store';
    import Login from './Login.svelte';
    import Flash from './Flash.svelte';
    import Nav from './Nav.svelte';
    import Schedule from './schedule/Schedule.svelte';
    import Project from './project/Project.svelte'
    import { projectCleanUp } from './project/project_utils.js';
    import { scheduleCleanUp} from './schedule/schedule_utils.js';
    import { unsetCookie, getCookie } from './cookie.js'; 
    import Admin from './admin/Admin.svelte';

    
    let csrf_refresh;

    async function smartRequest(url, req_object) {
        const res = await fetch(url, req_object);
        if(res.status === 200) {
            return res
        }
        else if(res.status === 401) {
            //Try to refresh and resend
            const refresh_success = await refresh()
            if(refresh_success) {
                //Got new access token, retry request
                if(req_object.method != 'GET') {
                    req_object.headers['X-CSRF-TOKEN'] = $csrf_tok
                }
                return await smartRequest(url, req_object);
            }
            else {
                logout();
            }
        }
        else {
            return res
        }
    }

    async function logout() {
    	const res = await fetch($api_host +"/logout", {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
        });
    	if (res.ok) {
            scheduleCleanUp();
            projectCleanUp();
            unsetCookie("username");
            unsetCookie("view");
            unsetCookie("remember_user");
            unsetCookie("roles");
            $current_user = false;
            $view = "split";
    	} else {
            $flash_message = ["failure","Failed to Logout."]
            throw new Error(res.message)
        }
        
    }

    async function refresh() {
        try {
                csrf_refresh = getCookie("csrf_refresh_token");
            }
        catch {
            console.log("Failed to set csrf_refresh");
        }  
        const res = await fetch($api_host + '/refresh', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': csrf_refresh
                }
        });
        if(res.status === 200) {
            $csrf_tok = getCookie("csrf_access_token")
            return true;
        }
        else {
            return false;
        }
    }

    document.addEventListener("DOMContentLoaded", async function(event) { 
        try {
            $remember_user = getCookie("remember_user");
        }
        catch {}
        try {
            $current_user = {};
            $current_user.username = getCookie("username");
            $current_user.roles = getCookie("roles").split(",");
            console.log($current_user.roles)
        }
        catch {
            $current_user = false;
        }
        try {
            $csrf_tok = getCookie("csrf_access_token");
        }
        catch {}
        try {
            $view = getCookie("view");
        }
        catch {}
        if($current_user === false) {
            logout();
        }
        else {
            const reload_refresh = await refresh()
            if(!reload_refresh) {
                logout();
            } 
        }
    });

    onMount(() => {
        $request = smartRequest;
        $api_host = "http://" + window.location.hostname + ":7890";
    });

</script>

<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
</head>

{#if $current_user == false}
    <div id="login">
        <Flash/>
    	<Login/>
    </div>			
{:else}
    
    <Nav/>
    <br>
    <br class="d-md-none">
    <Flash/>
    {#if $view === "split"}
    <br>
    <Schedule/>
    <br>
    <Project/>
    {:else if $view === "project"}
    <br>
    <Project/>
    {:else if $view === "schedule"}
    <br>
    <Schedule/>
    {:else if $view === "admin"}
    <br>
    <Admin/>
    {/if}
{/if}

<style>
    #login {
		text-align: center;
		max-width: 240px;
		margin: 0 auto;
		width: 100%;
	}

	@media (min-width: 640px) {
		#login {
			max-width: none;
		}
    }
</style>