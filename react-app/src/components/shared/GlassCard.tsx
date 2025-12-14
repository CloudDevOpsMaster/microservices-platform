import React from 'react';

export const GlassCard = ({ 
  children, 
  className = '', 
  glass = false 
}: { 
  children: React.ReactNode; 
  className?: string;
  glass?: boolean;
}) => (
  <div className={`
    ${glass ? 'bg-white/10' : 'bg-white/80'}
    backdrop-blur-xl 
    rounded-3xl 
    shadow-2xl 
    border 
    border-white/20 
    hover:shadow-3xl 
    transition-all 
    duration-500 
    ${className}
  `}>
    {children}
  </div>
);