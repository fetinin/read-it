<template>
    <div v-if='book !== null' class="book container">
        <div class="pages col-mx-auto" @wheel="handleScroll" ref="content">
          <p class="title hide-sm">{{book.title}} - {{book.author}}</p>

            <transition name="fade-page" mode="out-in">
              <div
               class="page"
               v-html="book.pages[currentPage - 1]" :key="currentPage"
               v-touch:tap="handleTap"
               v-touch:swipe="handleSwipe"
               ref="page">
            </div>
            </transition>
            
          
          <p class="page-count">{{ currentPage }} / {{ pageTotal }}</p>
      </div>
    </div>

    <div v-else class="loading loading-lg" id="book-loader"></div>
</template>

<script lang="ts">
import { Component, Watch, Vue } from 'vue-property-decorator';

import BookCover from '@/components/BookCover.vue';
import books from '@/data/books';
import { Book } from '@/types';
import { setTimeout, clearTimeout } from 'timers';

@Component({
  components: {
    BookCover,
  },
})
export default class BookView extends Vue {
  public book: Book | null = null;
  public currentPage = 1;

  private saveOnTimeoutID: NodeJS.Timer | null = null;

  public get pageTotal(): number {
    if (this.book !== null) {
      return this.book.pages.length;
    }
    return 0;
  }

  public goNextPage() {
    if (this.currentPage < this.pageTotal) {
      this.currentPage += 1;
      (this.$refs.page as Element).scrollTop = 0;
    }
  }

  public goPrevPage() {
    if (this.currentPage > 1) {
      this.currentPage -= 1;
      (this.$refs.page as Element).scrollTop = 0;
    }
  }

  @Watch('currentPage')
  private onPageChange(newPage: number, prevPage: number) {
    if (this.saveOnTimeoutID !== null) {
      clearTimeout(this.saveOnTimeoutID);
    }
    const savePage = () =>
      this.$http
        .patch(`books/${(this.book as Book).id}`, { page_active: this.currentPage })
        .catch((err) => {
          console.error(err);
          this.$snotify.error('Не удалось запомнить страницу.');
        });
    this.saveOnTimeoutID = setTimeout(savePage, 3000);
  }

  private handleScroll(evt: Event) {
    // console.log(evt);
  }

  private handleTap(event: TouchEvent) {
    const element = event.srcElement as Element;
    const xPosition = event.changedTouches[0].clientX;
    const oneThirdWidth = element.clientWidth / 3;
    if (xPosition <= oneThirdWidth) {
      this.goPrevPage();
    } else if (xPosition >= oneThirdWidth * 2) {
      this.goNextPage();
    }
  }

  private handleSwipe(direction: string) {
    if (direction === 'left') {
      this.goNextPage();
    } else if (direction === 'right') {
      this.goPrevPage();
    }
  }

  private handleKeyPress(evt: KeyboardEvent) {
    if (evt.key === 'ArrowRight') {
      evt.preventDefault();
      this.goNextPage();
    } else if (evt.key === 'ArrowLeft') {
      evt.preventDefault();
      this.goPrevPage();
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
          id: resp.data.id,
          author: resp.data.author,
          title: resp.data.title,
          pages: resp.data.pages,
          coverURL: resp.data.cover,
        } as Book;
        this.currentPage = resp.data.page_active;
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
.title,
.page-count {
  margin-bottom: 0.1rem;
}
.pages {
  height: 100%;
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
  font-size: 1rem;
}
.page-count {
  color: #acb3c2;
}
.page img {
  max-width: 100%;
}
#book-loader {
  margin: auto;
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
</style>