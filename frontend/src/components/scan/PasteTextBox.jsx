import React from 'react';
import { AlertCircle } from 'lucide-react';

/**
 * PasteTextBox – reusable component for the Scan page.
 * Props:
 *  - pasteText: string – current textarea value
 *  - setPasteText: (value: string) => void – update handler
 *  - setError: (msg: string) => void – optional error setter from parent
 */
export default function PasteTextBox({ pasteText, setPasteText, setError }) {
  const MAX_CHARS = 25000;
  const MIN_CHARS = 50;

  const handleChange = (e) => {
    const value = e.target.value;
    if (value.length > MAX_CHARS) {
      // prevent extra characters
      setError(`Maximum ${MAX_CHARS.toLocaleString()} characters allowed`);
    } else {
      setError('');
    }
    setPasteText(value);
  };

  const remaining = MAX_CHARS - pasteText.length;

  return (
    <div className="space-y-2">
      <h2 className="text-lg font-medium text-gray-900">Paste Text</h2>
      <textarea
        value={pasteText}
        onChange={handleChange}
        placeholder="Paste your content here..."
        className="w-full h-48 rounded-2xl border border-gray-300 p-4 text-sm focus:outline-none focus:ring-2 focus:ring-brand-purple resize-none"
      />
      <div className="flex justify-between text-xs text-gray-500">
        <span>{pasteText.length.toLocaleString()} / {MAX_CHARS.toLocaleString()} characters</span>
        {remaining < 0 && (
          <span className="flex items-center text-red-600">
            <AlertCircle className="w-4 h-4 mr-1" />
            Exceeded limit
          </span>
        )}
      </div>
      {pasteText.length > 0 && pasteText.length < MIN_CHARS && (
        <p className="text-sm text-red-600">Minimum {MIN_CHARS} characters required</p>
      )}
    </div>
  );
}
