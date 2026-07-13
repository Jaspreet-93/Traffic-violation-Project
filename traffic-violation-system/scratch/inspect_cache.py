from app.services.evidence.evidence_service import evidence_service, fallback_evidence_cache
print("Cache length:", len(fallback_evidence_cache))
for item in fallback_evidence_cache:
    print(item)
