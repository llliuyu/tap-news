import './NewsPanel.css';

import React from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { loadMoreNews } from '../../actions/news_actions/news_actions';

import Auth from '../../common/Auth';
//import NewsCard from '../NewsCard/NewsCard';
import _ from 'lodash';

class NewsPanel extends React.Component {
  constructor(props) {
    super(props);
    
    this.handleScroll = this.handleScroll.bind(this);
  }

  componentDidMount() {
    this.props.loadMoreNews(this.props.news, this.props.pageNum, this.props.loadedAll);
    this.props.loadMoreNews = _.debounce(this.props.loadMoreNews, 3000);
    window.addEventListener('scroll', this.handleScroll);
  }

  handleScroll() {
    let scrollY = window.scrollY ||
                  window.pageYOffset ||
                  document.documentElement.scrollTop;
    if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
      console.log('Loading more news');
      this.props.loadMoreNews(this.props.news, this.props.pageNum, this.props.loadedAll);
    }
  }

  redirectToUrl(news_item) {
        this.sendClickLog(news_item);
        window.open(news_item.url, '_blank');
    }

  sendClickLog(news_item) {
      let url = 'http://localhost:3000/news/userId/' + Auth.getEmail()
                  + '/newsId/' + news_item.digest;

      let request = new Request(encodeURI(url), {
          method: 'POST',
          headers: {
              'Authorization': 'bearer ' + Auth.getToken(),
          },
          cache: false});
      
          fetch(request);
  }

  renderNews() {
    console.log(this.props.news);
    return this.props.news.map((news_item) => {
      return(
        <a className='list-group-item' href="#" id='left'>
            <div className="news-container" onClick={(event) => { event.preventDefault(); this.redirectToUrl(news_item);}}>
                <div className='row'>
                    <div className='col s4 fill'>
                        <img src={news_item.urlToImage} alt='news'/>
                    </div>
                    <div className="col s8">
                        <div className="news-intro-col">
                            <div className="news-intro-panel">
                                <h4>{news_item.title}</h4>
                                <div className="news-description">
                                <p>{news_item.description}</p>
                                    <div>
                                        {news_item.source != null && <div className='chip light-blue news-chip'>{news_item.source}</div>}
                                        {news_item.reason != null && <div className='chip light-green news-chip'>{news_item.reason}</div>}
                                        {news_item.time != null && <div className='chip amber news-chip'>{news_item.time}</div>}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </a>

      );
    });

    // return(
    //   <div className='container-fluid'>
    //     <div className='list-group'>
    //       {news_list}
    //     </div>
    //   </div>
    // )
  }

  render() {
    if (this.props.news) {
      return(
        <div>
          {this.renderNews()}
        </div>
      );
    } else {
      return(
        <div>
          <div id='msg-app-loading'>
            Loading...
          </div>
        </div>
      );
    }
  }
}

function mapStateToProps(state) {
  return {
    news: state.NewsReducer.news,
    pageNum: state.NewsReducer.pageNum,
    loadedAll: state.NewsReducer.loadedAll
  }
} 

function mapDispatchToProps(dispatch) {
  return bindActionCreators({ loadMoreNews }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(NewsPanel)