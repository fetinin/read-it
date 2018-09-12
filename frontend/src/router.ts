import Vue from 'vue';
import Router from 'vue-router';

import { authorize } from './authorization';
import Book from './views/Book.vue';
import Books from './views/Books.vue';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import Signup from './views/Signup.vue';
import UploadBook from './views/UploadBook.vue';

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
      path: '/upload-book',
      name: 'uploadBook',
      component: UploadBook,
    },
    {
      path: '/books/:bookID',
      name: 'book',
      component: Book,
      props: (route) => ({ bookID: route.params.bookID }),
    },
    {
      path: '/authenticated/',
      name: 'auth',
      beforeEnter: (to, from, next) => {
        if (to.query.access_token) {
          authorize(to.query.access_token);
        }
        return next({ name: 'books' });
      },
    },
  ],
});
