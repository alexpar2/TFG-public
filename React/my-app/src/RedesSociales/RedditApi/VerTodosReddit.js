import React, { useState, useEffect } from 'react';
import { getAllRedditData } from './redditApi';
import { toast } from 'react-toastify';
import api, { generateTagCloud } from '../../Api/api';
import { TailSpin } from 'react-loader-spinner';
import { useNavigate } from 'react-router-dom';
import 'react-toastify/dist/ReactToastify.css';
import 'bootstrap/dist/css/bootstrap.min.css';


const VerTodosReddit = () => {
    const [redditData, setRedditData] = useState([]);
    const [dataLoaded, setDataLoaded] = useState(false);
    const [filter, setFilter] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const fetchData = async () => {
        setIsLoading(true);
        try {
            const data = await getAllRedditData();
            if (!data) {
                throw new Error('No data received');
            }

            const initializeComments = (comments) => {
                return comments.map(comment => ({
                    ...comment,
                    expanded: false,
                    Replies: comment.Replies ? initializeComments(comment.Replies) : []
                }));
            };

            const initializedData = data.map(post => ({
                ...post,
                Comments: initializeComments(post.Comments || [])
            }));

            setRedditData(initializedData);
            setDataLoaded(true);
            toast.success('Reddit data loaded successfully');
        } catch (error) {
            console.error('Failed to fetch Reddit data:', error);
            toast.error('Error fetching Reddit data');
        } finally {
            setIsLoading(false);
        }
    };

    const toggleComments = (comment) => {
        comment.expanded = !comment.expanded;
        setRedditData([...redditData]);
    };

    const renderComments = (comments) => {
        return comments.map((comment, index) => (
            <div key={index} style={{ marginLeft: '20px', marginBottom: '10px', borderLeft: '1px solid #ccc', paddingLeft: '10px' }}>
                <p><strong>{comment.Author}</strong></p>
                <p>{comment.Body}</p>
                {comment.Replies && comment.Replies.length > 0 && (
                    <div>
                        <button onClick={() => toggleComments(comment)}>
                            {comment.expanded ? 'Hide Replies' : 'Show Replies'}
                        </button>
                        {comment.expanded && renderComments(comment.Replies)}
                    </div>
                )}
            </div>
        ));
    };

    const handleFilterChange = (event) => {
        setFilter(event.target.value);
    };

    const handleAnalyze = async () => {
        try {
            const paragraphs = filteredData
            .flatMap(post => 
                post.Comments
                    .map(comment => comment.Body)
                    .filter(text => text.trim().length > 0) // Filtrar vacíos
            );
            console.log(paragraphs);
    
            const response = await api.post('/analysis/api/analyze', paragraphs);
            
            console.log("Respuesta recibida:", response.data);
            navigate('/search-results', { state: { results: response.data } });
        } catch (error) {
            console.error('Failed to analyze text:', error);
            toast.error('Error analyzing text');
        }
    };

    const handleCreateTagCloud = async () => {
        setIsLoading(true);
        try {
            const text = filteredData.map(post => post.Comments.map(comment => comment.Body).join(' ')).join(' ');
            console.log('Text for tag cloud:', text); // Mensaje de depuración
            const params = {
                max_words: 100,
                numbers: '',
                caps: 'lowercase',
                hashtags: 'noapply',
                urls: 'noapply',
                mentions: 'noapply',
                stopwords_l: 'english',
                lemmatize: true,
                stemming: false,
                punctuation: true,
                tags: false
            };
            const blob = await generateTagCloud(text, params);
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'tag_cloud.png';
            a.click();
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Failed to create tag cloud:', error);
            toast.error('Error creating tag cloud');
        } finally {
            setIsLoading(false);
        }
    };

    const handleCopyToClipboard = () => {
        try {
            const text = filteredData.map(post => post.Comments.map(comment => comment.Body).join(' ')).join(' ');
            navigator.clipboard.writeText(text);
            toast.success('Text copied to clipboard');
        } catch (error) {
            console.error('Failed to copy text to clipboard:', error);
            toast.error('Error copying text to clipboard');
        }
    };

    const handleDownloadJSON = () => {
        const dataStr = JSON.stringify(filteredData, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'filtered_data.json';
        a.click();
        URL.revokeObjectURL(url);
    };

    const filteredData = redditData.filter(post => 
        post.Title.toLowerCase().includes(filter.toLowerCase()) || 
        post.Author.toLowerCase().includes(filter.toLowerCase())
    );

    return (
        <div className="container">
            <h1 className="my-4">Reddit Posts</h1>
            {!dataLoaded ? (
                <button className="btn btn-primary button-primary" onClick={fetchData}>
                    Load Reddit Data
                </button>
            ) : (
                <>
                    {isLoading && (
                        <div className="loading-overlay">
                            <TailSpin color="#00BFFF" height={100} width={100} />
                        </div>
                    )}
                    <div className="mb-4">
                        <input 
                            type="text" 
                            placeholder="Filter by title or author" 
                            value={filter} 
                            onChange={handleFilterChange} 
                            className="form-control mb-2"
                        />
                        <div className="d-flex mb-2">
                            <button className="btn btn-secondary me-2" onClick={handleCreateTagCloud} disabled={isLoading}>Create Tag Cloud</button>
                            <button className="btn btn-secondary me-2" onClick={handleCopyToClipboard}>Copy to Clipboard</button>
                            <button className="btn btn-secondary me-2" onClick={handleDownloadJSON}>Download JSON</button>
                            <button className="btn btn-secondary" onClick={handleAnalyze}>Analyze</button>
                        </div>
                    </div>
                    {filteredData.length === 0 ? (
                        <p>No data available</p>
                    ) : (
                        filteredData.map(post => (
                            <div key={post._id} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
                                <h2>{post.Title}</h2>
                                <p>Author: {post.Author}</p>
                                <p>Score: {post.Score}</p>
                                <p>Karma: {post.Karma}</p>
                                {post.URL && (
                                    <p>
                                        <a href={post.URL} target="_blank" rel="noopener noreferrer">Link</a>
                                    </p>
                                )}
                                <h3>Comments</h3>
                                {renderComments(post.Comments)}
                            </div>
                        ))
                    )}
                </>
            )}
        </div>
    );
};

export default VerTodosReddit;
