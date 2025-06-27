import React, { useState } from 'react';
import { generateTagCloud } from '../../Api/api';
import { toast } from 'react-toastify';
import { TailSpin } from 'react-loader-spinner';
import 'react-toastify/dist/ReactToastify.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import './GenerateTagCloud.css';

const GenerateTagCloud = () => {
    const [text, setText] = useState('');
    const [maxWords, setMaxWords] = useState(100);
    const [numbers, setNumbers] = useState('');
    const [caps, setCaps] = useState('lowercase');
    const [hashtags, setHashtags] = useState('noapply');
    const [urls, setUrls] = useState('noapply');
    const [mentions, setMentions] = useState('noapply');
    const [stopwordsL, setStopwordsL] = useState('english');
    const [lemmatize, setLemmatize] = useState(true);
    const [punctuation, setPunctuation] = useState(true);
    const [isLoading, setIsLoading] = useState(false);
    const [imageBlob, setImageBlob] = useState(null);
    const [imageUrl, setImageUrl] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const params = {
                max_words: maxWords,
                numbers,
                caps,
                hashtags,
                urls,
                mentions,
                stopwords_l: stopwordsL,
                lemmatize,
                stemming: false,
                punctuation,
                tags: false
            };
            const blob = await generateTagCloud(text, params);
            const url = URL.createObjectURL(blob);
            setImageBlob(blob);
            setImageUrl(url);
            toast.success('Tag cloud generated successfully');
        } catch (error) {
            console.error('Failed to create tag cloud:', error);
            toast.error('Error creating tag cloud');
        } finally {
            setIsLoading(false);
        }
    };

    const handleDownload = () => {
        if (imageBlob) {
            const url = URL.createObjectURL(imageBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'tag_cloud.png';
            a.click();
            URL.revokeObjectURL(url);
        } else {
            toast.error('No tag cloud available to download');
        }
    };

    return (
        <div className="container">
            <h1 className="my-4">Generate Tag Cloud</h1>
            {isLoading && (
                <div className="loading-overlay">
                    <TailSpin color="#00BFFF" height={100} width={100} />
                </div>
            )}
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="text" className="form-label">Text</label>
                    <textarea
                        id="text"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        className="form-control"
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="maxWords" className="form-label">Max Words</label>
                    <p className="field-description">Número máximo de palabras a incluir en la nube de palabras (1-100).</p>
                    <input
                        type="number"
                        id="maxWords"
                        value={maxWords}
                        onChange={(e) => setMaxWords(e.target.value)}
                        className="form-control"
                        min="1"
                        max="100"
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="numbers" className="form-label">Numbers</label>
                    <p className="field-description">Determina si se eliminan o reemplazan los números en el texto. (noapply: se dejan igual, campo vacío: se eliminan, otro texto: se reemplazan por ese texto)</p>
                    <input
                        type="text"
                        id="numbers"
                        value={numbers}
                        onChange={(e) => setNumbers(e.target.value)}
                        className="form-control"
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="caps" className="form-label">Caps</label>
                    <p className="field-description">Determina si se convierte el texto a minúsculas o mayúsculas.</p>
                    <select
                        id="caps"
                        value={caps}
                        onChange={(e) => setCaps(e.target.value)}
                        className="form-select"
                    >
                        <option value="lowercase">Lowercase</option>
                        <option value="uppercase">Uppercase</option>
                        <option value="">No Change</option>
                    </select>
                </div>
                <div className="mb-3">
                    <label htmlFor="hashtags" className="form-label">Hashtags</label>
                    <p className="field-description">Determina si se eliminan o reemplazan los hashtags del texto. (noapply: se dejan igual, campo vacío: se eliminan, otro texto: se reemplazan por ese texto)</p>
                    <input
                        type="text"
                        id="hashtags"
                        value={hashtags}
                        onChange={(e) => setHashtags(e.target.value)}
                        className="form-control"
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="urls" className="form-label">URLs</label>
                    <p className="field-description">Determina si se eliminan o reemplazan las URLs del texto. (noapply: se dejan igual, campo vacío: se eliminan, otro texto: se reemplazan por ese texto)</p>
                    <input
                        type="text"
                        id="urls"
                        value={urls}
                        onChange={(e) => setUrls(e.target.value)}
                        className="form-control"
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="mentions" className="form-label">Mentions</label>
                    <p className="field-description">Determina si se eliminan o reemplazan las menciones del texto. (noapply: se dejan igual, campo vacío: se eliminan, otro texto: se reemplazan por ese texto)</p>
                    <input
                        type="text"
                        id="mentions"
                        value={mentions}
                        onChange={(e) => setMentions(e.target.value)}
                        className="form-control"
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="stopwordsL" className="form-label">Stopwords</label>
                    <p className="field-description">Determina el conjunto de palabras vacías a usar (ej. 'english').</p>
                    <input
                        type="text"
                        id="stopwordsL"
                        value={stopwordsL}
                        onChange={(e) => setStopwordsL(e.target.value)}
                        className="form-control"
                    />
                </div>
                <div className="mb-3 form-check">
                    <input
                        type="checkbox"
                        id="lemmatize"
                        checked={lemmatize}
                        onChange={(e) => setLemmatize(e.target.checked)}
                        className="form-check-input"
                    />
                    <label htmlFor="lemmatize" className="form-check-label">Lemmatize</label>
                    <p className="field-description">Determina si se lematiza el texto.</p>
                </div>
                <div className="mb-3 form-check">
                    <input
                        type="checkbox"
                        id="punctuation"
                        checked={punctuation}
                        onChange={(e) => setPunctuation(e.target.checked)}
                        className="form-check-input"
                    />
                    <label htmlFor="punctuation" className="form-check-label">Punctuation</label>
                    <p className="field-description">Determina si se eliminan todas las marcas de puntuación del texto.</p>
                </div>
                <button type="submit" className="btn btn-primary button-primary">Visualize Tag Cloud</button>
                <button type="button" className="btn btn-secondary" onClick={handleDownload}>Download Tag Cloud</button>
            </form>
            {imageUrl && (
                <div className="mt-4">
                    <h3>Generated Tag Cloud</h3>
                    <img src={imageUrl} alt="Tag Cloud" className="img-fluid" />
                </div>
            )}
        </div>
    );
};

export default GenerateTagCloud;
