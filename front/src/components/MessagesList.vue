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

        <Datepicker-range
            range
            v-model="selectedDate"
            lang="en"
        />
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
            <div class="indicator" v-bind:class="colorBage(message.label)"></div>
            <span class="date">{{message.date}}</span>
            <span class="text">{{ message.message_text }}</span>
          </li>
        </ul>
        <nav v-if="totalRows && pagination" aria-label="Message navigation">
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
            <div style="display: inline-flex">
              <label style="margin-right: .5rem;"><strong>Tone:</strong></label>
              {{ currentMessage?.label }}
              <div class="indicator-details" v-bind:class="colorBage(currentMessage?.label)"></div>
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
  import { BPagination } from 'bootstrap-vue'
  import Vue from 'vue';
  import VueDatepickerUi from 'vue-datepicker-ui';

  Vue.component('Datepicker-range', VueDatepickerUi)
  export default {
    components: { BPagination },
    name: "messages-list",
    data() {
      return {
        messages: [],
        currentMessage: null,
        currentIndex: -1,
          pagination:false,
        title: "",
        currentPage: 1,
        perPage: 20,
        meta: null,
        selectedDate: [
          new Date(),
          new Date(new Date().getTime() + 9 * 24 * 60 * 60 * 1000)
        ]
      };
    },
    computed: {
      totalRows () {
        const pages = this.meta && this.meta['pages'];
        console.log('pages', pages, this.messages.length)
        return this.messages.length * (pages || 1)
      }
    },
    methods: {
      scrollToTop() {
        window.scrollTo(0,0);
      },

      colorBage(value) {
        switch (value) {
          case 'NEUTRAL':
            return 'gray';
          case 'POSITIVE':
            return 'green';
          case 'NEGATIVE':
            return 'red';
        }
      },


      getMessages(text) {
      console.log('text', text)
        MessageDataService.search()
          .then(response => {
            console.log('response: ', response);
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

        getTop() {
          this.pagination=false;
          this.perPage=100;
            this.currentMessage = null;
            this.currentIndex = -1;
            MessageDataService.top()
                .then(response => {
                    console.log('response: ', response);
                        response.data.response.map((r) => {
                            this.messages.push({
                                channel: r.tweet.channel,
                                date: new Date(r.tweet.date).toLocaleDateString("en-US"),
                                message_text: r.tweet.message_text,
                                user_id: r.tweet.user_id,
                                likes: r.tweet.likes,
                                location: r.tweet.location,
                                label: r.tweet.label
                            })
                    });
                    console.log(response.data);
                })
                .catch(e => {
                    console.log(e);
                });
        },

      setActiveTutorial(message, index) {
        this.currentMessage = message;
        this.currentIndex = index;
      },

      clickPage(event, page) {
        console.log('page', page);
        this.currentPage = page;
        this.searchTitle();
        // this.scrollToTop();
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
          time: this.selectedDate
        };

        console.log('asd', this.selectedDate, body);

        MessageDataService.search(body)
          .then(response => {
            console.log('response.data', response.data, response.data.meta)
            this.messages = [];
            this.meta = response.data.meta;
              this.perPage=20;
              this.pagination=true;
            response.data.response.map((r) => {
              this.messages.push({
                channel: r.tweet.channel,
                date: new Date(r.tweet.date).toLocaleDateString("en-US"),
                message_text: r.tweet.message_text,
                user_id: r.tweet.user_id,
                likes: r.tweet.likes,
                location: r.tweet.location,
                label: r.tweet.label
              })
            });
            console.log('oh', response.data, this.meta);
          })
          .catch(e => {
            console.log(e);
          });
      }
    },
    mounted() {
        this.getTop();
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

    .gray {
      background: #6e6e6e !important;;
    }

    .green {
      background: #00f338 !important;;
    }

    .red {
      background: #b12a2a !important;
    }

    .indicator {
      position: absolute;
      z-index: 999;
      top: 17px;
      left: 4px;
      width: 12px;
      height: 12px;
      background: #000;
      border-radius: 6px;
    }

    .indicator-details {
      width: 22px;
      height: 22px;
      background: #000;
      border-radius: 12px;
      margin-left: .5rem;
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
