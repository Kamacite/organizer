<script>
import { fade, fly } from 'svelte/transition';

import { flash_message } from './app_store.js';

let visible = false;

$: if($flash_message) {
       visible = true;
   }
   else {
       visible = false;
   }
</script>

{#if visible}
<div id="flash" class="container-fluid w-75 p-1 {$flash_message[0]}" 
    in:fly="{{y:10, delay:0}}"
    out:fade="{{delay:1500}}" 
    on:introend="{() => $flash_message = null}"
    >
    <div class="row m-0 message">
        <div>
            {$flash_message[1]}
        </div>
    </div>
</div>
{/if}

<style>

 #flash {
     position: fixed;
     z-index: 100;
     bottom: 0;
     left: 12.5vw;
     border-radius: 1em 1em 0em 0em;
 }

 .message {
     justify-content: center;
 }
 
 .success {
     background-color: limegreen;
 }

 .failure {
     background-color: palevioletred;
 }

 .neutral {
     background-color: lightsteelblue;
 }
</style>