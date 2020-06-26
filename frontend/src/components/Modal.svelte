<script>
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let baseUrl;
  export let userId;
  export let usage;
  let amount = "";
  let date = "";
  let currency = "";
  let category = "";
  let loading = false;


  async function onSubmit(event) {
    event.preventDefault();

    if (amount.trim === "" || date.trim === "" || currency.trim === "") {
      return;
    }

    loading = true;
    const newPost = {
      user_uuid: userId,
      amount: amount,
      currency: currency,
      date: date,
      categories: {
        user_uuid: userId,
        name: category
      }
    };
    const newRow = {
      amount: amount,
      currency: currency,
      date: date,
      categories: {
        user_uuid: userId,
        name: category
      }
    }

    const res = await fetch(`${baseUrl}/${userId}/new_${usage}`, {
      method: "POST",
      body: JSON.stringify(newPost)
    });

    const post = await res.json();
    loading = false;
    dispatch("postCreated", [newRow])
    amount = "";
    date = "";
    currency = "";
    category = "";
    return false;
  }
</script>

<style>
  .progress {
    margin: 100px, 0px;
  }
  .datepicker {
    display: block;
    left: 40px;
    text-align: left;
    width: 130px;
    position: relative;
  }
</style>

{#if !loading}
  <form on:submit={onSubmit}>
    <div class="input-field">
      <label for="amount">Amount</label>
      <input type="number" bind:value={amount} min="1" />
    </div>
    <div class="input-field">
      <label for="date">Date</label>
      <input type="date" class="datepicker" bind:value={date} />
    </div>
    <div class="input-field">
      <label for="currency">Currency</label>
      <input type="text" bind:value={currency} />
    </div>
    <div class="input-field">
      <label for="category">Category</label>
      <input type="text" bind:value={category} />
    </div>
    <button class="btn waves-effect waves-light" type="submit">Submit</button>
  </form>
{:else}
  <div class="progress">
    <div class="indeterminate" />
  </div>
{/if}
