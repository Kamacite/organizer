<script>

	import { onMount } from 'svelte';
	
	import DayAgenda from './DayAgenda.svelte';
	import Week from './Week.svelte';
	import NewItem from './NewItem.svelte';
	import EditItem from './EditItem.svelte';
	import { flash_message, current_user, csrf_tok, api_host } from '../app_store.js';
	import { editing, inputing, day_date, week_date,  } from './schedule_store.js';
	
	let time = new Date();
	const DAYS_OF_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

	$: hours = ("0" + time.getHours()).slice(-2);
	$: minutes = ("0" + time.getMinutes()).slice(-2);
	$: seconds = ("0" + time.getSeconds()).slice(-2);
	$: date = (time.getMonth()+1) + "/" + (time.getDate()) + "/" + time.getFullYear();
	$: day = DAYS_OF_WEEK[time.getDay()]

	let itemButtonStyle = "";
	let itemButtonText = "New Item"

	let dayDisplay = "block";
	let dayButtonStyle = "background-color: grey";

	let weekDisplay = "block";
	let weekButtonStyle = "background-color: grey";

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
		itemButtonText = "New Item";
		itemButtonStyle = "background-color: grey";
	}
	else if($editing) {
		itemButtonText = "Edit Item";
		itemButtonStyle = "background-color: grey";
	}
	else {
		itemButtonText = "New Item";
		itemButtonStyle = ""
	}
	function dayOnClick() {
		if(dayDisplay === "none") {
			dayDisplay = "block"
			dayButtonStyle = "background-color: grey"
		}
		else {
			dayDisplay = "none"
			dayButtonStyle = ""
		}
	};
	function weekOnClick() {
		if(weekDisplay === "none") {
			weekDisplay = "block"
			weekButtonStyle = "background-color: grey"
		}
		else {
			weekDisplay = "none"
			weekButtonStyle = ""
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
				<button style={itemButtonStyle} on:click={newItemOnClick}>{itemButtonText}</button>
				<button class="d-none d-md-block" style={dayButtonStyle} on:click={dayOnClick}>Day</button>
				<button class="d-none d-md-block" style={weekButtonStyle} on:click={weekOnClick}>Week</button>

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
<div style="display:{dayDisplay}">
	<br>
	<DayAgenda/>
</div>
<div style="display:{weekDisplay}">
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