<template>
<div class="upload-form">
    <form class="form-group" @submit.prevent="save" enctype="multipart/form-data">
        <h2 class="header">Загрузить книгу</h2>
        <label class="form-label" for="title">Название</label>
        <input v-model="title" class="form-input" type="text" id="title" placeholder="A Good Man Is Hard to Find and Other Stories" required>
        <label class="form-label" for="author">Автор</label>
        <input v-model='author' class="form-input" type="text" id="author" placeholder="Flannery O'Connor" required>

        <div class="dropbox">
          <input type="file" :disabled="isSaving" @change="onBookUpload($event.target.files)"
            accept="application/pdf,text/*,.epub" class="input-file" id="book" rяequired>
            <p v-if="isInitial">
              Перетащите вашу книгу сюда<br> или кликните чтобы открыть обозреватель
            </p>
            <p v-else>
                {{bookFile.name}}
            </p>
        </div>

        <div class="dropbox">
          <input type="file" :disabled="isSaving" @change="onBookCoverUpload($event.target.files)"
            accept="image/*" class="input-file" id="book-cover">
            <p v-if="!bookCoverFile.name">
              Перетащите обложку книги сюда<br> или кликните чтобы открыть обозреватель
            </p>
            <p v-else>
                {{bookCoverFile.name}}
            </p>
        </div>
        <button class="btn btn-primary">Загрузить</button>
    </form>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { File } from '@/types.ts';

const STATUS = {
  INITIAL: 0,
  SAVING: 1,
  SUCCESS: 2,
  FAILED: 3,
};

@Component({
  components: {},
})
export default class BookUpload extends Vue {
  public title = '';
  public author = '';
  public bookFile: File = { name: '', reader: new FileReader() };
  public bookCoverFile: File = { name: '', reader: new FileReader() };
  public currentStatus = STATUS.INITIAL;

  get isInitial() {
    return this.currentStatus === STATUS.INITIAL;
  }
  get isSaving() {
    return this.bookFile.reader.readyState === this.bookFile.reader.LOADING;
  }
  get isSuccess() {
    return this.bookFile.reader.readyState === this.bookFile.reader.DONE;
  }
  get isFailed() {
    return this.currentStatus === STATUS.FAILED;
  }

  private save(formData: any) {
    this.$http
      .post('/books', {
        title: this.title,
        author: this.author,
        file: (this.bookFile.reader.result as string).split('base64,').pop(),
        format: this.bookFile.name.split('.').pop(),
        cover: this.bookCoverFile.reader.result,
      })
      .then((response) => {
        this.$router.push({ name: 'book', params: { bookID: response.data.id } });
      })
      .catch((err) => console.log(err.response));
  }

  private onBookUpload(files: FileList) {
    if (!files.length) {
      return;
    }
    const file = files[0];
    this.bookFile.name = file.name;
    this.bookFile.reader.readAsDataURL(file);
    this.currentStatus = STATUS.SAVING;
    console.log(files);
  }
  private onBookCoverUpload(files: FileList) {
    if (!files.length) {
      return;
    }
    const file = files[0];
    this.bookCoverFile.name = file.name;
    this.bookCoverFile.reader.readAsDataURL(file);
    this.currentStatus = STATUS.SAVING;
    return;
  }
}
</script>

<style scoped>
.header {
  text-align: center;
  margin-bottom: 0;
}
.upload-form {
  margin: auto;
  width: 600px;
}
.note {
  color: #acb3c2;
}
button {
  margin-top: 20px;
  position: relative;
  left: 50%;
  transform: translate(-50%);
}

.dropbox {
  outline: 2px dashed grey;
  outline-offset: -10px;
  background: lightcyan;
  color: dimgray;
  padding: 10px 10px;
  min-height: 200px;
  position: relative;
  cursor: pointer;
  margin-top: 10px;
}

.input-file {
  opacity: 0; /* invisible but it's there! */
  width: 100%;
  height: 200px;
  position: absolute;
  cursor: pointer;
}

.dropbox:hover {
  background: lightblue;
}

.dropbox p {
  font-size: 1.2em;
  text-align: center;
  padding: 50px 0;
}
</style>
