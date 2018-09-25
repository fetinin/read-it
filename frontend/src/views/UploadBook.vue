<template>
<div class="upload-form">
  <loader-modal ref='loader'></loader-modal>

    <form class="form-group" @submit.prevent="save" enctype="multipart/form-data">
        <h2 v-if="currentStep === 1" class="header">Выбери книгу</h2>
        <h2 v-else-if="currentStep === 2" class="header">Добавь название</h2>

        <ul class="step">
          <li :class="['step-item', {'active': currentStep === 1}]">
            <a href="#" class="tooltip" data-tooltip="Выбери книгу">Шаг 1</a>
          </li>
          <li :class="['step-item', {'active': currentStep === 2}]">
            <a href="#" class="tooltip" data-tooltip="Задай название и обложку">Шаг 2</a>
          </li>
        </ul>

        <div id="step1" v-if="currentStep === 1">
          <div class="dropbox">
            <input type="file" @change="onBookUpload($event.target.files)"
              accept="application/pdf,.txt,.epub" class="input-file" id="book" rяequired>
            <p>
              Перетащите вашу книгу сюда<br> или кликните чтобы открыть обозреватель.<br>
              Сейчас поддерживаются форматы: pdf, epub, txt.
            </p>
          </div>
        </div>

        <div id="step2"  v-else-if="currentStep === 2">
          <div class="columns">
            <div class="column col-8 col-sm-12">
              <label class="form-label" for="title">Название</label>
              <input v-model="title" class="form-input" type="text" id="title" placeholder="A Good Man Is Hard to Find and Other Stories" required>
              <label class="form-label" for="author">Автор</label>
              <input v-model='author' class="form-input" type="text" id="author" placeholder="Flannery O'Connor" required>
            </div>

            <div class="column col-4 col-sm-12">
              <label class="form-label text-center" for="cover">Обложка</label>
              <div :class="['dropbox-img', 'text-center', {'dropbox-no-image':  !coverImgData}]" :style="{ 'background-image': `url(${coverImgData})` }">
                <input type="file" @change="onBookCoverUpload($event.target.files)" accept="image/*" class="input-file" id="book-cover">
                <p v-if="!coverImgData">
                  Перетащите обложку книги сюда<br> или кликните чтобы открыть обозреватель
                </p>
              </div>
            </div>
          </div>
          <button class="btn btn-primary">Готово!</button>
        </div>
    </form>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { File, Book } from '@/types.ts';
import LoaderModal from '@/components/LoaderModal.vue';

const FILE_LOAD_STATUS = {
  INITIAL: 0,
  SAVING: 1,
  SUCCESS: 2,
  FAILED: 3,
};

@Component({
  components: { LoaderModal },
})
export default class BookUpload extends Vue {
  public title = '';
  public author = '';
  public bookFile: File = { name: '', reader: new FileReader() };
  public bookCoverFile: File = { name: '', reader: new FileReader() };
  public coverImgData: null | string = null;

  private currentStep = 1;

  private save(formData: any) {
    const loader = this.$refs.loader as LoaderModal;
    loader.show();
    this.$http
      .post(
        '/books',
        {
          title: this.title,
          author: this.author,
          file: (this.bookFile.reader.result as string).split('base64,').pop(),
          format: this.bookFile.name.split('.').pop(),
          cover: this.coverImgData,
        },
        { timeout: 120000 }, // 2 minutes timeout
      )
      .then((response) => {
        this.$store.commit('clearBooks');
        this.$router.push({ name: 'book', params: { bookID: response.data.id } });
      })
      .catch((err) => {
        console.log(err.response);
      })
      .finally(() => loader.hide());
  }

  private onBookUpload(files: FileList) {
    if (!files.length) {
      return;
    }
    const file = files[0];
    this.bookFile.name = file.name;
    this.bookFile.reader.readAsDataURL(file);
    this.bookFile.reader.onloadend = () => this.currentStep++;
  }
  private onBookCoverUpload(files: FileList) {
    if (!files.length) {
      return;
    }
    const file = files[0];
    this.bookCoverFile.name = file.name;
    this.bookCoverFile.reader.readAsDataURL(file);
    return;
  }

  private created() {
    this.bookCoverFile.reader.onloadend = (event: ProgressEvent) => {
      const result = (event.target as FileReader).result as string;
      this.coverImgData = result;
    };
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
  height: 100%;
  position: absolute;
  cursor: pointer;
  top: 0px;
  left: 0px;
}

.dropbox:hover {
  background: lightblue;
}

.dropbox p {
  font-size: 1.2em;
  text-align: center;
  padding: 50px 0;
}

.dropbox-img {
  color: dimgray;
  width: 100%;
  padding: 10px 10px;
  height: 100%;
  position: relative;
  cursor: pointer;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
}

.dropbox-img > p {
  padding: 5px;
}

.dropbox-no-image {
  outline: 2px dashed grey;
  outline-offset: -10px;
  background-color: lightcyan;
}

.dropbox-no-image:hover {
  background-color: lightblue;
}
</style>
