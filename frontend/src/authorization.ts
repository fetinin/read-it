import { User } from '@/types';
import axios from 'axios';
import jwt_decode from 'jwt-decode';

import store from './store';

interface TokenData {
  userID: string;
}

export const authorize = (token: string) => {
  const data: TokenData = jwt_decode(token);
  axios.get(`/users/${data.userID}`).then((resp) => {
    const user: User = resp.data;
    store.dispatch('saveUser', user);
  });
};
