import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: '/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96',
      alias: ["/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96"],
      redirect: '/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96/search'
    },
    {
      path: "/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96/search",
      alias: ["/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96/search", "/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96/messages"],
      name: "messages",
      component: () => import("./components/MessagesList")
    },
    {
      path: "/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96/similarity",
      alias: ["/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96/similarity"],
      name: "similarity",
      component: () => import("./components/SimilarityList")
    },
    {
      path: "/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96/add",
      alias: ["/e94a2b9a5eaed1b1b46b2eecc8310b61cc7b6c96/add"],
      name: "add",
      component: () => import("./components/AddChannel")
    }
  ]
});
