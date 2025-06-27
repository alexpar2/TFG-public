import React, { useState, useEffect } from 'react';
import { getAllGoogleNews, createTagCloud } from './googleApi';
import api, {  generateTagCloud } from '../../Api/api';
import { toast } from 'react-toastify';
import { TailSpin } from 'react-loader-spinner';
import { useNavigate } from 'react-router-dom';
import 'react-toastify/dist/ReactToastify.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import './VerTodosLosDatos.css';


const VerTodosLosDatos = () => {
    const [googleData, setGoogleData] = useState([]);
    const [dataLoaded, setDataLoaded] = useState(false);
    const [titleFilter, setTitleFilter] = useState('');
    const [contentFilter, setContentFilter] = useState('');
    const [mediaNameFilter, setMediaNameFilter] = useState('');
    const [mediaNames, setMediaNames] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const fetchData = async () => {
        setIsLoading(true);
        try {
            const data = await getAllGoogleNews();
            console.log(googleData)
            setGoogleData(data);
            setMediaNames([...new Set(data.map(post => post.MediaName))]);
            setDataLoaded(true);
            toast.success('Google data loaded successfully');
        } catch (error) {
            console.error('Failed to fetch Google data:', error);
            toast.error('Error fetching Google data');
        } finally {
            setIsLoading(false);
        }
    };

    const handleTitleFilterChange = (event) => {
        setTitleFilter(event.target.value);
    };

    const handleContentFilterChange = (event) => {
        setContentFilter(event.target.value);
    };

    const handleMediaNameFilterChange = (event) => {
        setMediaNameFilter(event.target.value);
    };

    const handleAnalyze = async () => {
    try {
        const paragraphs = filteredData.map(post => post.Title) ;
        console.log(paragraphs);

        const response = await api.post('/analysis/api/analyze', paragraphs, {
            headers: { 'Content-Type': 'application/json'}});
        
        console.log("Respuesta recibida:", response.data);
        navigate('/search-results', { state: { results: response.data } });
    } catch (error) {
        console.error('Failed to analyze text:', error);
        toast.error('Error analyzing text');
    }
};

    const handleCreateTagCloud = async () => {
        try {
            console.log(filteredData)
            const text = filteredData.map(post => post.Title).join(' '); // ver como traer data de  gnews
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
                tags: true
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
        }
    };

    const handleCopyToClipboard = () => {
        try {
            const text = filteredData.map(post => post.content).join(' ');
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

    const filteredData = googleData.filter(post => 
        (titleFilter === '' || post.Title.toLowerCase().includes(titleFilter.toLowerCase())) &&
        (contentFilter === '' || post.content.toLowerCase().includes(contentFilter.toLowerCase())) &&
        (mediaNameFilter === '' || post.MediaName === mediaNameFilter)
    );

    return (
        <div className="container">
            <h1 className="my-4">Google Posts</h1>
            {!dataLoaded ? (
                <button className="btn btn-primary button-primary" onClick={fetchData}>
                    Load Google Data
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
                            placeholder="Filter by title" 
                            value={titleFilter} 
                            onChange={handleTitleFilterChange} 
                            className="form-control mb-2"
                        />
                        <input 
                            type="text" 
                            placeholder="Filter by content" 
                            value={contentFilter} 
                            onChange={handleContentFilterChange} 
                            className="form-control mb-2"
                        />
                        <select 
                            value={mediaNameFilter} 
                            onChange={handleMediaNameFilterChange} 
                            className="form-select mb-2"
                        >
                            <option value="">All Media Names</option>
                            {mediaNames.map((name, index) => (
                                <option key={index} value={name}>{name}</option>
                            ))}
                        </select>
                        <div className="d-flex mb-2">
                            <button className="btn btn-secondary me-2" onClick={handleCreateTagCloud}>Create Tag Cloud</button>
                            <button className="btn btn-secondary me-2" onClick={handleCopyToClipboard}>Copy to Clipboard</button>
                            <button className="btn btn-secondary me-2" onClick={handleDownloadJSON}>Download JSON</button>
                            <button className="btn btn-secondary" onClick={handleAnalyze}>Analyze</button>
                        </div>
                    </div>
                    {filteredData.length === 0 ? (
                        <p>No data available</p>
                    ) : (
                        filteredData.map(post => (
                            <div key={post._id} className="card mb-4">
                                <div className="card-body">
                                    <h2 className="card-title">{post.Title}</h2>
                                    <p className="card-text">Media Name: {post.MediaName}</p>
                                    <p className="card-text">{post.content}</p>
                                    {post.url && (
                                        <p className="card-text">
                                            <a href={post.url} target="_blank" rel="noopener noreferrer">Link</a>
                                        </p>
                                    )}
                                </div>
                            </div>
                        ))
                    )}
                </>
            )}
        </div>
    );
};

export default VerTodosLosDatos;