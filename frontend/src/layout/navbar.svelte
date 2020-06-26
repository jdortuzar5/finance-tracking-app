<script>
    import { Link } from 'svelte-routing'; 

</script>
  
<style>
.header {
  position: relative;
}
</style>

  <nav class="header">
    <div class="nav-wrapper blue z-deph-2">
     <div class="container">
         <Link href="/" class="brand-logo"><span class="brand-logo">Finance Tracker</span></Link>
      <ul id="nav-mobile" class="right hide-on-med-and-down">
        <li><Link to="/home">Home</Link></li>
        <li><Link to="/about">About</Link></li>
        <li><Link to="/login">Log out</Link></li>
        
      </ul>
     </div>
    </div>
  </nav>
   