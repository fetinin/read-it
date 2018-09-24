<template>
    <div class="upload-form">
    <form class="form-group">
        <div class="columns">
            <div class="column col-8 col-sm-12">
                <label class="form-label" for="title">Название</label>
                <input v-model="data.title" class="form-input" type="text" id="title" placeholder="A Good Man Is Hard to Find and Other Stories" required>
                <label class="form-label" for="author">Автор</label>
                <input v-model='data.author' class="form-input" type="text" id="author" placeholder="Flannery O'Connor" required>
            </div>
            <div class="column col-4 col-sm-12">
                <label class="form-label text-center" for="cover">Обложка</label>
                <div :class="['dropbox', {'dropbox-no-image':  !data.coverURL}]" :style="{ 'background-image': `url(${data.coverURL})` }">
                <input type="file" @change="onBookCoverUpload($event.target.files)" accept="image/*" class="input-file" id="book-cover">
                    <p v-if="!data.coverURL">
                    Перетащите обложку книги сюда<br> или кликните чтобы открыть обозреватель
                    </p>
                </div>
            </div>
        </div>
    </form>
</div>
</template>

<script lang='ts'>
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Book as BookType, File } from '@/types.ts';
import Modal from '@/components/Modal.vue';

@Component
export default class Book extends Vue {
  @Prop() public book!: BookType;

  public bookCoverFile = { name: '', reader: new FileReader() };

  public data: BookType = {
    id: this.book.id,
    title: this.book.title,
    author: this.book.author,
    coverURL: this.book.coverURL,
    pages: this.book.pages,
  };

  private onBookCoverUpload(files: FileList) {
    if (files.length) {
      const file = files[0];
      this.bookCoverFile.name = file.name;
      this.bookCoverFile.reader.readAsDataURL(file);
    }
  }

  private created() {
    this.bookCoverFile.reader.onloadend = (event: ProgressEvent) => {
      const result = (event.target as FileReader).result as string;
      this.data.coverURL = result;
    };
  }
}
</script>

<style scoped>
.dropbox {
  color: dimgray;
  width: 100%;
  padding: 10px 10px;
  min-height: 200px;
  position: relative;
  cursor: pointer;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

.dropbox-no-image {
  outline: 2px dashed grey;
  outline-offset: -10px;
  background-color: lightcyan;
}

.dropbox-no-image:hover {
  background-color: lightblue;
}

.input-file {
  opacity: 0; /* invisible but it's there! */
  width: 100%;
  height: 200px;
  position: absolute;
  cursor: pointer;
}

.dropbox p {
  font-size: 1.2em;
  text-align: center;
}
</style>
