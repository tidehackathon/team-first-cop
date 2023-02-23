import http from '../http-common';

class ChannelDataService {
  getAll() {
    return http.get('sources_list/');
  }

  create(data) {
    return http.post('add_source/', data);
  }

  delete(url) {
    return http.post(`delete_source/`, { url });
  }
}

export default new ChannelDataService();