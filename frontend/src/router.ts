import * as Sentry from '@sentry/browser';
import Vue from 'vue';
import Router from 'vue-router';

import { authorize } from './authorization';
import router from './router';
import store from './store';
import Book from './views/Book.vue';
import Books from './views/Books.vue';
import Signup from './views/Signup.vue';
import UploadBook from './views/UploadBook.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'books',
      component: Books,
      alias: '/books',
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
        const goToNextPage = to.params.nextPage
          ? () => next({ path: to.params.nextPage })
          : () => next({ name: 'books' });
        if (!store.state.user) {
          const token: string = to.query.access_token
            ? to.query.access_token
            : String(localStorage.getItem('jwt'));
          if (token === 'null') {
            return next({ name: 'signup' });
          }
          return authorize(token)
            .then(() => goToNextPage())
            .catch((err) => {
              console.error('Failed to authorize');
              console.error(err);
              Sentry.captureException(err);
              next({ name: 'signup' });
            });
        }
        goToNextPage();
      },
    },
    {
      path: '*',
      redirect: { name: 'books' },
    },
  ],
});

router.beforeEach((to, from, next) => {
  if (to.name === 'signup' || to.name === 'auth') {
    return next();
  }
  if (!store.state.user) {
    return next({ name: 'auth', params: { nextPage: to.fullPath } });
  }
  return next();
});
