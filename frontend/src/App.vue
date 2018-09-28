<template>
  <div id="app">
    <vue-snotify></vue-snotify>
    <div id="nav">
      <NavBar></NavBar>
    </div>
    <div id="page-content">
      <transition name="fade-page" mode="out-in">
        <router-view/>
      </transition>
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
/* Animation */
.fade-page-enter-active,
.fade-page-leave-active {
  transition: opacity 0.1s;
}
.fade-page-enter,
.fade-page-leave-to {
  opacity: 0;
}
</style>
