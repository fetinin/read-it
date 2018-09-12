<template>
<header class="navbar">
  <section class="navbar-section">
    <router-link class="btn btn-link" to='/books'>Книги</router-link>
    <router-link class="btn btn-link" to='/upload-book'>Upload</router-link>
  </section>
  <section class="navbar-center">ReadIT</section>
  <section class="navbar-section">
    <template v-if="user">
      <a @click.prevent="logout" href="#logout" class="btn btn-link">Logout</a>
      <div class="user">
        <figure class="avatar avatar-lg" :data-initial="user.name[0].toUpperCase()" style="background-color: #5755d9;">
          <img v-if="user.profilePic" :src="user.profilePic" alt="Avatar">
        </figure>
      </div>
    </template>
    <template v-else>
      <router-link class="btn btn-link" to='/login'>Login</router-link>
    <router-link class="btn btn-link" to='/signup'>Sign Up</router-link>
    </template>
  </section>
</header>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { User } from '@/types';

@Component
export default class NavBar extends Vue {
  get user(): User {
    return this.$store.state.user;
  }
  private logout() {
    this.$store.dispatch('deleteUser');
  }
}
</script>

<style scoped>
.navbar {
  min-height: 48px;
}
div.user > * {
  margin-right: 10px;
}
</style>
