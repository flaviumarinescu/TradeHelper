import createPersistedState from "vuex-persistedstate";
import Vue from "vue";
import Vuex from "vuex";

import notes from "./modules/notes";
import entries from "./modules/entries";
import users from "./modules/users";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        notes,
        entries,
        users,
    },
    plugins: [createPersistedState()],
});
