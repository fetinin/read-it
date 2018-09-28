<template>
<header v-if="user" class="navbar">
  <section class="navbar-section">
    <router-link class="btn btn-link" to='/books'><img src="@/assets/icons/book_60x60.png" alt="book" class="img-icon bg-blue"><span class="hide-xs">Книги</span></router-link>
    <router-link class="btn btn-link" to='/upload-book'><img src="@/assets/icons/add_book_60x60.png" alt="book" class="img-icon bg-blue"><span class="hide-xs">Добавить книгу</span></router-link>
  </section>
  <section class="navbar-center"><img src="@/assets/logo.png" alt="ReadIT logo" class="img-responsive"></section>
  <section class="navbar-section">
      <div class="dropdown">
        <a href="#" class="btn-link dropdown-toggle" tabindex="0">
          <div class="user">
            <figure :class="['avatar', 'avatar-lg', {'no-bg': user.avatar}]" :data-initial="user.name[0].toUpperCase()">
              <img v-if="user.avatar" :src="'data:image/jpg;base64,' + user.avatar" alt="Avatar">
            </figure>
          </div>
        </a>
        <ul class="menu">
          <a @click.prevent="logout" href="#logout" class="btn btn-link">Выйти</a>
        </ul>
      </div>
  </section>
</header>

<header v-else class="navbar navbar-no-user">
  <section class="navbar-center"><img src="@/assets/logo.png" alt="ReadIT logo" class="img-responsive"></section>
</header>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { User } from '@/types';
import { logout as logoutUser } from '@/authorization';

@Component
export default class NavBar extends Vue {
  get user(): User {
    return this.$store.state.user;
  }
  private logout() {
    logoutUser();
    this.$router.push({ name: 'signup' });
  }
}
</script>

<style scoped>
.no-bg {
  background: transparent;
}
.navbar {
  min-height: 48px;
}
div.user > * {
  margin-right: 10px;
}
.navbar-center > img {
  height: 25px;
}
.bg-blue {
  background-color: #5755d9;
}
.img-icon {
  height: 25px;
  margin-right: 5px;
}
.navbar-no-user {
  justify-content: center;
}
</style>
