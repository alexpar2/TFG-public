import React, { useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import api from '../Api/api';
import 'bootstrap/dist/css/bootstrap.min.css';

function SearchResultsPage() {
  const location = useLocation();
  const { results, query } = location.state || {};
  const [news, setNews] = useState({});
  const [explanations, setExplanations] = useState({});
  const [visibleTopics, setVisibleTopics] = useState({});
  const [loadedTopics, setLoadedTopics] = useState({});
  const [fakeNewsResults, setFakeNewsResults] = useState({});

  if (!results) {
    return (
      <div className="container mt-4">
        <h2>No se encontraron resultados</h2>
        <Link to="/">Volver a la búsqueda</Link>
      </div>
    );
  }

  const { topics, sentiment_counts: sentimentCounts } = results;

  const fetchNews = async (topicIndex) => {
    if (visibleTopics[topicIndex]) {
      setVisibleTopics((prev) => ({ ...prev, [topicIndex]: false }));
      return;
    }
    if (loadedTopics[topicIndex]) {
      setVisibleTopics((prev) => ({ ...prev, [topicIndex]: true }));
      return;
    }
    try {
      const response = await api.get(`/analysis/api/news?n_topic=${topicIndex - 1}`);
      const limitedNews = response.data.slice(0, 10);
      setNews((prevNews) => ({ ...prevNews, [topicIndex]: limitedNews }));

      const explanationResponse = await api.get(`/analysis/api/explanation`);
      setExplanations((prevExplanations) => ({ ...prevExplanations, [topicIndex]: explanationResponse.data }));

      setVisibleTopics((prev) => ({ ...prev, [topicIndex]: true }));
      setLoadedTopics((prev) => ({ ...prev, [topicIndex]: true }));
    } catch (error) {
      console.error("Error fetching news or explanation:", error);
    }
  };

  const toggleFakeNews = async (articleIndex, articleText) => {
    if (fakeNewsResults[articleIndex]) {
      setFakeNewsResults((prev) => ({
        ...prev,
        [articleIndex]: {
          ...prev[articleIndex],
          visible: !prev[articleIndex].visible
        }
      }));
      return;
    }
    try {
      const response = await api.get(`/analysis/api/fakenews`, { params: { text: articleText } });
      const { assessment, verdict, probability } = response.data;
      setFakeNewsResults((prev) => ({
        ...prev,
        [articleIndex]: {
          assessment,
          verdict,
          probability,
          visible: true
        }
      }));
    } catch (error) {
      console.error("Error fetching fake news assessment:", error);
    }
  };

  const getBackgroundColor = (correlation, allCorrelations) => {
    if (!allCorrelations || allCorrelations.length === 0) return "#ffffff";
    const minCorrelation = Math.min(...allCorrelations);
    const maxCorrelation = Math.max(...allCorrelations);

    if (maxCorrelation === minCorrelation) {
      return "rgb(127, 255, 127)";
    }

    const normalized = (correlation - minCorrelation) / (maxCorrelation - minCorrelation);
    const red = Math.round(255 * (1 - normalized));
    const green = 255;
    return `rgb(${red}, ${green}, 0)`;
  };

  const total = sentimentCounts ? sentimentCounts.NEU + sentimentCounts.NEG + sentimentCounts.POS : 0;

  const sentimentData = sentimentCounts ? [
    {
      name: 'Neutral',
      value: total ? parseFloat(((sentimentCounts.NEU / total) * 100).toFixed(2)) : 0,
      color: '#FFD700'
    },
    {
      name: 'Negative',
      value: total ? parseFloat(((sentimentCounts.NEG / total) * 100).toFixed(2)) : 0,
      color: '#FF0000'
    },
    {
      name: 'Positive',
      value: total ? parseFloat(((sentimentCounts.POS / total) * 100).toFixed(2)) : 0,
      color: '#008000'
    },
  ] : [];

  return (
    <div className="container mt-4 text-body">
      <h1 className="text-center display-3 fw-bold my-4">Results for: {query}</h1>
      <h3 className='text-center display-4'>Topics</h3>
      <p className='text-center'>Click on the topic to see related news and explanations.</p>
      {topics && topics.length > 0 ? (
        <ol>
          {topics.map((topic, index) => (
            <li key={index}>
              <button className='btn-primary rounded text-body w-100 m-1 p-1' onClick={() => fetchNews(index)}>
                <h5>{topic.Words}</h5>
              </button>
              {visibleTopics[index] && (
                <>
                  {news[index] && (
                    <>
                      <h4 className='display-5'>Related News</h4>
                      <p>Background color represents more or less relation to the topic. Click on title to navigate to the source.</p>
                      <ul>
                        {news[index].map((article, i, arr) => {
                          const key = `${index}-${i}`;
                          const result = fakeNewsResults[key];
                          return (
                            <li
                              key={i}
                              className="d-flex flex-column align-items-start"
                              style={{
                                backgroundColor: getBackgroundColor(article.Correlation, arr.map(a => a.Correlation)),
                                padding: '5px',
                                borderRadius: '5px',
                                margin: '5px'
                              }}
                            >
                              <div className="d-flex justify-content-between w-100">
                                <a
                                  href={article.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  style={{ textDecoration: 'none', color: 'black', flex: 1 }}
                                >
                                  {article.Title}
                                </a>
                                <button
                                  className='btn btn-primary ms-2'
                                  onClick={() => toggleFakeNews(key, article.Title)}
                                >
                                  Is this fake news?
                                </button>
                              </div>
                              {result?.visible && (
                                <div className='mt-2 p-3 border rounded bg-dark text-white w-100'>
                                  <h5>LLM Assessment</h5>
                                  <p>{result.assessment}</p>
                                  <h5>Trained Model Assessment</h5>
                                  <p>
                                    The trained model assesses that the text is likely <strong>{result.verdict}</strong>
                                     with a <strong>{result.probability.toFixed(2)}%</strong> chance of being fake news.
                                  </p>
                                  <div className="progress">
                                    <div
                                      className={`progress-bar ${result.verdict === 'Fake' ? 'bg-danger' : 'bg-success'}`}
                                      role="progressbar"
                                      style={{ width: `${result.probability.toFixed(2)}%` }}
                                      aria-valuenow={result.probability.toFixed(2)}
                                      aria-valuemin="0"
                                      aria-valuemax="100"
                                    ></div>
                                  </div>
                                </div>
                              )}
                            </li>
                          );
                        })}
                      </ul>
                    </>
                  )}
                  {explanations[index] && (
                    <>
                      <br />
                      <div className="card bg-info mb-3">
                        <div className="card-header">What are these news about?</div>
                        <div className="card-body">
                          <p className="card-text text-white">{explanations[index]}</p>
                        </div>
                      </div>
                    </>
                  )}
                </>
              )}
            </li>
          ))}
        </ol>
      ) : (
        <p>No se encontraron topics.</p>
      )}

      <h3 className='text-center'>Sentiment Analysis</h3>
      {sentimentCounts ? (
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={sentimentData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              stroke="#72ff6b"
              strokeWidth={2}
              outerRadius={100}
              startAngle={-180}
              endAngle={180}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(2)}%`}
            >
              {sentimentData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      ) : (
        <p>No sentiment analysis was found.</p>
      )}
      <Link to="/analysis" className="text-center">Search for another term</Link>
    </div>
  );
}

export default SearchResultsPage;
