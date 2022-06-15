<template>
  <ul class="list-group">
    <template v-for="item in items" :key="item.UID">
      <li class="list-group-item">
        <input
          class="form-check-input me-1"
          type="checkbox"
          :value="item['@id']"
          :checked="item['@id'] in selected"
          v-model="selected"
          @change="checked"
        />
        <a
          v-if="item.is_folderish"
          @click.prevent.stop="fetchData(item['@id'])"
          :href="item['@id']"
          class="list-group-item-action"
          >{{ item.title }}</a
        >
        <span v-else> {{ item.title }}</span>
      </li>
    </template>
  </ul>
</template>
<script>
export default {
  data() {
    return {
      selected: [],
    };
  },
  props: {
    items: {
      type: Array,
      required: true,
      default: () => {
        return [];
      },
    },
    selectedItems: {
      type: Array,
      required: true,
      default: () => {
        return [];
      },
    },
    fetchData: {
      type: Function,
      required: true,
      default: () => {
        return null;
      },
    },
  },
  mounted() {
    this.selected = this.selectedItems;
  },
  methods: {
    checked() {
      this.$emit("checked", this.selected);
    },
  },
};
</script>
