import { useState, useEffect } from 'react';
import apiClient from '../api/client';

export default function HistorySidebar({ onSelectHistory }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    try {
      const response = await apiClient.get('/history');
      setHistory(response.data);
    } catch (err) {
      console.error('Failed to fetch history', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="w-64 bg-gray-50 border-r border-gray-200 h-screen overflow-y-auto flex flex-col hidden md:flex">
      <div className="p-4 border-b border-gray-200 bg-white sticky top-0 z-10 flex justify-between items-center">
        <h2 className="font-bold text-gray-800">Recent Queries</h2>
        <button 
          onClick={fetchHistory}
          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          Refresh
        </button>
      </div>
      
      <div className="p-2 flex-1">
        {loading ? (
          <p className="text-sm text-gray-500 text-center mt-4">Loading...</p>
        ) : history.length === 0 ? (
          <p className="text-sm text-gray-500 text-center mt-4">No history yet.</p>
        ) : (
          <ul className="space-y-2">
            {history.map((item) => (
              <li key={item.id}>
                <button
                  onClick={() => onSelectHistory(item)}
                  className="w-full text-left p-3 rounded-md hover:bg-gray-100 transition-colors group"
                >
                  <p className="text-sm font-medium text-gray-800 line-clamp-2 group-hover:text-blue-600">
                    {item.question}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(item.timestamp).toLocaleDateString()}
                  </p>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
