<template>
  <div class="channel-list row">
    <div class="col-md-6">
      <h4>Channels List</h4>
      <ul class="list-group">
        <li class="list-group-item"
            :class="{ active: index == currentIndex }"
            v-for="(channel, index) in channels"
            :key="index"
        >
          {{ channel.url }}

          <div class="close" @click="remove(channel.url)">x</div>
        </li>
      </ul>
    </div>

    <div class="col-md-6">
      <div class="submit-form">
        <div v-if="!submitted">
          <div class="form-group">
            <label for="title">Twitter channel url</label>
            <input
              type="text"
              class="form-control add-input"
              id="title"
              required
              v-model="channel.url"
              name="title"
            />
          </div>

          <button @click="addChannel" class="btn btn-success">Submit</button>
        </div>

        <div v-else>
          <h4>You submitted successfully!</h4>
          <button class="btn btn-success" @click="newChannel">Add</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import ChannelDataService from '../services/ChannelDataService';

  export default {
    name: 'add-channel',
    data() {
      return {
        channel: {
          id: null,
          url: '',
        },
        channels: [],
        currentIndex: -1,
        submitted: false
      };
    },
    methods: {
      getChannels() {
        ChannelDataService.getAll()
          .then(response => {
            this.channels = response.data?.sources_list;
            console.log(this.channels);
          })
          .catch(e => {
            console.log(e);
          });
      },

      addChannel() {
        var data = {
          url: this.channel.url
        };

        this.channels.push(data);

        ChannelDataService.create(data)
          .then(response => {
            this.channel.id = response.data.id;
            this.channels.unshift(data);

            console.log(response.data);
            this.submitted = true;
          })
          .catch(e => {
            console.log(e);
          });
      },

      remove(url) {
        ChannelDataService.delete(url)
          .then(response => {
            this.channels = this.channels.filter((c => c.url !== url ));
            console.log(response.data);
          })
          .catch(e => {
            console.log(e);
          });
      },

      newChannel() {
        this.submitted = false;
        this.channel = {};
      }
    },
    mounted() {
      this.getChannels();
    }
  };
</script>

<style>
  .submit-form {
    max-width: 300px;
    margin: auto;
  }

  .channel-list {
    width: 60rem;
    min-height: 20rem;
    max-height: 40rem;
    border-radius: 16px;
    background: #75c9cf;
    padding: 2rem;
    display: flex;
    margin: 5rem auto;
    color: #fff;
  }

  .btn-success {
    background: #ffc832;
    border-radius: 8px;
    border: none;
    box-shadow: none !important;
  }

  .btn-success:focus, .btn-success:active {
    background: #deaf30 !important;
    box-shadow: none !important;
  }

  .btn-success:hover {
    background: #deaf30;
    border: none;
  }

  .add-input {
    border-radius: 8px !important;
  }

  .close {
    width: 20px;
    height: 20px;
    font-size: 12px;
    text-align: center;
    padding-top: 3px;
    margin-top: 2px;
    color: #fff;
    background: #6ac7cd;
    border-radius: 14px;
  }

  .list-group {
    min-height: 20rem;
    max-height: 34rem;
    overflow-y: scroll;
  }

  .list-group-item {
    color: #302f03;
    margin-bottom: .5rem;
    justify-content: space-between;
    border-radius: 8px !important;
  }
</style>