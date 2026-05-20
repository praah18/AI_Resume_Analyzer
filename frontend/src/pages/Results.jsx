import { useEffect, useState } from 'react';
import { Link, useLocation, useParams } from 'react-router-dom';
import { Download, RotateCcw } from 'lucide-react';
import { analysisApi } from '../api/client';
import LoadingSpinner from '../components/LoadingSpinner';
import { ATSScoreGauge, MetricsBarChart } from '../components/ScoreChart';
import { SkillList } from '../components/SkillBadge';

export default function Results() {
  const { id } = useParams();
  const location = useLocation();
  const [result, setResult] = useState(location.state?.result || null);
  const [loading, setLoading] = useState(!result);
  const [error, setError] = useState('');

  useEffect(() => {
    if (result) return;
    analysisApi
      .get(id)
      .then(({ data }) => setResult(data))
      .catch(() => setError('Could not load analysis'))
      .finally(() => setLoading(false));
  }, [id, result]);

  const downloadReport = () => {
    const token = localStorage.getItem('token');
    const url = analysisApi.reportUrl(id);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `analysis_${id}.pdf`);
    fetch(url, { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => r.blob())
      .then((blob) => {
        const blobUrl = URL.createObjectURL(blob);
        link.href = blobUrl;
        link.click();
        URL.revokeObjectURL(blobUrl);
      });
  };

  if (loading) return <LoadingSpinner label="Loading results..." />;
  if (error || !result) {
    return (
      <div className="py-20 text-center">
        <p className="text-red-600">{error || 'Not found'}</p>
        <Link to="/analyze" className="btn-primary mt-4 inline-flex">
          New Analysis
        </Link>
      </div>
    );
  }

  const feedback = result.feedback || {};

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">Analysis Results</h1>
          <p className="mt-1 text-slate-600 dark:text-slate-400">
            {result.resume_filename}
            {result.job_title && ` · ${result.job_title}`}
          </p>
        </div>
        <div className="flex gap-3">
          <button type="button" onClick={downloadReport} className="btn-secondary">
            <Download className="h-4 w-4" />
            Download PDF
          </button>
          <Link to="/analyze" className="btn-primary">
            <RotateCcw className="h-4 w-4" />
            Analyze Again
          </Link>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="card flex flex-col items-center lg:col-span-1">
          <h2 className="mb-2 text-lg font-semibold">ATS Score</h2>
          <ATSScoreGauge score={Math.round(result.ats_score)} />
        </div>
        <div className="card lg:col-span-2">
          <h2 className="mb-4 text-lg font-semibold">Score Breakdown</h2>
          <MetricsBarChart
            semantic={result.semantic_similarity}
            keyword={result.keyword_match_rate}
            ats={result.ats_score}
          />
        </div>
      </div>

      <div className="mt-6 grid gap-6 md:grid-cols-2">
        <div className="card">
          <h2 className="mb-4 font-semibold text-emerald-700 dark:text-emerald-400">
            Matched Skills ({result.matched_skills?.length || 0})
          </h2>
          <SkillList skills={result.matched_skills} variant="matched" />
        </div>
        <div className="card">
          <h2 className="mb-4 font-semibold text-amber-700 dark:text-amber-400">
            Missing Skills ({result.missing_skills?.length || 0})
          </h2>
          <SkillList skills={result.missing_skills} variant="missing" />
        </div>
      </div>

      {feedback.summary && (
        <div className="card mt-6">
          <h2 className="text-lg font-semibold">AI Feedback</h2>
          <p className="mt-3 text-slate-700 dark:text-slate-300">{feedback.summary}</p>
          <div className="mt-6 grid gap-6 md:grid-cols-3">
            <FeedbackList title="Strengths" items={feedback.strengths} color="emerald" />
            <FeedbackList title="Weaknesses" items={feedback.weaknesses} color="amber" />
            <FeedbackList title="ATS Tips" items={feedback.ats_tips} color="brand" />
          </div>
        </div>
      )}

      <div className="mt-6 grid gap-6 md:grid-cols-2">
        <div className="card">
          <h2 className="mb-4 font-semibold">Improvement Suggestions</h2>
          <ul className="space-y-2">
            {(result.suggestions || []).map((s, i) => (
              <li key={i} className="flex gap-2 text-sm text-slate-700 dark:text-slate-300">
                <span className="font-bold text-brand-600">{i + 1}.</span>
                {s}
              </li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h2 className="mb-4 font-semibold">Keyword Optimization</h2>
          <div className="flex flex-wrap gap-2">
            {(result.keyword_suggestions || []).map((kw) => (
              <span
                key={kw}
                className="rounded-lg bg-brand-50 px-3 py-1 text-xs font-medium text-brand-800 dark:bg-brand-900/40 dark:text-brand-200"
              >
                {kw}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function FeedbackList({ title, items, color }) {
  if (!items?.length) return null;
  const dot =
    color === 'emerald'
      ? 'bg-emerald-500'
      : color === 'amber'
        ? 'bg-amber-500'
        : 'bg-brand-500';

  return (
    <div>
      <h3 className="text-sm font-semibold">{title}</h3>
      <ul className="mt-2 space-y-2">
        {items.map((item, i) => (
          <li key={i} className="flex gap-2 text-sm text-slate-600 dark:text-slate-400">
            <span className={`mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full ${dot}`} />
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
