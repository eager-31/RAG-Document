export default function AnswerPanel({ result }) {
  if (!result) return null;

  return (
    <div className="p-6 bg-blue-50 rounded-lg border border-blue-100 mt-4 shadow-sm">
      <h2 className="text-xl font-bold mb-4 text-blue-900">Answer</h2>
      
      <div className="prose max-w-none text-gray-800 whitespace-pre-wrap">
        {result.answer}
      </div>

      {result.citations && result.citations.length > 0 && (
        <div className="mt-6 pt-4 border-t border-blue-200">
          <h3 className="text-sm font-semibold text-gray-600 mb-2 uppercase tracking-wide">Citations</h3>
          <div className="flex flex-wrap gap-2">
            {result.citations.map((cite, idx) => (
              <span 
                key={idx}
                className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
              >
                📄 {cite.file} (Page {cite.page})
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
