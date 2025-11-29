import React, { useState } from 'react';

export default function Input({ onGenerate, isLoading }) {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url) onGenerate(url);
  };

  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      setUrl(text);
    } catch (err) {
      console.error('Failed to read clipboard', err);
    }
  };

  return (
    <div className="input-container">
      <h1>レシピ動画スライド生成</h1>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="YouTube URLを貼り付け"
            required
            disabled={isLoading}
          />
          <button type="button" onClick={handlePaste} className="paste-btn" disabled={isLoading}>
            📋
          </button>
        </div>
        <button type="submit" className="generate-btn" disabled={isLoading}>
          {isLoading ? '生成中...' : 'レシピを生成'}
        </button>
      </form>
    </div>
  );
}
