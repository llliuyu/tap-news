import { CHANGE_LOADEDALL_STATUS, ADD_NEWS_TO_LIST} from '../../actions/news_actions/news_actions';

const initialState = {
	news: null,
	pageNum: 1,
	loadedAll: false
}

export default (state = initialState, action) => {
	switch(action.type) {
		case CHANGE_LOADEDALL_STATUS:
			return Object.assign({}, state, {
                      loadedAll: true
                  }); 
		case ADD_NEWS_TO_LIST:
			console.log(action.curr_pageNum);
			return Object.assign({}, state, {
				news: state.news ? state.news.concat(action.new_news) : action.new_news,
				pageNum: action.curr_pageNum + 1
			});
		default:
			return state;                		
	}
}