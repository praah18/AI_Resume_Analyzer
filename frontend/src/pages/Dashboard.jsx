import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, FileSearch, TrendingUp } from 'lucide-react';
import { analysisApi } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { ATSScoreGauge } from '../components/ScoreChart';

export default function Dashboard() {
  const { user } = useAuth();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    analysisApi
      .history()
      .then(({ data }) => setHistory(data))
      .catch(() => setHistory([]))
      .finally(() => setLoading(false));
  }, []);

  const latest = history[0];
  const avgScore =
    history.length > 0
      ? Math.round(history.reduce((s, h) => s + h.ats_score, 0) / history.length)
      : 0;

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Welcome, {user?.full_name?.split(' ')[0]}</h1>
        <p className="mt-1 text-slate-600 dark:text-slate-400">
          Your AI-powered resume optimization dashboard
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="card lg:col-span-1">
          <h2 className="text-sm font-medium text-slate-500">Latest ATS Score</h2>
          {latest ? (
            <ATSScoreGauge score={Math.round(latest.ats_score)} />
          ) : (
            <div className="py-12 text-center text-sm text-slate-500">No analyses yet</div>
          )}
        </div>

        <div className="card lg:col-span-2">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-lg font-semibold">Quick Stats</h2>
              <p className="text-sm text-slate-500">Overview of your resume analyses</p>
            </div>
            <TrendingUp className="h-6 w-6 text-brand-600" />
          </div>
          <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3">
            <Stat label="Total Analyses" value={history.length} />
            <Stat label="Average ATS" value={avgScore ? `${avgScore}%` : '—'} />
            <Stat
              label="Latest Role"
              value={latest?.job_title || '—'}
              className="col-span-2 sm:col-span-1"
            />
          </div>
          <Link to="/analyze" className="btn-primary mt-8 inline-flex">
            <FileSearch className="h-4 w-4" />
            New Analysis
          </Link>
        </div>
      </div>

      <div className="card mt-8">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Recent Analyses</h2>
          <Link to="/history" className="text-sm font-medium text-brand-600 hover:underline">
            View all
          </Link>
        </div>
        {loading ? (
          <p className="mt-4 text-sm text-slate-500">Loading...</p>
        ) : history.length === 0 ? (
          <p className="mt-4 text-sm text-slate-500">
            No history yet.{' '}
            <Link to="/analyze" className="text-brand-600 hover:underline">
              Run your first analysis
            </Link>
          </p>
        ) : (
          <ul className="mt-4 divide-y divide-slate-200 dark:divide-slate-800">
            {history.slice(0, 5).map((item) => (
              <li key={item.id} className="flex items-center justify-between py-3">
                <div>
                  <p className="font-medium">{item.resume_filename}</p>
                  <p className="text-xs text-slate-500">
                    {item.job_title || 'No title'} · {new Date(item.created_at).toLocaleDateString()}
                  </p>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-lg font-bold text-brand-600">
                    {Math.round(item.ats_score)}%
                  </span>
                  <Link
                    to={`/results/${item.id}`}
                    className="text-brand-600 hover:text-brand-700"
                  >
                    <ArrowRight className="h-5 w-5" />
                  </Link>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

function Stat({ label, value, className = '' }) {
  return (
    <div className={`rounded-xl bg-slate-50 p-4 dark:bg-slate-800/50 ${className}`}>
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-1 text-2xl font-bold">{value}</p>
    </div>
  );
}
