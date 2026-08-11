import { useState } from 'react';
import UploadBox from './components/UploadBox';
import QueryBox from './components/QueryBox';
import AnswerPanel from './components/AnswerPanel';
import HistorySidebar from './components/HistorySidebar';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleHistorySelect = (historyItem) => {
    // Reconstruct result format expected by AnswerPanel
    setResult({
      answer: historyItem.answer,
      citations: historyItem.chunks_used?.map(chunk => ({
        file: chunk.metadata?.source_file || 'unknown',
        page: chunk.metadata?.page || 'unknown'
      })) || []
    });
  };

  return (
    <div className="flex h-screen bg-gray-100 font-sans">
      <HistorySidebar onSelectHistory={handleHistorySelect} />
      
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <header className="mb-8">
            <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">
              📄 RAG Document Q&A
            </h1>
            <p className="mt-2 text-sm text-gray-500">
              Upload PDF documents and ask questions. The system will retrieve relevant context and provide a cited answer.
            </p>
          </header>

          <div className="space-y-6">
            <UploadBox />
            
            <QueryBox 
              onQueryResult={setResult} 
              loading={loading} 
              setLoading={setLoading} 
            />
            
            <AnswerPanel result={result} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
