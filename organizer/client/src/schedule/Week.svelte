<script>
    import { onMount } from 'svelte';
    import { api_host, csrf_tok, request } from '../app_store.js';
    import { day_date, week_date, submit_week_check} from './schedule_store.js'
    import Day from './Day.svelte';
    // List containing every agenda item for the week
    let items_week = [];
    // Used to correcttly order items later than midnight
    let late_items = [];
    let d = new Date();
    // week_date, store that controls what the current date the week starts at
    // defaults to today
    week_date.set(d.getFullYear() + "-" + ("0" + (d.getMonth()+1)).slice(-2) 
                    + "-" + ("0" + (d.getDate())).slice(-2));
         
    // List containing the current dates for the 7 week divs
    let week_dates = [];
    let week_dates_strings = [];
    // List containing the current day of the week for the 7 divs (int index into days_of_week)
    let week_days = [];
    
    let week_items = [[],[],[],[],[],[],[]];
    // Ensures everything if fully loaded before change to $week_date store have any effect
    let loaded = false;
    // Bind variables for the 7 Day components
    let day0;
    let day1;
    let day2;
    let day3;
    let day4;
    let day5;
    let day6;

    // Function to add (or subtract) days from a current date. Helps with isodate string addition
    function addDays(date, days) {
        let new_date = new Date(date);
        new_date.setDate(new_date.getDate() +1+ days);
        return new_date;
    }

    //Used with chevron buttons to advance the day in the date select
    function changeDay(change) {
        if(!$week_date) {
            $week_date = week_dates[0]
        }
        d = addDays($week_date , change);
        $week_date = d.getFullYear() + "-" + ("0" + (d.getMonth()+1)).slice(-2) 
            + "-" + ("0" + (d.getDate())).slice(-2);
    }

    onMount( () => {
    		loaded=true;
            updateDates();
    });

    // anytime week_date changes, update the current week agenda
    $: if($week_date && loaded) {
        getWeekAgenda()
    }

    // Checks if a newly submitted item falls in the current shown week.
    // Reloads content if true
    $: if($submit_week_check && loaded) {
        for(let i=0;i<7;i++) {
            if ($submit_week_check === week_dates_strings[i]) {
                $submit_week_check = null
                getWeekAgenda();
            }
        }
        $submit_week_check = null
    }

    // Updates the week dates and days when reloading week agenda
    // called on load and from getWeekAgenda
    function updateDates() {
        for( let i = 0; i<7; i++) {
                let day = addDays($week_date, i);
                week_dates[i] = day;
                week_dates_strings[i] = day.getFullYear() + "-" + ("0" + (day.getMonth()+1)).slice(-2) + "-" + ("0" + (day.getDate())).slice(-2);
                week_days[i] = day.getDay();
        }
    }
    
    // called from getWeekAgenda
    function clearWeekAgenda() {
        week_items = [[],[],[],[],[],[],[]];
    }

    // Fetch week agenda from api
    async function getWeekAgenda() {    
        clearWeekAgenda()
        const res = await $request($api_host + "/week/"+ $week_date, {
            credentials: "include",
            headers: {
                'X-CSRF-TOKEN': $csrf_tok
            }
        });
		if (res.ok) {
            items_week = await res.json();
            updateDates();
            updateDayItems();
		} else {
			throw new Error(res.status)
		}
    }

    function updateDayItems(){
        if(!(items_week === [])) {
        for(let item in items_week) {
            // Check for late night early morning items and add to late_items
            if (items_week[item].item_time >= "00:00" && items_week[item].item_time < "05:00") {
                late_items.push(items_week[item]);
                continue;
            }
            if (items_week[item].item_date === week_dates_strings[0]) {
                week_items[0].push(items_week[item].title);               
            } else if (items_week[item].item_date === week_dates_strings[1]) {
                week_items[1].push(items_week[item].title);              
            } else if (items_week[item].item_date === week_dates_strings[2]) {
                week_items[2].push(items_week[item].title);             
            } else if (items_week[item].item_date === week_dates_strings[3]) {
                week_items[3].push(items_week[item].title);              
            } else if (items_week[item].item_date === week_dates_strings[4]) {
                week_items[4].push(items_week[item].title);               
            } else if (items_week[item].item_date === week_dates_strings[5]) {
                week_items[5].push(items_week[item].title);                
            } else if (items_week[item].item_date === week_dates_strings[6]) {
                week_items[6].push(items_week[item].title);               
            }
        }
        //add late items after all others
        for(let item in late_items) {
            if (late_items[item].item_date === week_dates_strings[0]) {
                week_items[0].push(late_items[item].title);                 
            } else if (late_items[item].item_date === week_dates_strings[1]) {
                week_items[1].push(late_items[item].title);             
            } else if (late_items[item].item_date === week_dates_strings[2]) {
                week_items[2].push(late_items[item].title);           
            } else if (late_items[item].item_date === week_dates_strings[3]) {
                week_items[3].push(late_items[item].title);           
            } else if (late_items[item].item_date === week_dates_strings[4]) {
                week_items[4].push(late_items[item].title);            
            } else if (late_items[item].item_date === week_dates_strings[5]) {
                week_items[5].push(late_items[item].title);              
            } else if (late_items[item].item_date === week_dates_strings[6]) {
                week_items[6].push(late_items[item].title);               
            }
        }
        late_items = []
        day0.setItems(week_items[0]);
        day1.setItems(week_items[1]);
        day2.setItems(week_items[2]);
        day3.setItems(week_items[3]);
        day4.setItems(week_items[4]);
        day5.setItems(week_items[5]);
        day6.setItems(week_items[6]);
    }
    }
    function goToDay(day) {
        window.scrollTo(0, document.body.scrollTop);
        $day_date = day;
    }
</script>
<!-- Date controller -->
<div class="d-flex justify-content-center justify-content-md-start  mx-1">
    <button on:click={() => changeDay(-1)}>
        <svg width=".5em" height="1em" viewBox="0 0 16 16" class="bi bi-chevron-left" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/>
        </svg>
    </button>
    <input type="date" bind:value={$week_date}>
    <button on:click={() => changeDay(1)}>
        <svg width=".5em" height="1em" viewBox="0 0 16 16" class="bi bi-chevron-right" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
        </svg>
    </button>
</div>
<div class="spacer d-none d-md-block"></div>
<!-- Divs for each day of the week -->
<div class="container-fluid">
    <div id="week" class="row">
        <div class="day col mx-1 pt-2" on:click={() => goToDay(week_dates_strings[0])}>
            <Day bind:this={day0} date={week_dates[0]}/>
        </div>
        <div class="seperator w-100 d-block d-md-none"></div>
        <div class="day col mx-1 pt-2" on:click={() => goToDay(week_dates_strings[1])}>
            <Day bind:this={day1} date={week_dates[1]}/>     
        </div>
        <div class="seperator w-100 d-block d-md-none"></div>
        <div class="day col mx-1 pt-2" on:click={() => goToDay(week_dates_strings[2])}>
            <Day bind:this={day2} date={week_dates[2]}/>
        </div>
        <div class="seperator w-100 d-block d-md-none"></div>
        <div class="day col mx-1 pt-2" on:click={() => goToDay(week_dates_strings[3])}>
            <Day bind:this={day3} date={week_dates[3]}/>
        </div>
        <div class="seperator w-100 d-block d-md-none"></div>
        <div class="day col mx-1 pt-2" on:click={() => goToDay(week_dates_strings[4])}>
            <Day bind:this={day4} date={week_dates[4]}/>
        </div>
        <div class="seperator w-100 d-block d-md-none"></div>
        <div class="day col mx-1 pt-2" bon:click={() => goToDay(week_dates_strings[5])}>
            <Day bind:this={day5} date={week_dates[5]}/>
        </div>
        <div class="seperator w-100 d-block d-md-none"></div>
        <div class="day col mx-1 pt-2" on:click={() => goToDay(week_dates_strings[6])}>
            <Day bind:this={day6} date={week_dates[6]}/>
        </div>
    </div>

</div>



<style>

    .day {
        cursor: pointer;
        background-color: rgb(90, 199, 86);
        padding: 1vw;
    }

    .day:hover {
       background-color: rgb(105, 156, 103);
    }

    .seperator {
        height: .25em;

    }

    .spacer {
        min-height: 2rem;
    }

</style>