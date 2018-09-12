export interface Book {
  id: string;
  title: string;
  author: string;
  pages: string[];
  coverURL: string;
}

export interface File {
  name: string;
  reader: FileReader;
}

export interface User {
  id: string;
  name: string;
  surname: string;
}
