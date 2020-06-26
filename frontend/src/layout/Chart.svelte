<script>

  import { onMount, afterUpdate } from 'svelte';
  import Chart from 'svelte-frappe-charts';

  export let data;
  export let usage;
  export let baseUrl;
  export let userId;

  let loading = true;
  
  onMount(async() => {
    loading = false;

    if (data.length === 0){
      const res = await fetch(`${baseUrl}/${userId}/${usage}/time_series`)
      const time_series = await res.json();

      data = {
        labels: time_series["labels"],
        dataset: [
          {
            values: time_series["values"]
          }
        ]
      }

    }
  })

  afterUpdate(async () => {
    console.log("Prop updated")
    if (data.length === 0){
      const res = await fetch(`${baseUrl}/${userId}/${usage}/time_series`)
      const time_series = await res.json();

      data = {
        labels: time_series["labels"],
        dataset: [
          {
            values: time_series["values"]
          }
        ]
      }

    }
  })
  
</script>

{#if !loading}
  {#if data.length != 0}
    <Chart bind:data={data} type="line" />
  {:else}
    <p></p>
  {/if}
{:else}
  <div class="progress">
        <div class="indeterminate">
        </div>
    </div>
{/if}