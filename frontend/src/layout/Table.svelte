<script>
    import { onMount } from 'svelte';
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let usage;
    export let userId;
    export let baseUrl;
    export let updates;

    let usage_list = [];
    let new_list = [];

    let promise = onMount(async () => {
        const res = await fetch(`${baseUrl}/${userId}/${usage}`)
        new_list = await res.json();
        new_list = new_list["payload"];

        var i;
        for (i=0; i < new_list.length; i++){
            new_list[i] = JSON.parse(new_list[i])
        }
        
        dispatch("updatedTable", new_list)

    })
    
    async function deleteRow(row){
        console.log(row)
        const res = await fetch(`${baseUrl}/${userId}/delete_${usage}`, {
            method: "POST",
            body: JSON.stringify(row)
        })
        const deletedPost = await res.json()
        var index = updates.indexOf(row);
        if (index !== -1) updates.splice(index, 1);
        console.log(updates)
        updates = updates
        return false;
    }

   
</script>

<style>
    .delete-btn {
        color: red !important;
    }
</style>


<div class="row">
    {#await promise}
        <h4>Getting your {usage}.</h4>
    {:then}
        {#if updates.length === 0}
            <h4>You Dont have any {usage}</h4>
        {:else}
            <table class="highlight">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Ammount</th>
                        <th>Currency</th>
                        <th>Category</th>
                    </tr>
                </thead>
                <tbody>
                {#each updates as usage_row}
                    <tr>
                        <th>{usage_row.date}</th>
                        <th>{usage_row.amount}</th>
                        <th>{usage_row.currency}</th>
                        <th>{usage_row.categories.name}</th>
                        <th><a class="delete-btn" on:click={() => deleteRow(usage_row)}>Delete</a></th>
                    </tr>
                {/each}
                </tbody>
            </table>
            
        {/if}
    {/await}

</div>