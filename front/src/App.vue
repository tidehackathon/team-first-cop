<template>
  <div id="app">
    <nav class="navbar navbar-expand navbar-app">
      <router-link to="/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96/search" class="navbar-brand">twi-parser</router-link>
      <div class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link to="/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96/add" class="nav-link">Add Channel</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96/search" class="nav-link">Search</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96/similarity" class="nav-link">Similarity</router-link>
        </li>
      </div>
    </nav>

    <div class="container mt-3">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "app"
};
</script>

<style>
  .navbar-app {
    background: #2faeb8;
    color: #fff;
  }

  .navbar-app a {
    color: #fff;
  }

  .nav-item {
    transition: .3s all;
  }

  .nav-item:hover {
    background: #ffc832;
    border-radius: 6px;
  }
</style>
