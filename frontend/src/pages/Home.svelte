<script>
    import { onMount } from 'svelte';
    import Modal from "../components/Modal.svelte";
    import Table from "../layout/Table.svelte";
    import Chart from "../layout/Chart.svelte"
    
    export let baseUrl;
    export let userId = "";
    export let updatedIncomes;
    export let updatedSpending;

    let incomeChartDates = [];
    let spendingChartDates = [];
    let incomeChartAmounts = [];
    let spendingChartAmounts = [];
    let incomeChart = {};
    let spendingChart = {};

    let loading = true;

    onMount(async () => {

        loading = false
        incomeChart = {
        labels: incomeChartDates,
        datasets: [
                    {
                        values: incomeChartAmounts
                    }
                ]
        }

        spendingChart = {
        labels: spendingChartDates,
        datasets: [
                    {
                        values: spendingChartAmounts
                    }
                ]
        }

    });
    
    function cleanUpdates(updatedDates, updatedAmounts, updates){
        var i;
        let init_date_length = updatedDates.length
        let init_amount_length = updatedAmounts.length
        for(i=0; i<updates.length; i++){
            let cleanDate = updates[i]["date"].substr(0, 7);
            updatedDates[init_date_length + i] = cleanDate 
            updatedAmounts[init_amount_length + i] = updates[i]["amount"]
        }
    }

    function updateChartData(updatedDates, updatedAmounts, data){
        data = {
        labels: updatedDates,
        datasets: [
                    {
                        values: updatedAmounts
                    }
                ]
        }
    }

    function addIncome({detail: post}){
        console.log("New Income Post")
        console.log(post)
        cleanUpdates(incomeChartDates, incomeChartAmounts, post)
        updateChartData(incomeChartDates, incomeChartAmounts, incomeChart)
        updatedIncomes = [...updatedIncomes,...post]
        console.log("Break")

    }
    function addSpending({detail: post}){
        console.log("New Spending Post")
        console.log(post)
        cleanUpdates(spendingChartDates, spendingChartAmounts, post)
        updateChartData(spendingChartDates, spendingChartAmounts, spendingChart)
        updatedSpending = [...updatedSpending,...post]
        console.log("Break")
    }
    
</script>
{#if !loading}
    <h1>Incomes</h1>
    <Modal baseUrl={baseUrl} userId={userId} on:postCreated={addIncome} usage="income"/>
    <Table usage="income" {userId} {baseUrl} updates={updatedIncomes} on:updatedTable={addIncome}/>
    <Chart bind:data={incomeChart} usage="income" {userId} {baseUrl} />
    
    <h1>Spendings</h1>

    <Modal baseUrl={baseUrl} userId={userId} on:postCreated={addSpending} usage="spending"/>
    <Table usage="spending" {userId} {baseUrl} updates={updatedSpending} on:updatedTable={addSpending}/>
    <Chart bind:data={spendingChart} usage="spending" {userId} {baseUrl} />
{:else}
    <div class="progress">
        <div class="indeterminate">
        </div>
    </div>
{/if}
