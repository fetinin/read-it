<template>
<header class="navbar">
  <section class="navbar-section">
    <router-link class="btn btn-link" to='/books'>Книги</router-link>
    <router-link class="btn btn-link" to='/login'>Login</router-link>
    <router-link class="btn btn-link" to='/signup'>Sign Up</router-link>
  </section>
  <section class="navbar-center">ReadIT</section>
  <section class="navbar-section">
    <div class="user">
      <figure class="avatar avatar-lg" data-initial="D" style="background-color: #5755d9;">
        <!-- If has image -->
        <!-- <img src="" alt="Avatar"> -->
      </figure>
    </div>
  </section>
</header>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class NavBar extends Vue {}
</script>

<style scoped>
div.user > * {
  margin-right: 10px;
}
</style>
