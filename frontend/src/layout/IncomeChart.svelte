<script>

  import { onMount } from 'svelte';
  import Chart from 'svelte-frappe-charts';
  export let baseUrl;
  export let userId;

  let loading = true;
  let data = {};
  onMount(async() => {
    loading = true;
    const res = await fetch(`${baseUrl}/${userId}/income/time_series`)
    const time_series = await res.json()
    data = {
    labels: time_series["labels"],
    datasets: [
      {
        values: time_series["values"]
      }
    ]
  };
  loading = false;
  })

  
</script>

{#if !loading}
  {#if data.length != 0}
    <Chart data={data} type="line" />
  {:else}
    <p></p>
  {/if}
{:else}
  <div class="progress">
        <div class="indeterminate">
        </div>
    </div>
{/if}