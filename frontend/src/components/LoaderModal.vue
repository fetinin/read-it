<template>
    <div v-if="showLoader" class="modal modal-sm active">
        <a class="modal-overlay" aria-label="Close"></a>
            <div class="loading loading-lg"></div>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class LoaderModal extends Vue {
  private showLoader = false;

  public show() {
    this.showLoader = true;
  }
  public hide() {
    this.showLoader = false;
  }
}
</script>

<style >
</style>
