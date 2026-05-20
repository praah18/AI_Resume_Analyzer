export function SkillList({ skills, variant = 'matched' }) {
  if (!skills?.length) {
    return <p className="text-sm text-slate-500">None detected</p>;
  }

  const colors =
    variant === 'matched'
      ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300'
      : 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300';

  return (
    <div className="flex flex-wrap gap-2">
      {skills.map((skill) => (
        <span key={skill} className={`rounded-full px-3 py-1 text-xs font-medium ${colors}`}>
          {skill}
        </span>
      ))}
    </div>
  );
}
