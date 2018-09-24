import { updateArrayItem } from '@/tools';
import { Book, User } from '@/types';
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: null as null | User,
    books: null as null | Book[],
  },
  mutations: {
    saveBooks(state, books: Book[]) {
      state.books = books;
    },
    updateBook(state, book: Book) {
      if (state.books !== null) {
        state.books = updateArrayItem(state.books, book, 'id');
      }
    },
    deleteBook(state, bookID: string) {
      if (state.books !== null) {
        const index = state.books.findIndex((v) => v.id === bookID);
        state.books.splice(index, 1);
      }
    },
    clearBooks(state) {
      state.books = null;
    },
    saveUser(state, user: User) {
      state.user = user;
    },
    deleteUser(state, user: User) {
      state.user = null;
    },
  },
  actions: {},
  strict: process.env.NODE_ENV !== 'production',
});
