import { useState } from 'react';
import apiClient from '../api/client';

export default function QueryBox({ onQueryResult, loading, setLoading }) {
  const [query, setQuery] = useState('');
  const [error, setError] = useState('');

  const handleQuery = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');

    try {
      const response = await apiClient.post('/query', { question: query });
      onQueryResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error processing query.');
      onQueryResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-sm border border-gray-200 mt-4">
      <h2 className="text-lg font-semibold mb-4 text-gray-800">2. Ask a Question</h2>
      <form onSubmit={handleQuery} className="flex flex-col gap-3">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about your uploaded documents..."
          className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 min-h-[100px] text-gray-700"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-medium py-2 px-6 rounded-md transition-colors self-end"
        >
          {loading ? 'Thinking...' : 'Ask'}
        </button>
        {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
      </form>
    </div>
  );
}
