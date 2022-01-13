<template>
  <div>
    <section>
      <h1>Add new entry</h1>
      <hr />
      <br />

      <form @submit.prevent="submit">
        <div class="mb-3">
          <label for="market" class="form-label">Market:</label>
          <input
            type="text"
            name="market"
            v-model="form.market"
            class="form-control"
          />
        </div>
        <div class="mb-3">
          <label for="direction" class="form-label">Direction:</label>
          <textarea
            name="direction"
            v-model="form.direction"
            class="form-control"
          ></textarea>
        </div>
        <div class="mb-3">
          <label for="setup" class="form-label">Setup:</label>
          <textarea
            name="setup"
            v-model="form.setup"
            class="form-control"
          ></textarea>
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

    <br /><br />

    <section>
      <h1>Entries</h1>
      <hr />
      <br />

      <div v-if="entries.length">
        <div v-for="entry in entries" :key="entry.id" class="entries">
          <div class="card" style="width: 18rem">
            <div class="card-body">
              <ul>
                <li><strong>Market:</strong> {{ entry.market }}</li>
                <li><strong>Direction:</strong> {{ entry.direction }}</li>
                <li><strong>Created at:</strong> {{ entry.created_at }}</li>
                <li><strong>Result:</strong> {{ entry.result }}</li>
                <li><strong>Author:</strong> {{ entry.author.username }}</li>
                <li>
                  <router-link :to="{ name: 'Entry', params: { id: entry.id } }"
                    >View</router-link
                  >
                </li>
              </ul>
            </div>
          </div>
          <br />
        </div>
      </div>

      <div v-else>
        <p>Nothing to see. Check back later.</p>
      </div>
    </section>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "Journal",
  data() {
    return {
      form: {
        market: "",
        direction: "",
        setup: "",
        order: "",
        result: "",
        obs: "",
      },
    };
  },
  created: function () {
    return this.$store.dispatch("getEntries");
  },
  computed: {
    ...mapGetters({ entries: "stateEntries" }),
  },
  methods: {
    ...mapActions(["createEntry"]),
    async submit() {
      await this.createEntry(this.form);
    },
  },
};
</script>