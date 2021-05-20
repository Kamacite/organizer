<script>
    import { onMount } from 'svelte';
    import { api_host, csrf_tok, request } from '../app_store.js';
    import { day_date, submit_day_check } from './schedule_store.js';
    import Item from './Item.svelte';
    
    // List containing all agenda items for given day_date
    let items_today = [];
    // Used to correcttly order items later than midnight
    let late_items = [];
    
    let d = new Date()
    const DAYS_OF_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    let today=DAYS_OF_WEEK[d.getDay()+1];
    // day_date, store that controls what the current date is shown for the day
    // defaults to today
    day_date.set(d.getFullYear() + "-" + ("0" + (d.getMonth()+1)).slice(-2) 
                        + "-" + ("0" + (d.getDate())).slice(-2));
    
    let backup_date = $day_date;

    // Bind variables for the time of day divs
    let morning;
    let morning_items = [];
    let afternoon;
    let afternoon_items = [];
    let evening;
    let evening_items = [];
    // Ensures everything if fully loaded before change to $day_date store have any effect
    let loaded = false;
    
    onMount(async () => {
        loaded = true;
	});

    // anytime day_date changes, update the current day agenda
    $: if($day_date && loaded) {
        backup_date = $day_date;
        
        getDaysAgenda();
    }

    // Checks if a newly submitted item falls in the current shown day.
    // Reloads content if true
    $: if($submit_day_check && loaded) {
        
        if ($submit_day_check === $day_date) {
            backup_date = $day_date;
            getDaysAgenda();
        }
        $submit_day_check = null
    }

    // remove all child elements from each time segment
    // called from getDaysAgenda
    function clearAgenda() {
        while(morning_items[0]) {
            morning_items.pop();
        }
        while(afternoon_items[0]) {
            afternoon_items.pop();
        }
        while(evening_items[0]) {
            evening_items.pop();
        }
    }

    // Fetch days agenda from api
    export async function getDaysAgenda() {
        clearAgenda()
        const res = await $request($api_host + "/day/"+$day_date, {
            credentials: "include",
            headers: {
                'X-CSRF-TOKEN': $csrf_tok
            }
        });
		if (res.ok) {
            items_today = await res.json();
            d = new Date($day_date);
            today=DAYS_OF_WEEK[d.getDay()+1];
		} else {
			throw new Error(res.status)
		}
    }

    // Function to add (or subtract) days from a current date. Helps with isodate string addition
    function addDays(date, days) {
        let new_date = new Date(date);
        new_date.setDate(new_date.getDate() +1+ days);
        return new_date;
    }

    // Used with chevron buttons to advance the day in the date select
    function changeDay(change) {
        if(!$day_date) {
            $day_date = backup_date;
        }
        d = addDays($day_date , change);
        $day_date = d.getFullYear() + "-" + ("0" + (d.getMonth()+1)).slice(-2) 
                    + "-" + ("0" + (d.getDate())).slice(-2);
    }

    // when items_today changes fill in new items to divs
    
    $: if(!(items_today === [])) {
        
        for(let item in items_today) {
            if (items_today[item].item_time < "12:00" && items_today[item].item_time >= "05:00") {
                morning_items.push(items_today[item]);         
            }
            else if (items_today[item].item_time < "18:00" && items_today[item].item_time >= "05:00") {
                afternoon_items.push(items_today[item]);    
            }
            else {
                // Check if an evening item is past midnight
                if(items_today[item].item_time[0] === "0") {
                    // add it to second array, allowing them to be listed later.
                    late_items.push(items_today[item])
                    continue;
                }
                evening_items.push(items_today[item])    
            }
        };
        // List all late night/early am (12am-5am)
        for(let item in late_items) {
            evening_items.push(items_today[item])
        }
        late_items = [];
        
        morning_items = morning_items;
        afternoon_items = afternoon_items;
        evening_items = evening_items;
    }
    
</script>
<!-- Date controller -->

            <div class="d-flex justify-content-start justify-content-md-start  mx-1">
            <button on:click={() => changeDay(-1)}>
                <svg width=".5em" height="1em" viewBox="0 0 16 16" class="bi bi-chevron-left" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/>
                </svg>
            </button>
            <input class="" id="item_date" type="date" bind:value={$day_date}>
            <button on:click={() => changeDay(1)}>
                <svg width=".5em" height="1em" viewBox="0 0 16 16" class="bi bi-chevron-right" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
                </svg>
            </button>

            </div>
            <div class="w-100 d-block d-md-none"></div>
            <h5 class="align-self-center text-center ml-2">{today}</h5>
        
<!-- Divs for morning, afternoon, evening -->
<div class="container-fluid">
    <div class="row d-none d-md-flex">
        <div class="morning col mx-1"><h3>Morning:</h3></div>
        <div class="afternoon col mx-1"><h3>Afternoon:</h3></div>
        <div class="evening col mx-1"><h3>Evening:</h3></div>
    </div>
    <div class="row">
        
        <div class="morning col mx-1" bind:this={morning}>
            {#each morning_items as item}
                <Item mode="day" id={item.id} date={item.item_date} time={item.item_time} title={item.title} details={item.details}/>
            {/each}
        </div>
        <div class="w-100 d-block d-md-none"></div>
        <div class="afternoon col mx-1" bind:this={afternoon}>
            {#each afternoon_items as item}
                <Item mode="day" id={item.id} date={item.item_date} time={item.item_time} title={item.title} details={item.details}/>
            {/each}
        </div>
        <div class="w-100 d-block d-md-none"></div>
        <div class="evening col mx-1" bind:this={evening}>
            {#each evening_items as item}
                <Item mode="day" id={item.id} date={item.item_date} time={item.item_time} title={item.title} details={item.details}/>
            {/each}
        </div>
        
    </div>
</div>

<style>
    .morning {
        background-color: rgb(255, 246, 119);
        padding: 1em;
        text-align: left;
    }
    .afternoon {
        background-color: rgb(128, 172, 255);
        padding: 1em;
        text-align: left;
    }
    .evening {
        background-color: darkgrey;
        padding: 1em;
        text-align: left;   
        
    }

</style>