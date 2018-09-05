export interface Book {
  id: string;
  title: string;
  author: string;
  pages: string[];
  coverURL: string;
}

export interface User {
  id: string;
  name: string;
  token: string;
  profilePic: string;
}

export interface File {
  name: string;
  reader: FileReader;
}
