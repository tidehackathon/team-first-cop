import http from '../http-common';

class MessageDataService {
  getAll() {
    return http.get('sources_list/');
  }

  get(id) {
    return http.get(`get_source/${id}`);
  }

  search(body) {
    return http.post(`search/`, body, {withCredentials: true});
  }

  top() {
    return http.get(`top_100/`);
  }
}

export default new MessageDataService();
