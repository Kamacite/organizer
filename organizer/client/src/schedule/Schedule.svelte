<script>

	import { onMount } from 'svelte';
	
	import Day from './Day.svelte';
	import Week from './Week.svelte';
	import NewItem from './NewItem.svelte';
	import EditItem from './EditItem.svelte';
	import { flash_message, current_user, csrf_tok, api_host } from '../app_store.js';
	import { editing, inputing, day_date, week_date,  } from './schedule_store.js';
	
	let time = new Date();
	const days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

	$: hours = ("0" + time.getHours()).slice(-2);
	$: minutes = ("0" + time.getMinutes()).slice(-2);
	$: seconds = ("0" + time.getSeconds()).slice(-2);
	$: date = (time.getMonth()+1) + "/" + (time.getDate()) + "/" + time.getFullYear();
	$: day = days_of_week[time.getDay()]

	let item_button_style = "";
	let item_button_text = "New Item"

	let day_display = "block";
	let day_button_style = "background-color: grey";

	let week_display = "block";
	let week_button_style = "background-color: grey";

	onMount(() => {
		
		const interval = setInterval(() => {
			time = new Date();
		}, 1000);
		return () => {
			clearInterval(interval);
		};
	});

	

	function newItemOnClick() {
		if(!$inputing && !$editing) {
			$inputing = true;
			
		}
		else {
			$inputing = false;
			
		}
	};
	$: if($inputing) {
		item_button_text = "New Item";
		item_button_style = "background-color: grey";
	}
	else if($editing) {
		item_button_text = "Edit Item";
		item_button_style = "background-color: grey";
	}
	else {
		item_button_text = "New Item";
		item_button_style = ""
	}
	function dayOnClick() {
		if(day_display === "none") {
			day_display = "block"
			day_button_style = "background-color: grey"
		}
		else {
			day_display = "none"
			day_button_style = ""
		}
	};
	function weekOnClick() {
		if(week_display === "none") {
			week_display = "block"
			week_button_style = "background-color: grey"
		}
		else {
			week_display = "none"
			week_button_style = ""
		}
	};
	function todayOnClick() {
		day_date.set(time.getFullYear() + "-" + ("0" + (time.getMonth()+1)).slice(-2) 
						+ "-" + ("0" + (time.getDate())).slice(-2));
		week_date.set(time.getFullYear() + "-" + ("0" + (time.getMonth()+1)).slice(-2) 
						+ "-" + ("0" + (time.getDate())).slice(-2));
		$flash_message = ["neutral","Set day and week to today."]
	}
</script>




<nav class="container-fluid">
	<div class="row">
		<div class="col">
			<div class="row">
				<button style={item_button_style} on:click={newItemOnClick}>{item_button_text}</button>
				<button class="d-none d-md-block" style={day_button_style} on:click={dayOnClick}>Day</button>
				<button class="d-none d-md-block" style={week_button_style} on:click={weekOnClick}>Week</button>

			</div>
		</div>
		
		<div align="center" class="col">
			<h4 class="datetime d-none d-md-block">
				{day}
				
				{date}
				
				{hours}:{minutes}:{seconds}
			</h4>
		</div>
		<div class="col" align="right">
			<button on:click={todayOnClick}>Today</button>
		</div>
	</div>
</nav>
<main>
{#if $inputing}
<div>
	<NewItem/>
</div>
{/if}
{#if $editing}
<div>
	<EditItem/>
</div>
{/if}
<div style="display:{day_display}">
	<br>
	<Day/>
</div>
<div style="display:{week_display}">
	<br>
	<Week/>
</div>

</main>

<style>
	.datetime {
		font-family: "Lucida Console", Courier, monospace;
	}

	nav {
		color: black;
	}
	main {
		text-align: center;
		
		max-width: 240px;
		margin: 0 auto;
		width: 100%;
	}

	@media (min-width: 768px) {
		main {
			max-width: none;
		}
	}
</style>