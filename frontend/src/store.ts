import { User } from '@/types';
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: null as null | User,
  },
  mutations: {
    saveUser(state, user: User) {
      state.user = user;
    },
    deleteUser(state, user: User) {
      state.user = null;
    },
  },
  actions: {
    saveUser({ commit }, user: User) {
      commit('saveUser', user);
    },
    deleteUser({ commit }, user: User) {
      commit('deleteUser', user);
    },
  },
  strict: process.env.NODE_ENV !== 'production',
});
