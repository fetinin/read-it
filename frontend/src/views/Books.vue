<template>
  <div class="books container grid-xl">
    <div class="columns">
      <BookCover class="column col-2 col-mg-4 col-md-4 col-sm-4 col-xs-6"
      v-for="book in books"
      :key="book.id"
      :book="book">
      </BookCover>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BookCover from '@/components/BookCover.vue';
import bookData from '@/data/books';
import { Book as BookType } from '@/types';

@Component({
  components: {
    BookCover,
  },
})
export default class BooksVue extends Vue {
  public books: BookType[] = [];
  private created() {
    // this.books = bookData;
    this.$http
      .get('/books')
      .then((resp) => {
        this.books = resp.data.map((el: any): BookType => {
          return {
            id: el.id,
            title: el.title,
            author: el.author,
            pages: [],
            coverURL: el.cover,
          };
        });
      })
      .catch((err) => console.log(err.response));
  }
}
</script>
<style scoped>
</style>
