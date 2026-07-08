import React from 'react';
import { GitCommit, GitPullRequest, ArrowDown } from 'lucide-react';

export default function DecisionTree({ path }) {
  if (!path) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <GitPullRequest className="w-4.5 h-4.5 text-purple-400" />
        <span>Infraction Decision Tree Nodes</span>
      </h3>

      <div className="flex flex-col items-center space-y-3 font-semibold text-xs">
        {/* Rule Root */}
        <div className="bg-purple-500/10 border border-purple-500/20 text-purple-450 p-2.5 rounded-lg text-center w-full">
          Root Evaluator: {path.rule}
        </div>

        <ArrowDown className="w-4.5 h-4.5 text-slate-600" />

        {/* Branches */}
        <div className="grid grid-cols-1 gap-2.5 w-full">
          {path.branches.map((b, idx) => (
            <div key={idx} className="bg-slate-950/40 border border-slate-850 p-2.5 rounded-lg flex items-center space-x-2 text-slate-350">
              <GitCommit className="w-3.5 h-3.5 text-purple-400" />
              <span>{b}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
