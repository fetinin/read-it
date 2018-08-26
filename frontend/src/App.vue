<template>
  <div id="app">
    <div id="nav">
      <NavBar></NavBar>
    </div>
    <div id="page-content">
      <router-view/>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';

import NavBar from './components/NavBar.vue';

@Component({
  components: { NavBar },
})
export default class App extends Vue {}
</script>


<style>
#nav {
  width: 60vw;
  margin: auto;
  padding-top: 10px;
  padding-bottom: 20px;
}
#page-content {
  display: flex;
}
.text-grey {
  color: #acb3c2;
}
@media (max-width: 840px) {
  #nav {
    width: 100vw;
  }
}
</style>
