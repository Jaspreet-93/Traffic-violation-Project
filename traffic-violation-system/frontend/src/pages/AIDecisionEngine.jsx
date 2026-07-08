import React, { useState, useEffect } from 'react';
import { decisionAPI } from '../services/decisionApi';
import DecisionCard from '../components/decision/DecisionCard';
import DecisionTimeline from '../components/decision/DecisionTimeline';
import DecisionTree from '../components/decision/DecisionTree';
import ExplanationPanel from '../components/decision/ExplanationPanel';
import ConfidenceReasoning from '../components/decision/ConfidenceReasoning';
import PipelineFlow from '../components/decision/PipelineFlow';
import AuditTrail from '../components/decision/AuditTrail';
import DecisionSummary from '../components/decision/DecisionSummary';

export default function AIDecisionEngine() {
  const [latest, setLatest] = useState(null);
  const [history, setHistory] = useState([]);
  const [explanation, setExplanation] = useState(null);
  const [audit, setAudit] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeId, setActiveId] = useState(null);

  const fetchDecisionDetails = async (violationId) => {
    try {
      const [resExpl, resAudit] = await Promise.all([
        decisionAPI.getExplanation(violationId),
        decisionAPI.getAudit(violationId)
      ]);
      setExplanation(resExpl.data);
      setAudit(resAudit.data);
    } catch (err) {
      console.error("Error loading explainable AI stats:", err);
    }
  };

  const loadDashboardData = async () => {
    try {
      const resLatest = await decisionAPI.getLatest();
      const resHistory = await decisionAPI.getHistory();
      
      setLatest(resLatest.data);
      setHistory(resHistory.data.history || []);
      
      const defaultId = violationId => violationId;
      const firstId = resLatest.data?.violation_id || (resHistory.data.history?.[0]?.violation_id);
      if (firstId) {
        setActiveId(firstId);
        await fetchDecisionDetails(firstId);
      }
    } catch (err) {
      console.error("Error loading explainable decision data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const handleSelectViolation = async (violationId) => {
    setActiveId(violationId);
    await fetchDecisionDetails(violationId);
  };

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center space-y-3 p-12 text-slate-550 text-xs">
        <span className="w-6 h-6 rounded-full border-2 border-purple-500 border-t-transparent animate-spin"></span>
        <span>Loading Explainable AI Decision Engine...</span>
      </div>
    );
  }

  // Get current decision path for tree view
  const currentPath = {
    rule: explanation?.reason || "Checking classifier rules matching parameters",
    branches: explanation?.supporting_detections || ["Object tracked: True", "Violations Logged: True"]
  };

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100 font-sans">Explainable AI Decision Engine</h2>
        <p className="text-xs text-slate-500">Trace model classifier decision branches, rule criteria, and audit logs.</p>
      </div>

      {/* Horizontal pipeline flow */}
      <PipelineFlow />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <DecisionCard decision={latest} />
            <DecisionTree path={currentPath} />
          </div>

          {/* Explanation panel */}
          <ExplanationPanel explanation={explanation} />
        </div>

        {/* Right (1 col) */}
        <div className="space-y-6">
          {/* Decision Timeline */}
          <DecisionTimeline activeIndex={activeId ? 11 : 0} />

          {/* Audit trail details */}
          <AuditTrail audit={audit} />
        </div>
      </div>

      {/* Decision Summary History */}
      <DecisionSummary historyList={history} onSelect={handleSelectViolation} />
    </div>
  );
}
