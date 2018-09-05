<template>
    <div class="modal active" id="modal-id">
        <a @click="confirm(false)" class="modal-overlay" aria-label="Close"></a>
        <div class="modal-container">
            <div class="modal-header">
            <a @click="confirm(false)" class="btn btn-clear float-right" aria-label="Close"></a>
            <div class="modal-title h5">
                <slot name="title"></slot>
            </div>
            </div>
            <div class="modal-body">
            <div class="content">
                <slot name="content"></slot>
            </div>
            </div>
            <div class="modal-footer">
            <button class="btn btn-link" @click="confirm(false)">Отмена</button>
            <button class="btn btn-primary" @click="confirm(true)">
                <slot name="confirmation"></slot>
            </button>
            </div>
        </div>
    </div>
</template>

<script lang='ts'>
import { Vue, Prop } from 'vue-property-decorator';

export default class App extends Vue {
  private confirm(isConfirmed: boolean) {
    this.$emit('is-confirmed', isConfirmed);
  }
}
</script>

<style>
</style>
