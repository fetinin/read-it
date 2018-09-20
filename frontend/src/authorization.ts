import store from '@/store';
import { User } from '@/types';
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
    store.dispatch('saveUser', user);
    localStorage.setItem('jwt', token);
  });
};

export const logout = () => {
  store.dispatch('deleteUser');
  localStorage.removeItem('jwt');
  axios.defaults.headers.Authentication = null;
};
