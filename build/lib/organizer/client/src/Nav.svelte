<script>
    import { api_host, current_user, flash_message, remember_user, view } from "./app_store";
    import { setCookie, unsetCookie } from './cookie.js';
    import { projectCleanUp } from './project/project_utils.js';
    import { scheduleCleanUp } from './schedule/schedule_utils.js';


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
            $flash_message = ["success","Logout was successful."]
    	} else {
            $flash_message = ["failure","Failed to Logout."]
            throw new Error(res.message)
        }
    }
    
</script>

<div id="main-nav" class="container-fluid">
    <div class="row">
            <h6 class="m-2">Hi, {$current_user.username} |</h6>
            {#if $current_user.roles.includes("user")}
            <button class="btn btn-light view-btn"
                    style={($view === "split" ? "background-color:white;": "")}
                    on:click={()=>{$view="split";setCookie("view",$view,!$remember_user)}}>
                Split View
            </button>
            <button class="btn btn-light view-btn"
                    style={($view === "project" ? "background-color:white;": "")}
                    on:click={()=>{$view="project";setCookie("view",$view,!$remember_user)}}>
                Project View
            </button>
            <button class="btn btn-light view-btn"
                style={($view === "schedule" ? "background-color:white;": "")}
                on:click={()=> {$view="schedule";setCookie("view",$view,!$remember_user)}}>
                Schedule View
            </button>
            {/if}
            {#if $current_user.roles.includes("admin")}
            <button class="btn btn-light view-btn"
                style={($view === "admin" ? "background-color:white;": "")}
                on:click={()=> {$view="admin";setCookie("view",$view,!$remember_user)}}>
                Admin View
            </button>
            {/if}
        <div class="col p-0 m-0 mt-1" align="right">
            <a class="m-2" href="/" on:click|preventDefault={logout}>Logout</a>
        </div>
    </div>
</div>

<style>

    .view-btn {
        position: relative;
        align-self: flex-end;
        padding: 0;
        padding-left: .5em;
        padding-right: .5em;
        margin: 0;
        margin-left: .5em;
        font-size: .85em;
        height: 2em;
        border-radius: 1em 1em 0em 0em;
        border: 0px;
        outline: 0px;
        background-color: lightgrey;
    }

    .view-btn:hover {
        background-color: rgb(230, 230, 230);
    }

    #main-nav {
        z-index: 100;
        position: fixed;
        top: 0;
        left: 0;
        color:white;
        margin: 0;
        background-color: rgb(33, 27, 66); 
    }

    a {
        color: white;
    }
    a:hover {
        color: gray;
    }
</style>