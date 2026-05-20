import { Link } from 'react-router-dom';
import {
  BarChart3,
  Brain,
  Download,
  Sparkles,
  Target,
  Zap,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const features = [
  {
    icon: Target,
    title: 'ATS Compatibility Score',
    desc: 'BERT semantic similarity + keyword matching for recruiter-ready scores.',
  },
  {
    icon: Brain,
    title: 'AI-Powered Feedback',
    desc: 'Gemini 2.0 Flash generates personalized strengths, gaps, and tips.',
  },
  {
    icon: BarChart3,
    title: 'Skill Gap Analysis',
    desc: 'See matched vs missing skills against any job description instantly.',
  },
  {
    icon: Sparkles,
    title: 'Keyword Optimization',
    desc: 'Get ATS keyword suggestions tailored to your target role.',
  },
  {
    icon: Download,
    title: 'PDF Report Export',
    desc: 'Download a professional analysis report for interviews and revisions.',
  },
  {
    icon: Zap,
    title: 'RAG-Style Pipeline',
    desc: 'Sentence Transformers embeddings with intelligent retrieval scoring.',
  },
];

export default function Landing() {
  const { user } = useAuth();

  return (
    <div>
      <section className="relative overflow-hidden bg-gradient-to-br from-brand-50 via-white to-indigo-50 py-20 dark:from-slate-950 dark:via-slate-950 dark:to-brand-950/20 sm:py-28">
        <div className="mx-auto max-w-6xl px-4 text-center sm:px-6">
          <span className="mb-4 inline-block rounded-full bg-brand-100 px-4 py-1 text-xs font-semibold text-brand-700 dark:bg-brand-900/50 dark:text-brand-300">
            Gemini · BERT · FastAPI · React
          </span>
          <h1 className="text-4xl font-extrabold tracking-tight sm:text-6xl">
            Beat the ATS. <span className="gradient-text">Land the interview.</span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-600 dark:text-slate-400">
            Upload your resume, paste a job description, and get instant ATS scores,
            skill gap analysis, and AI-powered improvement suggestions.
          </p>
          <div className="mt-10 flex flex-wrap justify-center gap-4">
            <Link to={user ? '/analyze' : '/register'} className="btn-primary px-8 py-3 text-base">
              Analyze My Resume
            </Link>
            <Link to={user ? '/dashboard' : '/login'} className="btn-secondary px-8 py-3 text-base">
              View Dashboard
            </Link>
          </div>
        </div>
      </section>

      <section className="py-20">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <h2 className="text-center text-3xl font-bold">Everything you need to optimize</h2>
          <p className="mx-auto mt-3 max-w-xl text-center text-slate-600 dark:text-slate-400">
            Industry-grade pipeline built for FAANG-level portfolios and internship applications.
          </p>
          <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {features.map(({ icon: Icon, title, desc }) => (
              <div key={title} className="card hover:shadow-md transition">
                <Icon className="mb-4 h-8 w-8 text-brand-600" />
                <h3 className="text-lg font-semibold">{title}</h3>
                <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-t border-slate-200 bg-slate-100 py-16 dark:border-slate-800 dark:bg-slate-900/50">
        <div className="mx-auto max-w-3xl px-4 text-center sm:px-6">
          <h2 className="text-2xl font-bold">Ready to stand out?</h2>
          <p className="mt-3 text-slate-600 dark:text-slate-400">
            Join thousands of candidates optimizing resumes with AI — free to start.
          </p>
          <Link to="/register" className="btn-primary mt-8 inline-flex px-8 py-3">
            Create Free Account
          </Link>
        </div>
      </section>
    </div>
  );
}
