import store from '@/store';
import { User } from '@/types';
import * as Sentry from '@sentry/browser';
import axios from 'axios';
import jwt_decode from 'jwt-decode';

interface TokenData {
  userID: string;
}

export const authorize = (token: string) => {
  axios.defaults.headers = { Authentication: token };

  const data: TokenData = jwt_decode(token);
  return axios.get(`/users/${data.userID}`).then((resp) => {
    const user: User = resp.data;
    store.commit('saveUser', user);
    localStorage.setItem('jwt', token);
    Sentry.configureScope((scope) =>
      scope.setUser({ id: user.id, username: user.name + user.surname }),
    );
  });
};

export const logout = () => {
  store.commit('deleteUser');
  localStorage.removeItem('jwt');
  axios.defaults.headers.Authentication = null;

  Sentry.configureScope((scope) => scope.clear());
};
