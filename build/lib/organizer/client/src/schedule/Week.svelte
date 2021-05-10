<script>
    import { onMount } from 'svelte';
    import { api_host, csrf_tok, request } from '../app_store.js';
    import { day_date, week_date, submit_week_check} from './schedule_store.js'
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
    // List containing the current day of the week for the 7 divs (int index into days_of_week)
    let week_days = [];
    const days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    
    // Ensures everything if fully loaded before change to $week_date store have any effect
    let loaded = false;
    // Bind variables for the 7 divs
    let day0;
    let day1;
    let day2;
    let day3;
    let day4;
    let day5;
    let day6;
    let child;
    
    // creates week_dates and days array before divs load
    updateDates()

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
    });

    // anytime week_date changes, update the current week agenda
    $: if($week_date && loaded) {
        getWeekAgenda()
    }

    // Checks if a newly submitted item falls in the current shown week.
    // Reloads content if true
    $: if($submit_week_check && loaded) {
        for(let i=0;i<7;i++) {
            if ($submit_week_check === week_dates[i]) {
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
                week_dates[i] = day.getFullYear() + "-" + ("0" + (day.getMonth()+1)).slice(-2) + "-" 
                + ("0" + (day.getDate())).slice(-2);
                
                week_days[i] = day.getDay()
        }
    }
    
    // remove all child elements except the first one (header with date and day)
    // called from getWeekAgenda
    function clearWeekAgenda() {
        while(!day0.firstChild.isEqualNode(day0.lastChild)) {
            day0.removeChild(day0.lastChild);
        }
        while(!day1.firstChild.isEqualNode(day1.lastChild)) {
            day1.removeChild(day1.lastChild);
        }
        while(!day2.firstChild.isEqualNode(day2.lastChild)) {
            day2.removeChild(day2.lastChild);
        }
        while(!day3.firstChild.isEqualNode(day3.lastChild)) {
            day3.removeChild(day3.lastChild);
        }
        while(!day4.firstChild.isEqualNode(day4.lastChild)) {
            day4.removeChild(day4.lastChild);
        }
        while(!day5.firstChild.isEqualNode(day5.lastChild)) {
            day5.removeChild(day5.lastChild);
        }
        while(!day6.firstChild.isEqualNode(day6.lastChild)) {
            day6.removeChild(day6.lastChild);
        }
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
		} else {
			throw new Error(res.status)
		}
    }

    // when items_week changes fill in new items to divs
    $: if(!(items_week === [])) {
        for(let item in items_week) {
                // Check for late night early morning items and add to late_items
                if (items_week[item].item_time >= "00:00" && items_week[item].item_time < "05:00") {
                    late_items.push(items_week[item]);
                    continue;
                }
                if (items_week[item].item_date === week_dates[0]) {
                    child = document.createElement('div');
                    child.textContent = items_week[item].title;
                    day0.appendChild(child);                
                } else if (items_week[item].item_date === week_dates[1]) {
                    child = document.createElement('div');
                    child.textContent = items_week[item].title;
                    day1.appendChild(child);                
                } else if (items_week[item].item_date === week_dates[2]) {
                    child = document.createElement('div');
                    child.textContent = items_week[item].title;
                    day2.appendChild(child);                
                } else if (items_week[item].item_date === week_dates[3]) {
                    child = document.createElement('div');
                    child.textContent = items_week[item].title;
                    day3.appendChild(child);                
                } else if (items_week[item].item_date === week_dates[4]) {
                    child = document.createElement('div');
                    child.textContent = items_week[item].title;
                    day4.appendChild(child);                
                } else if (items_week[item].item_date === week_dates[5]) {
                    child = document.createElement('div');
                    child.textContent = items_week[item].title;
                    day5.appendChild(child);                
                } else if (items_week[item].item_date === week_dates[6]) {
                    child = document.createElement('div');
                    child.textContent = items_week[item].title;
                    day6.appendChild(child);                
                }
                     
                
        };
        //add late items after all others
        for(let item in late_items) {
            if (late_items[item].item_date === week_dates[0]) {
                    child = document.createElement('div');
                    child.textContent = late_items[item].title;
                    day0.appendChild(child);                
                } else if (late_items[item].item_date === week_dates[1]) {
                    child = document.createElement('div');
                    child.textContent = late_items[item].title;
                    day1.appendChild(child);                
                } else if (late_items[item].item_date === week_dates[2]) {
                    child = document.createElement('div');
                    child.textContent = late_items[item].title;
                    day2.appendChild(child);                
                } else if (late_items[item].item_date === week_dates[3]) {
                    child = document.createElement('div');
                    child.textContent = late_items[item].title;
                    day3.appendChild(child);                
                } else if (late_items[item].item_date === week_dates[4]) {
                    child = document.createElement('div');
                    child.textContent = late_items[item].title;
                    day4.appendChild(child);                
                } else if (late_items[item].item_date === week_dates[5]) {
                    child = document.createElement('div');
                    child.textContent = late_items[item].title;
                    day5.appendChild(child);                
                } else if (late_items[item].item_date === week_dates[6]) {
                    child = document.createElement('div');
                    child.textContent = late_items[item].title;
                    day6.appendChild(child);                
                }
        }
        late_items = []
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
<!-- Divs for each day of the week -->
<div class="container-fluid">
    <div id="week" class="row">
        <div class="day col mx-1 pt-2" bind:this={day0} on:click={() => goToDay(week_dates[0])}>
            <div>
                <h5>{week_dates[0].slice(5)}-{week_dates[0].slice(0,4)}<br>{days_of_week[week_days[0]]}</h5>
            </div>           
        </div>
        <div class="seperator w-100 d-block d-md-none"></div>
        <div class="day col mx-1 pt-2" bind:this={day1} on:click={() => goToDay(week_dates[1])}>
            <div>
                <h5>{week_dates[1].slice(5)}-{week_dates[1].slice(0,4)}<br>{days_of_week[week_days[1]]}</h5>
            </div>         
        </div>
        <div class="seperator w-100 d-block d-md-none"></div>
        <div class="day col mx-1 pt-2" bind:this={day2} on:click={() => goToDay(week_dates[2])}>
            <div>
                <h5>{week_dates[2].slice(5)}-{week_dates[2].slice(0,4)}<br>{days_of_week[week_days[2]]}</h5>
            </div>
        </div>
        <div class="seperator w-100 d-block d-md-none"></div>
        <div class="day col mx-1 pt-2" bind:this={day3} on:click={() => goToDay(week_dates[3])}>
            <div>
                <h5>{week_dates[3].slice(5)}-{week_dates[3].slice(0,4)}<br>{days_of_week[week_days[3]]}</h5>
            </div>
        </div>
        <div class="seperator w-100 d-block d-md-none"></div>
        <div class="day col mx-1 pt-2" bind:this={day4} on:click={() => goToDay(week_dates[4])}>
            <div>
                <h5>{week_dates[4].slice(5)}-{week_dates[4].slice(0,4)}<br>{days_of_week[week_days[4]]}</h5>
            </div>
        </div>
        <div class="seperator w-100 d-block d-md-none"></div>
        <div class="day col mx-1 pt-2" bind:this={day5} on:click={() => goToDay(week_dates[5])}>
            <div>
                <h5>{week_dates[5].slice(5)}-{week_dates[5].slice(0,4)}<br>{days_of_week[week_days[5]]}</h5>
            </div>
        </div>
        <div class="seperator w-100 d-block d-md-none"></div>
        <div class="day col mx-1 pt-2" bind:this={day6} on:click={() => goToDay(week_dates[6])}>
            <div>
                <h5>{week_dates[6].slice(5)}-{week_dates[6].slice(0,4)}<br>{days_of_week[week_days[6]]}</h5>
            </div>
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

    svg {
        vertical-align: initial;
    }

</style>