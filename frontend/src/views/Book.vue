<template>
    <div class="book container">
        <div class="pages col-mx-auto" @wheel="handleScroll" ref="content">
          <p class="title">{{book.title}} - {{book.author}}</p>
          <transition name="fade" mode="out-in">
            <p class="page" v-html="formatPage(book.pages[currentPage - 1])" :key="currentPage"></p>
          </transition>
          <p class="page-count">{{ currentPage }} / {{ pageTotal }}</p>
      </div>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import BookCover from '@/components/BookCover.vue';
import books from '@/data/books';
import { Book } from '@/types';

@Component({
  components: {
    BookCover,
  },
})
export default class BookView extends Vue {
  public bookData: Book = { id: '', title: '', author: '', pages: [], coverURL: '' };
  public currentPage = 1;

  public get book(): Book {
    return this.bookData;
  }

  public get pageTotal(): number {
    return this.book.pages.length;
  }

  public nextPage() {
    if (this.currentPage < this.pageTotal) {
      this.currentPage += 1;
    }
  }

  public prevPage() {
    if (this.currentPage > 1) {
      this.currentPage -= 1;
    }
  }

  private handleScroll(evt: Event) {
    // console.log(evt)
  }

  private handleKeyPress(evt: KeyboardEvent) {
    if (evt.key === 'ArrowRight') {
      evt.preventDefault();
      this.nextPage();
    } else if (evt.key === 'ArrowLeft') {
      evt.preventDefault();
      this.prevPage();
    }
  }

  private formatPage(page: string) {
    // todo: should this be done on the backend beforehand?
    return page.replace(/\n/g, '<br>').replace(/ /g, '&nbsp');
  }

  private created() {
    document.addEventListener('keydown', this.handleKeyPress);
  }
  private mounted() {
    const bookID = this.$route.params.bookID;
    this.$http.get(`books/${bookID}`).then((resp) => {
      this.bookData = {
        id: resp.data.book,
        author: resp.data.author,
        title: resp.data.title,
        pages: resp.data.pages,
        coverURL: resp.data.cover,
      };
    });
  }

  private destroyed() {
    document.removeEventListener('keydown', this.handleKeyPress);
  }
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css?family=Open+Sans');
.pages {
  height: 90vh;
  word-wrap: break-word;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.page {
  font-family: 'Open Sans', sans-serif;
  overflow-y: auto;
  width: 100%;
  height: 100%;
  max-width: 960px;
}
/* Animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>