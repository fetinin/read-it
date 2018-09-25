<template>
  <div id="app">
    <vue-snotify></vue-snotify>
    <div v-if="user" id="nav">
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
export default class App extends Vue {
  get user() {
    return this.$store.state.user;
  }
}
</script>


<style>
#nav {
  height: 70px;
  width: 60vw;
  margin: auto;
  padding-top: 10px;
  padding-bottom: 20px;
}
#page-content {
  display: flex;
  height: 90vh;
}
.text-grey {
  color: #acb3c2;
}
@media (max-width: 840px) {
  #nav {
    width: 100vw;
  }
}
html,
body,
#app {
  height: 100%;
}
</style>
