import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Input from './components/Input';
import IngredientList from './components/IngredientList';
import SlideView from './components/SlideView';
import './index.css';

const API_BASE = 'http://localhost:8000/api';

function App() {
  const [status, setStatus] = useState('input'); // input, processing, result, error
  const [jobId, setJobId] = useState(null);
  const [progress, setProgress] = useState('');
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState('ingredients');

  const handleGenerate = async (url) => {
    try {
      setStatus('processing');
      setProgress('Starting...');
      const res = await axios.post(`${API_BASE}/generate`, { url });
      setJobId(res.data.job_id);
    } catch (err) {
      console.error(err);
      setStatus('error');
    }
  };

  useEffect(() => {
    let interval;
    if (status === 'processing' && jobId) {
      interval = setInterval(async () => {
        try {
          const res = await axios.get(`${API_BASE}/status/${jobId}`);
          setProgress(res.data.progress);
          if (res.data.status === 'completed') {
            setResult(res.data.result);
            setStatus('result');
            clearInterval(interval);
          } else if (res.data.status === 'failed') {
            setStatus('error');
            clearInterval(interval);
          }
        } catch (err) {
          console.error(err);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [status, jobId]);

  // Wake Lock
  useEffect(() => {
    let wakeLock = null;
    const requestWakeLock = async () => {
      try {
        if ('wakeLock' in navigator) {
          wakeLock = await navigator.wakeLock.request('screen');
          console.log('Wake Lock active');
        }
      } catch (err) {
        console.error(`${err.name}, ${err.message}`);
      }
    };

    if (status === 'result') {
      requestWakeLock();
    }

    return () => {
      if (wakeLock) wakeLock.release();
    };
  }, [status]);

  if (status === 'input') {
    return <Input onGenerate={handleGenerate} isLoading={false} />;
  }

  if (status === 'processing') {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>{progress}</p>
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div className="error-screen">
        <p>エラーが発生しました。</p>
        <button onClick={() => setStatus('input')}>戻る</button>
      </div>
    );
  }

  return (
    <div className="app-container">
      <div className="tabs">
        <button className={activeTab === 'ingredients' ? 'active' : ''} onClick={() => setActiveTab('ingredients')}>材料</button>
        <button className={activeTab === 'summary' ? 'active' : ''} onClick={() => setActiveTab('summary')}>サマリー</button>
        <button className={activeTab === 'slides' ? 'active' : ''} onClick={() => setActiveTab('slides')}>手順</button>
      </div>

      <div className="content-area">
        {activeTab === 'ingredients' && <IngredientList ingredients={result.ingredients} />}
        {activeTab === 'summary' && (
          <div className="summary-list">
            <ul>
              {result.summary.map((line, i) => <li key={i}>{line}</li>)}
            </ul>
          </div>
        )}
        {activeTab === 'slides' && <SlideView steps={result.steps} />}
      </div>
    </div>
  );
}

export default App;
