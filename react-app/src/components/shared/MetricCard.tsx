import type { LucideIcon } from 'lucide-react';
import { TrendingUp } from 'lucide-react';
import { GlassCard } from './GlassCard';
import { AnimatedCounter } from './AnimatedCounter';

export const MetricCard = ({
  title,
  value,
  subtitle,
  icon: Icon,
  gradient,
  trend
}: {
  title: string;
  value: string | number;
  subtitle: string;
  icon: LucideIcon;
  gradient: string;
  trend?: number;
}) => (
  <GlassCard className="p-6 group hover:scale-105 transition-all duration-500">
    <div className="flex items-start justify-between mb-4">
      <div className="flex-1">
        <p className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">
          {title}
        </p>
        <div className="flex items-baseline gap-2">
          <h3 className={`text-4xl font-black bg-gradient-to-br ${gradient} bg-clip-text text-transparent`}>
            {typeof value === 'number' ? <AnimatedCounter value={value} /> : value}
          </h3>
          {trend !== undefined && (
            <span className={`text-sm font-bold flex items-center gap-1 ${trend >= 0 ? 'text-green-500' : 'text-red-500'}`}>
              {trend >= 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingUp className="w-4 h-4 rotate-180" />}
              {Math.abs(trend)}%
            </span>
          )}
        </div>
        <p className="text-xs text-gray-500 mt-2 font-medium">{subtitle}</p>
      </div>
      <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${gradient} flex items-center justify-center shadow-lg group-hover:scale-110 group-hover:rotate-6 transition-all duration-500`}>
        <Icon className="w-8 h-8 text-white" />
      </div>
    </div>
  </GlassCard>
);