export const ModernTooltip = ({ active, payload, label }: { 
  active?: boolean; 
  payload?: any[]; 
  label?: string;
}) => {
  if (!active || !payload || !payload.length) return null;

  return (
    <div className="bg-gray-900/95 backdrop-blur-xl px-4 py-3 rounded-2xl shadow-2xl border border-white/10">
      <p className="text-white font-bold mb-2">{label}</p>
      {payload.map((entry: any, index: number) => (
        <div key={index} className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: entry.color }} />
          <span className="text-gray-300 text-sm font-medium">
            {entry.name}: <span className="text-white font-bold">{entry.value}</span>
          </span>
        </div>
      ))}
    </div>
  );
};