<script>

import {day_date} from './schedule_store';

export let date = new Date();
let items = [];
let groupedItems = [];
let string_date;
const DAYS_OF_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

$: if(date) {
    string_date = date.getFullYear() + "-" + ("0" + (date.getMonth()+1)).slice(-2) + "-" + ("0" + (date.getDate())).slice(-2);
}
export function setItems(newItems) {
    items = newItems;
    if (items.length != 0) {
        groupItems();
    }
    else {
        groupedItems = [];
    }
}

// Checks if item has the same title as the one before, groups them together to save space (shows a count). Does not impact the agenda display
function groupItems() {
    groupedItems = [];
    groupedItems.push({'title':items[0], 'count':1})
    if (items.length > 1) {
        let i = 1;
        let j = 0;
        do {
            if(groupedItems[j].title === items[i]) {
                groupedItems[j].count += 1;
            }
            else {
                groupedItems.push({'title':items[i], 'count':1})
                j += 1;
            }
            i += 1;
        }
        while( i < items.length); 
    }
    
}

function goToDay(day) {
    window.scrollTo(0, document.body.scrollTop);
    $day_date = day;
}
</script>

<div>
    <h5>{DAYS_OF_WEEK[date.getDay()]}</h5><h5>{string_date.slice(5)}-{string_date.slice(0,4)}</h5>
    {#each groupedItems as item}
        <div>{item.title}{item.count > 1 ? " ("+item.count+")": ""}</div>
    {/each}
</div>   

<style>

</style>