<template>
  <ul class="list-group">
    <template v-for="item in items" :key="item.UID">
      <li class="list-group-item">
        <input
          class="form-check-input me-1"
          :type="inputType"
          :value="item['@id']"
          :checked="item['@id'] in selectedProxy"
          :selected="item['@id'] in selectedProxy"
          v-model="selectedProxy"
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
    inputType: {
      type: String,
      required: true,
      default: () => {
        return "checkbox";
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
  computed: {
    selectedProxy: {
      get() {
        return this.selected;
      },
      set(value) {
        if (this.inputType == "checkbox") {
          this.selected = value;
        } else {
          this.selected = [value];
        }
      },
    },
  },
};
</script>
