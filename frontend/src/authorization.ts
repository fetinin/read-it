import { User } from '@/types';
import axios from 'axios';
import jwt_decode from 'jwt-decode';

import store from './store';

interface TokenData {
  userID: string;
}

export const authorize = (token = '') => {
  token = token ? token : String(localStorage.getItem('jwt'));
  if (token === 'null') {
    throw Error('No jwt provided.');
  }
  axios.defaults.headers = { Authentication: token };

  const data: TokenData = jwt_decode(token);
  return axios
    .get(`/users/${data.userID}`)
    .then((resp) => {
      const user: User = resp.data;
      store.dispatch('saveUser', user);
      localStorage.setItem('user', JSON.stringify(user));
      localStorage.setItem('jwt', token);
    })
    .catch((err) => console.error(err));
};

export const logout = () => {
  store.dispatch('deleteUser');
  localStorage.removeItem('user');
  localStorage.removeItem('jwt');
  axios.defaults.headers.Authentication = null;
};
