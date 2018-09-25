<template>
    <div v-if='book !== null' class="book container">
        <div class="pages col-mx-auto" @wheel="handleScroll" ref="content">
          <p class="title">{{book.title}} - {{book.author}}</p>
          <transition name="fade-page" mode="out-in">
            <p class="page" v-html="book.pages[currentPage - 1]" :key="currentPage"></p>
          </transition>
          <p class="page-count">{{ currentPage }} / {{ pageTotal }}</p>
      </div>
    </div>

    <div v-else class="loading loading-lg" id="book-loader"></div>
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
  public book: Book | null = null;
  public currentPage = 1;

  public get pageTotal(): number {
    if (this.book !== null) {
      return this.book.pages.length;
    }
    return 0;
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

  private created() {
    document.addEventListener('keydown', this.handleKeyPress);
  }
  private mounted() {
    const bookID = this.$route.params.bookID;
    this.$http
      .get(`books/${bookID}`)
      .then((resp) => {
        this.book = {
          id: resp.data.book,
          author: resp.data.author,
          title: resp.data.title,
          pages: resp.data.pages,
          coverURL: resp.data.cover,
        } as Book;
      })
      .catch((err) => {
        console.error(err);
        if (err.response && err.response.status === 404) {
          this.$snotify.error('Не удалось найти книгу.');
        } else {
          this.$snotify.error('Не удалось загрузить книгу.');
        }
        this.$router.push({ name: 'books' });
      });
  }

  private destroyed() {
    document.removeEventListener('keydown', this.handleKeyPress);
  }
}
</script>
<style>
/* Styles are not scoped due to the fact that scoped styles are not applied to raw html */
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
.page img {
  max-width: 100%;
}
/* Animation */
.fade-page-enter-active,
.fade-page-leave-active {
  transition: opacity 0.3s;
}
.fade-page-enter,
.fade-page-leave-to {
  opacity: 0;
}
#book-loader {
  margin: auto;
}
</style>