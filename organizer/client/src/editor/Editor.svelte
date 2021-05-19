<script>
import { onMount, tick } from "svelte";
import { sanitize } from '../utils';

export let autoFocus = true;
export let editable = false;
export let initialContent = "";
let editor;
let backupContent = initialContent;

// Load initial content
onMount(()=>{
    editor.innerHTML = initialContent;
    if(editable && autoFocus) {
        editor.focus();
        var sel = window.getSelection();
        var range = sel.getRangeAt(0);
        range.selectNodeContents(editor);
        range.collapse(false);
    }
})

// Meant to be called from a separate component
export function getSanitizedContent() {
    return sanitize(editor.innerHTML)
}
// Meant to be called from a separate component
export async function startEdit() {
    backupContent = editor.innerHTML;
    editable = true;
    await tick()
    editor.focus();
    var sel = window.getSelection();
    var range = sel.getRangeAt(0);
    range.selectNodeContents(editor);
    range.collapse(false);
}

// Call after a succesful save, does not revert changes
export function stopEdit() {
    editable = false;
}

// Stop editing a revert changes
export function cancelEdit() {
    editable = false;
    editor.innerHTML = backupContent;
}

export function clearContent() {
    editor.innerHTML = "";
    backupContent = "";
}

</script>

<div class="d-block w-100 contenteditable" contenteditable={editable}  bind:this={editor}></div>

<style>
    .contenteditable {
        text-align: left;
        white-space: pre-wrap;
        display: inline-block;
        padding: 3px;
        min-height: 3.4em;
        border: 1px solid #ced4da;
        border-radius: .25rem;
    }
</style>