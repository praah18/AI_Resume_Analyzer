export default function LoadingSpinner({ label = 'Analyzing your resume...' }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-16">
      <div className="relative h-16 w-16">
        <div className="absolute inset-0 rounded-full border-4 border-brand-100 dark:border-brand-900" />
        <div className="absolute inset-0 animate-spin rounded-full border-4 border-transparent border-t-brand-600" />
      </div>
      <p className="text-sm font-medium text-slate-600 dark:text-slate-400">{label}</p>
      <p className="max-w-sm text-center text-xs text-slate-500">
        Running BERT embeddings, skill extraction, and Gemini AI feedback...
      </p>
    </div>
  );
}
