<template>
  <div ref="root">
    <input type="hidden" value="hans" name="hans" />
    <button
      type="button"
      class="btn btn-primary"
      data-bs-toggle="modal"
      data-bs-target="#reference-widget-modal"
    >
      Browse
    </button>
    <div
      id="reference-widget-modal"
      class="modal fade"
      tabindex="-1"
      aria-labelledby="ref-modal-title"
      aria-hidden="true"
      ref="modal"
    >
      <div class="modal-dialog modal-dialog-scrollable modal-xl">
        <div class="modal-content">
          <div class="modal-header">Choose content</div>
          <div class="modal-body">
            <searchForm @search="search" @reset="reset" />
            <nav aria-label="breadcrumb">
              <ol class="breadcrumb">
                <li class="breadcrumb-item">
                  <a
                    :href="portalURL"
                    @click.prevent.stop="fetchData(portalURL)"
                    >Startpage</a
                  >
                </li>
                <template
                  v-for="(item, index) in breadcrumbs"
                  :key="item['@id0']"
                >
                  <li
                    class="breadcrumb-item"
                    v-if="index != breadcrumbs.length - 1"
                  >
                    <a
                      :href="item['@id']"
                      @click.stop.prevent="fetchData(item['@id'])"
                      >{{ item.title }}</a
                    >
                  </li>
                  <li v-else class="breadcrumb-item active" aria-current="page">
                    {{ item.title }}
                  </li>
                </template>
              </ol>
            </nav>

            <Pagination
              v-if="data.batching"
              @next="fetchData"
              @previous="fetchData"
              :batching="data.batching"
            />
            total {{ data.items_total }}

            <ul class="list-group">
              <template v-for="item in data.items" :key="item.UID">
                <li class="list-group-item">
                  <input
                    class="form-check-input me-1"
                    type="checkbox"
                    :value="item['@id']"
                    :checked="item['@id'] in selected"
                    v-model="selected"
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
          </div>

          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Pagination from "@/components/Pagination.vue";
import SearchForm from "@/components/searchForm.vue";
export default {
  components: {
    Pagination,
    SearchForm,
  },
  data() {
    return {
      portalURL: "",
      baseURL: "",
      startURL: "",
      fieldName: "",
      type: "",
      translations: {},
      data: {},
      breadcrumbs: [],
      selected: [],
      formData: {
        searchTerm: "",
        sortOn: "getObjPositionInParent",
        sortOrder: "ascending",
      },
    };
  },
  created() {
    this.baseURL = document.body.getAttribute("data-base-url");
    this.portalURL = document.body.getAttribute("data-portal-url");
  },
  mounted() {
    const wrapperElement = this.$refs.root.parentElement;
    this.startURL = wrapperElement.getAttribute("data-starturl");
    this.fieldName = wrapperElement.getAttribute("data-fieldname");
    this.type = wrapperElement.getAttribute("data-type");
    this.translations = JSON.parse(
      wrapperElement.getAttribute("data-translations")
    );

    this.$refs.modal.addEventListener("show.bs.modal", () => {
      this.fetchData(this.startURL);
    });
  },
  methods: {
    async fetchData(url, options) {
      let params = {
        metadata_fields: ["UID", "is_folderish"],
        sort_on: this.formData.sortOn,
        sort_order: this.formData.sortOrder,
      };

      if (!url) {
        url = this.data["@id"];
      }

      const isSearch = url.indexOf("/@search") != -1;

      if (options) {
        params = Object.assign(params, options);
      }

      if (!isSearch) {
        params.expand = "breadcrumbs";
      }

      const response = await this.axios.get(url, { params: params });

      this.data.items = response.data.items;
      this.data.items_total = response.data.items_total;
      this.data.batching = response.data.batching;

      if (!isSearch) {
        this.data["@id"] = response.data["@id"];
      }
      if (response.data["@components"]) {
        this.breadcrumbs = response.data["@components"].breadcrumbs.items;
      }
    },
    search(formData) {
      this.formData = Object.assign({}, this.formData, formData);
      const url = this.data["@id"] + "/@search";
      const currentURL = new URL(this.data["@id"]);
      let options = { "path.query": currentURL.pathname, "path.depth": 1 };
      if (this.formData.searchTerm.length > 2) {
        options.SearchableText = "*" + this.formData.searchTerm + "*";
        options["path.depth"] = -1;
      }
      this.fetchData(url, options);
    },
    reset(formData) {
      this.formData = formData;
      this.fetchData(this.startURL);
    },
  },
};
</script>
