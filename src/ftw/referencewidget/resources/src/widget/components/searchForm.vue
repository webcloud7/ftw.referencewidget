<template>
  <div class="row my-2 gy-2 gx-3 align-items-center">
    <div class="col">
      <div class="form-floating">
        <select
          class="form-select"
          id="sortattr"
          :aria-label="$i18n('Sort on')"
          v-model="sortOn"
          @change="() => search()"
        >
          <template
            v-for="(option, index) in sortAttribute"
            :key="option.value"
          >
            <option :selected="index == 0" :value="option.value">
              {{ option.title }}
            </option>
          </template>
        </select>
        <label for="sortattr">{{ $i18n("Sort on") }}</label>
      </div>
    </div>
    <div class="col">
      <div class="form-floating">
        <select
          class="form-select"
          id="sortorder"
          :aria-label="$i18n('Sort order')"
          v-model="sortOrder"
          @change="() => search()"
        >
          <option selected value="ascending">{{ $i18n("Ascending") }}</option>
          <option selected value="descending">{{ $i18n("Descending") }}</option>
        </select>
        <label for="sortorder">{{ $i18n("Sort order") }}</label>
      </div>
    </div>
    <div class="col">
      <div class="form-floating">
        <input
          type="text"
          class="form-control"
          id="searchFilter"
          placeholder="Text"
          v-model="searchTerm"
          @keydown.enter.prevent="search"
        />
        <label for="searchFilter">{{ $i18n("Search text") }}</label>
      </div>
    </div>
    <div class="col">
      <button type="button" class="btn btn-primary" @click="search">
        {{ $i18n("Search") }}
      </button>
      <button type="button" class="btn btn-danger" @click="reset">
        {{ $i18n("Reset") }}
      </button>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      searchTerm: "",
      sortOn: "getObjPositionInParent",
      sortOrder: "ascending",
      sortAttribute: [
        { title: this.$i18n("Relevance"), value: "" },
        { title: this.$i18n("Position"), value: "getObjPositionInParent" },
        { title: this.$i18n("Title"), value: "sortable_title" },
        { title: this.$i18n("Created"), value: "created" },
        { title: this.$i18n("Modified"), value: "modified" },
      ],
    };
  },
  methods: {
    search() {
      if (this.searchTerm && this.sortOn == "getObjPositionInParent") {
        this.sortOn = "";
      }

      this.$emit("search", {
        searchTerm: this.searchTerm,
        sortOn: this.sortOn,
        sortOrder: this.sortOrder,
      });
    },
    reset() {
      this.searchTerm = "";
      this.sortOn = "getObjPositionInParent";
      this.sortOrder = "ascending";
      this.$emit("reset", {
        searchTerm: "",
        sortOn: "getObjPositionInParent",
        sortOrder: "ascending",
      });
    },
  },
};
</script>
