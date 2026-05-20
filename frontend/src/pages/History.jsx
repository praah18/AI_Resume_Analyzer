import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { analysisApi } from '../api/client';

export default function History() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    analysisApi
      .history()
      .then(({ data }) => setItems(data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <h1 className="text-3xl font-bold">Analysis History</h1>
      <p className="mt-1 text-slate-600 dark:text-slate-400">
        All your past resume analyses
      </p>

      <div className="card mt-8 overflow-x-auto">
        {loading ? (
          <p className="text-sm text-slate-500">Loading...</p>
        ) : items.length === 0 ? (
          <p className="text-sm text-slate-500">
            No analyses yet.{' '}
            <Link to="/analyze" className="text-brand-600 hover:underline">
              Start one
            </Link>
          </p>
        ) : (
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-700">
                <th className="pb-3 font-semibold">Resume</th>
                <th className="pb-3 font-semibold">Role</th>
                <th className="pb-3 font-semibold">ATS Score</th>
                <th className="pb-3 font-semibold">Date</th>
                <th className="pb-3 font-semibold" />
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr
                  key={item.id}
                  className="border-b border-slate-100 dark:border-slate-800"
                >
                  <td className="py-3">{item.resume_filename}</td>
                  <td className="py-3 text-slate-600 dark:text-slate-400">
                    {item.job_title || '—'}
                  </td>
                  <td className="py-3 font-bold text-brand-600">
                    {Math.round(item.ats_score)}%
                  </td>
                  <td className="py-3 text-slate-500">
                    {new Date(item.created_at).toLocaleString()}
                  </td>
                  <td className="py-3">
                    <Link
                      to={`/results/${item.id}`}
                      className="font-medium text-brand-600 hover:underline"
                    >
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
