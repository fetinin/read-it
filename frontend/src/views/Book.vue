<template>
    <div class="book container">
        <div class="text col-mx-auto" @wheel="handleScroll" ref="content">
            <p class="title">{{book.title}} - {{book.author}}</p>
            <div v-html="book.text" ref="text"></div>
        </div>
        <p class="page-count">{{ currentPage }} / {{ pageTotal }}</p>
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
  @Prop({ required: true, type: Number })
  public bookID!: number;

  public book!: Book;
  public currentPage = 1;
  public pageTotal = 0;

  public nextPage() {
    const elem = this.$refs.content as HTMLElement;
    const offset = elem.offsetWidth + 500;
    const prevStep = !['', null].includes(elem.style.left)
      ? parseInt(elem.style.left as string, 10)
      : 0;
    const step = prevStep - offset;
    // if (Math.abs(step + offset) < (this.$refs.text as HTMLElement).offsetHeight) {
    elem.style.cssText = `left: ${step}px`;
    this.currentPage += 1;
    // }
  }

  public prevPage() {
    const elem = this.$refs.content as HTMLElement;
    let step = elem.offsetWidth + 500;
    const prevStep = !['', null].includes(elem.style.left)
      ? parseInt(elem.style.left as string, 10)
      : 0;
    step = prevStep + step;
    if (step <= 0) {
      elem.style.cssText = `left: ${step}px`;
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
    this.book = books[this.bookID - 1];
    this.book.text = this.book ? this.book.text.replace('\n', '<br>') : '';
    document.addEventListener('keydown', this.handleKeyPress);
  }
  private mounted() {
    const contentWidth = (this.$refs.content as HTMLElement).offsetWidth;
    const textWidth = (this.$refs.text as HTMLElement).offsetHeight;
    this.pageTotal = 1 + Math.round(textWidth / (contentWidth + 500));
    console.log(this.book.text.length);
  }

  private destroyed() {
    document.removeEventListener('keydown', this.handleKeyPress);
  }
}
</script>
<style scoped>
.text {
  max-height: 90vh;
  column-gap: 500px;
  word-wrap: break-word;
  column-width: 90vw;
  width: 85%;
  position: relative;
  transition: left 0.3s linear;
  left: 0;
}
.page-count {
  position: fixed;
  left: 50%;
  -webkit-transform: translateX(-50%);
  transform: translateX(-50%);
  bottom: -10px;
}
</style>
