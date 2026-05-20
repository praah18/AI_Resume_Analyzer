import {
  Bar,
  BarChart,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

const COLORS = ['#2563eb', '#6366f1', '#8b5cf6'];

export function ATSScoreGauge({ score }) {
  const data = [
    { name: 'Score', value: score },
    { name: 'Remaining', value: Math.max(0, 100 - score) },
  ];

  return (
    <div className="relative h-48 w-full">
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            startAngle={180}
            endAngle={0}
            dataKey="value"
            stroke="none"
          >
            <Cell fill="#2563eb" />
            <Cell fill="#e2e8f0" className="dark:fill-slate-700" />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <div className="absolute inset-0 flex flex-col items-center justify-center pt-8">
        <span className="text-4xl font-bold text-brand-600">{score}%</span>
        <span className="text-xs text-slate-500">ATS Score</span>
      </div>
    </div>
  );
}

export function MetricsBarChart({ semantic, keyword, ats }) {
  const data = [
    { name: 'Semantic (BERT)', value: semantic },
    { name: 'Keyword Match', value: keyword },
    { name: 'Overall ATS', value: ats },
  ];

  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={data} layout="vertical" margin={{ left: 20, right: 20 }}>
        <XAxis type="number" domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
        <YAxis type="category" dataKey="name" width={120} tick={{ fontSize: 12 }} />
        <Tooltip formatter={(v) => [`${v}%`, 'Score']} />
        <Bar dataKey="value" radius={[0, 8, 8, 0]}>
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
