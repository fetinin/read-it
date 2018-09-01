<template>
    <div class="book-cover card">
        <router-link :to="{name: 'book', params: { bookID: book.id }}">
        <div class="card-image">
          <object :data="book.coverURL" class="img-responsive">
            <img src="https://via.placeholder.com/200x300" :alt="book.title" class="img-responsive">
          </object>
        </div>
        <div class="card-header">
            <div class="card-title h6">{{ book.title }}</div>
            <div class="card-subtitle text-gray">{{ book.author }}</div>
        </div>
        </router-link>
    </div>
</template>

<script lang='ts'>
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Book as BookType } from '@/types.ts';

@Component
export default class Book extends Vue {
  @Prop({ required: true })
  public book!: BookType;
}
</script>

<style scoped>
a {
  color: #807fe2;
  height: 100%;
}
.card-image {
  height: 65%;
}
.card-image:first-child {
  padding-top: 10px;
}
.card-image > object,
.card-image img {
  margin: auto;
  height: 100%;
  max-height: 300px;
}
.card-header {
  text-align: center;
  padding: 0.4rem;
}
.book-cover {
  height: 100%;
}
</style>
