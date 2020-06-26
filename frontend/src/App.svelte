<script>
    import '../node_modules/materialize-css/dist/css/materialize.css';
    import '../node_modules/materialize-css/dist/js/materialize.js';

    import { Router, Route } from "svelte-routing";

    import Navbar from './layout/navbar.svelte';
    import Home from './pages/Home.svelte';
    import About from './pages/About.svelte';
    import Login from "./pages/Login.svelte";

    const baseUrl = 'http://0.0.0.0:8000';
    let userId = "";
    let updatedIncomes = [];
    let updatedSpending = [];
    function logInCallBack(event){
        userId = event.detail["payload"]
    }
</script>

<style>
</style>

<Router>
    <Navbar/>
    <div class="container">
        <Route path="/">
            {#if userId == ""  }
                <Login {baseUrl} on:logIn={logInCallBack}/>
            {:else}
                <Home {baseUrl} {userId} {updatedIncomes} {updatedSpending}/>
            {/if}
        </Route>
        <Route path="/home" >
            <Home {baseUrl} {userId}/>
        </Route>
        <Route path="/about" component={About}/>
    </div>

</Router>
