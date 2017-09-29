import Auth from '../../common/Auth';

export const CHANGE_LOADEDALL_STATUS = 'CHANGE_LOADEDALL_STATUS';
export const ADD_NEWS_TO_LIST = 'ADD_NEWS_TO_LIST';

export function loadMoreNews(news, pageNum, loadedAll) {
	const thunk = (dispatch) => {

		if (loadedAll === true) {
	      return
	    }

	    let url = 'http://18.221.76.85:3000/news/userId/' + Auth.getEmail()
	              + '/pageNum/' + pageNum

	    let request = new Request(encodeURI(url), {
	      method: 'GET',
	      headers: {
	        'Authorization': 'bearer ' + Auth.getToken(),
	      },
	      cache: false
	    });

	    fetch(request)
	    .then((res) => res.json())
	    .then((news_from_res) => {
		      if (!news_from_res || news_from_res.length === 0) {
		      	dispatch(changeLoadedAllStatus);
		      }
		      console.log(news_from_res);
		      dispatch(addNewsToList(news_from_res, pageNum));
	    });
	}
	
	thunk.meta = {
    	debounce: {
      		time: 1000,
      		key: 'LOAD_MORE_NEWS'
		}
	}
	
	return thunk;
}

function changeLoadedAllStatus () {
	return {
		type: CHANGE_LOADEDALL_STATUS		
	}
}

function addNewsToList(news_from_res, pageNum) {
	return {
		type: ADD_NEWS_TO_LIST,
		new_news: news_from_res,
		curr_pageNum: pageNum
	}
}
