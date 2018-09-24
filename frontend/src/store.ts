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
        const index = state.books.findIndex((v) => v.id === book.id);
        if (index !== -1) {
          state.books[index] = book;
        } else {
          console.error(
            `Book with id ${book.id} not found and can't be updated.`,
          );
        }
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
