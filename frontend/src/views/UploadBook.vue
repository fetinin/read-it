<template>
<div class="upload-form">
    <form class="form-group" @submit.prevent="save" enctype="multipart/form-data">
        <h2 class="header">Загрузить книгу</h2>
        <label class="form-label" for="name">Название</label>
        <input v-model="name" class="form-input" type="text" id="name" placeholder="A Good Man Is Hard to Find and Other Stories" required>
        <label class="form-label" for="author">Автор</label>
        <input v-model='author' class="form-input" type="text" id="author" placeholder="Flannery O'Connor" required>

        <div class="dropbox">
          <input type="file" :name="uploadFieldName" :disabled="isSaving" @change="onBookUpload($event.target.files)"
            accept="text/*" class="input-file" required>
            <p v-if="isInitial">
              Перетащите вашу книгу сюда<br> или кликните чтобы открыть обозреватель
            </p>
            <p v-else>
                {{fileName}}
            </p>
        </div>
        <button class="btn btn-primary">Загрузить</button>
    </form>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

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
  public name = '';
  public author = '';
  public fileName = '';
  public uploadedFile: FileReader = new FileReader();
  public uploadError = null;
  public currentStatus = STATUS.INITIAL;
  public uploadFieldName = '';

  get isInitial() {
    return this.currentStatus === STATUS.INITIAL;
  }
  get isSaving() {
    return this.uploadedFile.readyState === this.uploadedFile.LOADING;
  }
  get isSuccess() {
    return this.uploadedFile.readyState === this.uploadedFile.DONE;
  }
  get isFailed() {
    return this.currentStatus === STATUS.FAILED;
  }

  private save(formData: any) {
    // upload data to the server

    console.log(formData);

    // upload(formData)
    //   .then(x => {
    //     this.uploadedFiles = [].concat(x);
    //     this.currentStatus = STATUS_SUCCESS;
    //   })
    //   .catch(err => {
    //     this.uploadError = err.response;
    //     this.currentStatus = STATUS_FAILED;
    //   });
  }

  private onBookUpload(files: FileList) {
    if (files.length) {
      const file = files[0];
      this.fileName = file.name;
      this.uploadedFile.readAsBinaryString(files[0]);
      this.currentStatus = STATUS.SAVING;
    } else {
      this.fileName = '';
      this.currentStatus = STATUS.INITIAL;
    }
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
  outline: 2px dashed grey; /* the dash box */
  outline-offset: -10px;
  background: lightcyan;
  color: dimgray;
  padding: 10px 10px;
  min-height: 200px; /* minimum height */
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
  background: lightblue; /* when mouse over to the drop zone, change color */
}

.dropbox p {
  font-size: 1.2em;
  text-align: center;
  padding: 50px 0;
}
</style>
