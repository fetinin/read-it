import Vue from 'vue';
import Router from 'vue-router';

import Book from './views/Book.vue';
import Books from './views/Books.vue';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import Signup from './views/Signup.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/books',
      name: 'books',
      component: Books,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
    },
    {
      path: '/books/:bookID',
      name: 'book',
      component: Book,
      props: (route) => ({ bookID: Number(route.params.bookID) }),
      beforeEnter: (to, from, next) => {
        if (Number.isInteger(Number(to.params.bookID))) {
          return next();
        }
        return next(false);
      },
    },
  ],
});
