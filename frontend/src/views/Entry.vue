<template>
  <div v-if="entry">
    <p><strong>Market:</strong> {{ entry.market }}</p>
    <p><strong>Direction:</strong> {{ entry.direction }}</p>
    <p><strong>Setup:</strong> {{ entry.setup }}</p>
    <p><strong>Order:</strong> {{ entry.order }}</p>
    <p><strong>Result:</strong> {{ entry.result }}</p>
    <p><strong>Observations:</strong> {{ entry.obs }}</p>
    <p><strong>Author:</strong> {{ entry.author.username }}</p>
    <p><strong>Created at:</strong> {{ entry.created_at }}</p>
    <p><strong>Modified at:</strong> {{ entry.modified_at }}</p>

    <div v-if="user.id === entry.author.id">
      <p>
        <router-link
          :to="{ name: 'EditEntry', params: { id: entry.id } }"
          class="btn btn-primary"
          >Edit</router-link
        >
      </p>
      <p>
        <button @click="removeEntry()" class="btn btn-secondary">Delete</button>
      </p>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "Entry",
  props: ["id"],
  async created() {
    try {
      await this.viewEntry(this.id);
    } catch (error) {
      console.error(error);
      this.$router.push("/journal");
    }
  },
  computed: {
    ...mapGetters({ entry: "stateEntry", user: "stateUser" }),
  },
  methods: {
    ...mapActions(["viewEntry", "deleteEntry"]),
    async removeEntry() {
      try {
        await this.deleteEntry(this.id);
        this.$router.push("/journal");
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
