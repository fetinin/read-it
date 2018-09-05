<template>
<header class="navbar">
  <section class="navbar-section">
    <router-link class="btn btn-link" to='/books'>Книги</router-link>
    <router-link class="btn btn-link" to='/upload-book'>Upload</router-link>
  </section>
  <section class="navbar-center">ReadIT</section>
  <section class="navbar-section">
    <router-link class="btn btn-link" to='/login'>Login</router-link>
    <router-link class="btn btn-link" to='/signup'>Sign Up</router-link>
    <div class="user">
      <figure class="avatar avatar-lg" :data-initial="user.name[0].toUpperCase()" style="background-color: #5755d9;">
        <img v-if="user.profilePic" :src="user.profilePic" alt="Avatar">
      </figure>
    </div>
  </section>
</header>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { User } from '@/types';

@Component
export default class NavBar extends Vue {
  get user(): User {
    return {
      id: '123rweg453267yer',
      name: 'Denis',
      token: '1328432tq34yterhErfawerq2t',
      profilePic: '',
    };
  }
}
</script>

<style scoped>
div.user > * {
  margin-right: 10px;
}
</style>
