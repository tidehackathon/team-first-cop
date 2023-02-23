<template>
    <div class="list row">
      <div class="col-md-12 search-header">
        <div class="input-group mb-3">
          <input type="text" class="form-control search-input" placeholder="Search by words"
            v-model="title"/>
          <div class="input-group-append">
            <button class="btn btn-outline-secondary search-btn" type="submit"
              @click="searchTitle"
            >
              Search
            </button>
          </div>
        </div>

        <div class="filters">
          <div class="ranges">
            <b-form-input id="similarity-range" v-model="value" type="range" min="0.25" max="1" step="0.25"></b-form-input>
            <div class="mt-2 info">Value: {{ value }} ({{ similarityType(value) }})</div>
          </div>
        </div>
      </div>

      <div class="col-md-8 result-list">
        <h5>Result List:</h5>
        <ul class="list-group-msg">
          <li class="list-group-item"
            :class="{ active: index == currentIndex }"
            v-for="(message, index) in messages"
            :key="index"
            @click="setActiveTutorial(message, index)"
          >
            <span class="date">{{message.date}}</span>
            <span class="text">{{ message.message_text }}</span>
          </li>
        </ul>
        <nav v-if="totalRows" aria-label="Message navigation">
          <ul class="pagination">
            <b-pagination
              name="pag"
              :total-rows="totalRows"
              v-model="currentPage"
              :per-page="perPage"
              v-on:page-click="clickPage"
            />
          </ul>
        </nav>
      </div>
      <div class="col-md-4 details">
        <div v-if="currentMessage">
          <h5>Message Details</h5>
          <div class="msg-details">
            <div>
              <label><strong>Text:</strong></label> {{ currentMessage?.message_text }}
            </div>
            <div>
              <label><strong>User id:</strong></label> {{ currentMessage?.user_id }}
            </div>
            <div>
              <label><strong>Date:</strong></label> {{ currentMessage?.date }}
            </div>
            <div>
              <label><strong>Location:</strong></label> {{ currentMessage?.location }}
            </div>
            <div>
              <label><strong>Likes:</strong></label> {{ currentMessage?.likes }}
            </div>
          </div>
        </div>
        <div v-else>
          <br />
          <p>Please click on a Message...</p>
        </div>
      </div>

    </div>
  </template>

  <script>
  import MessageDataService from '../services/MessageDataService';
  import { BPagination, BFormInput } from 'bootstrap-vue'
  import Vue from 'vue';
  import VueDatepickerUi from 'vue-datepicker-ui';

  Vue.component('Datepicker-range', VueDatepickerUi)
  export default {
    components: { BPagination, BFormInput },
    name: "similarity-list",
    data() {
      return {
        messages: [],
        currentMessage: null,
        currentIndex: -1,
        title: "",
        currentPage: 1,
        perPage: 20,
        meta: null,
        value: 0.25,
        selectedDate: [
          new Date(),
          new Date(new Date().getTime() + 9 * 24 * 60 * 60 * 1000)
        ]
      };
    },
    computed: {
      totalRows () {
        const pages = this.meta && this.meta['pages'];
        return this.messages.length * (pages || 1)
      }
    },
    methods: {
      scrollToTop() {
        window.scrollTo(0,0);
      },

      similarityType(value) {
        console.log('v', value)
        switch (value.toString()) {
          case '0.25':
            return 'Low';
          case '0.5':
            return 'Medium';
          case '0.75':
            return 'High';
          default:
            return 'Identical';
        }
      },

      getMessages(text) {
      console.log('text', text)

      MessageDataService.search()
        .then(response => {

          response.data.map((r) => {
            this.messages.push({
              channel: r[0].tweet.channel,
              date: r[0].tweet.date,
              message_text: r[0].tweet.message_text,
              user_id: r[0].tweet.user_id,
              likes: r[0].tweet.likes,
              location: r[0].tweet.location
            })
          });
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        });
      },

      refreshList() {
        this.getMessages();
        this.currentMessage = null;
        this.currentIndex = -1;
      },

      setActiveTutorial(message, index) {
        this.currentMessage = message;
        this.currentIndex = index;
      },

      clickPage(event, page) {
        console.log('page', page);
        this.currentPage = page;
        this.searchTitle();
        this.scrollToTop();
      },

      transformDate(d) {
        if (!d[0]) return [];

        return d.map((fd) => {
          const date = new Date(fd).toLocaleDateString("en-US")
          console.log('ddd', date)
          const temp = date.split('/');
          return `${temp[2]}.${temp[1]}.${temp[0]}`;
        });
      },

      searchTitle() {
        console.log('datae', this.transformDate(this.selectedDate))
        const body = {
          string: this.title,
          page: this.currentPage,
          time: this.transformDate(this.selectedDate)
        };

        console.log('asd', this.selectedDate);

        MessageDataService.search(body)
          .then(response => {
            console.log('response.data', response.data)
            this.messages = [];
            response.data.response.map((r) => {
              this.meta = response.data.meta;
              this.messages.push({
                channel: r.tweet.channel,
                date: new Date(r.tweet.date).toLocaleDateString("en-US"),
                message_text: r.tweet.message_text,
                user_id: r.tweet.user_id,
                likes: r.tweet.likes,
                location: r.tweet.location
              })
            });
            console.log(response.data);
          })
          .catch(e => {
            console.log(e);
          });
      }
    },
    mounted() {
      // this.getMessages();
    }
  };
  </script>

  <style>
    .list {
      width: 60rem;
      min-height: 20rem;
      max-height: 43rem;
      border-radius: 16px;
      background: #75c9cf;
      display: flex;
      margin: 5rem auto;
      color: #fff;
    }

    .input-group {
      margin: 1.2rem 0;
    }

    .search-input {
      border-radius: 8px;
    }

    .search-btn {
      background: #ffc832;
      color: #302f03;
      border: none;
      -webkit-border-top-right-radius: 8px;
      -webkit-border-bottom-right-radius: 8px;
      -moz-border-radius-topright: 8px;
      -moz-border-radius-bottomright: 8px;
      border-top-right-radius: 8px;
      border-bottom-right-radius: 8px;
      outline: none;
    }

    .search-btn:focus, .search-btn:active {
      background: #deaf30 !important;
      outline: none !important;
    }

    .search-btn:hover {
      background: #deaf30;
    }

    .search-header {
      width: 100%;
      height: 8rem;
      border-radius: 16px;
      background: #2faeb8;
    }

    .filters {
      display: flex;
      justify-content: space-between;
    }

    .ranges {
      width: 350px;
    }

    .ranges .info {
      margin-top: -5px;
      font-size: 12px;
    }

    .list-group-msg {
      padding: 0;
    }

    .list-group-item {
      height: 3rem;
      flex-direction: row;
      display: flex;
      border: 1px solid #268d94;
      cursor: pointer;
      color: #302f03;
    }

    .list-group-item .date {
      display: flex;
      font-size: 12px;
      align-items: center;
      margin-right: 1rem;
    }

    .msg-details {
      color: #302f03;
    }

    .list-group-item .text {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .list-group-item.active {
      background-color: #ffc832;
      border-color: #ffc832;
      color: #302f03;
    }

    .result-list {
      margin-top: 1rem;
      min-height: 20rem;
      max-height: 34rem;
      overflow-y: scroll;
    }

    .v-calendar input {
      height: 40px !important;
    }

    .v-calendar .input-field svg.datepicker {
      fill: #ffc832;
    }

    .v-calendar .calendar .days .day.selectedDate .number {
      background: #ffc832;
    }

    .v-calendar .calendar .days .day.selectedRange {
      background: #fff8df;
    }

    .v-calendar .calendar .days .day.disabledDate.selectedRange {
      background: #fff7ee;
    }

    .pagination {
      margin: 1rem auto;
    }

    .page-item.active .page-link {
      border-color: #ffc832 !important;
      background-color: #ffc832 !important;
    }

    .pagination .page-link {
      color: #302f03;
    }

    .details {
      margin-top: 1rem;
    }
  </style>