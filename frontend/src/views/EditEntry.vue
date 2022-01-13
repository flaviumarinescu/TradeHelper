<template>
  <section>
    <h1>Edit Entry</h1>
    <hr />
    <br />

    <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="setup" class="form-label">Setup:</label>
        <input
          type="text"
          name="setup"
          v-model="form.setup"
          class="form-control"
        />
      </div>
      <div class="mb-3">
        <label for="order" class="form-label">Order:</label>
        <textarea
          name="order"
          v-model="form.order"
          class="form-control"
        ></textarea>
      </div>
      <div class="mb-3">
        <label for="result" class="form-label">Result:</label>
        <textarea
          name="result"
          v-model="form.result"
          class="form-control"
        ></textarea>
      </div>
      <div class="mb-3">
        <label for="obs" class="form-label">Observations:</label>
        <textarea
          name="obs"
          v-model="form.obs"
          class="form-control"
        ></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </section>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "EditEntry",
  props: ["id"],
  data() {
    return {
      form: {
        setup: "",
        order: "",
        result: "",
        obs: "",
      },
    };
  },
  created: function () {
    this.GetEntry();
  },
  computed: {
    ...mapGetters({ entry: "stateEntry" }),
  },
  methods: {
    ...mapActions(["updateEntry", "viewEntry"]),
    async submit() {
      try {
        let entry = {
          id: this.id,
          form: this.form,
        };
        await this.updateEntry(entry);
        this.$router.push({ name: "Entry", params: { id: this.entry.id } });
      } catch (error) {
        console.log(error);
      }
    },
    async GetEntry() {
      try {
        await this.viewEntry(this.id);
        this.form.setup = this.entry.setup;
        this.form.order = this.entry.order;
        this.form.result = this.entry.result;
        this.form.obs = this.entry.obs;
      } catch (error) {
        console.error(error);
        this.$router.push("/journal");
      }
    },
  },
};
</script>
