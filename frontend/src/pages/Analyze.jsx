import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles } from 'lucide-react';
import { analysisApi } from '../api/client';
import FileDropzone from '../components/FileDropzone';
import LoadingSpinner from '../components/LoadingSpinner';

export default function Analyze() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please upload a PDF resume');
      return;
    }
    if (jobDescription.trim().length < 50) {
      setError('Job description must be at least 50 characters');
      return;
    }

    setError('');
    setLoading(true);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);
    formData.append('job_title', jobTitle);

    try {
      const { data } = await analysisApi.analyze(formData);
      navigate(`/results/${data.id}`, { state: { result: data } });
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-20">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold">Analyze Resume</h1>
        <p className="mt-2 text-slate-600 dark:text-slate-400">
          Upload your PDF and paste the job description for instant ATS insights
        </p>
      </div>

      <form onSubmit={handleAnalyze} className="space-y-6">
        {error && (
          <div className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700 dark:bg-red-900/30 dark:text-red-300">
            {error}
          </div>
        )}

        <div className="card">
          <h2 className="mb-4 font-semibold">1. Upload Resume (PDF)</h2>
          <FileDropzone file={file} onFileChange={setFile} />
        </div>

        <div className="card space-y-4">
          <h2 className="font-semibold">2. Job Details</h2>
          <div>
            <label className="mb-1 block text-sm font-medium">Job Title (optional)</label>
            <input
              className="input-field"
              placeholder="e.g. Software Engineer Intern"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Job Description *</label>
            <textarea
              required
              rows={10}
              className="input-field resize-y"
              placeholder="Paste the full job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
            <p className="mt-1 text-xs text-slate-500">
              {jobDescription.length} characters (min 50)
            </p>
          </div>
        </div>

        <button type="submit" className="btn-primary w-full py-3 text-base">
          <Sparkles className="h-5 w-5" />
          Run AI Analysis
        </button>
      </form>
    </div>
  );
}
