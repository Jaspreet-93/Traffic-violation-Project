from app.services.analytics.analytics_service import analytics_service

def test_analytics_metrics_generation():
    print("Testing analytics summary query...")
    summary = analytics_service.get_summary()
    assert summary is not None
    assert "total_violations" in summary
    assert "helmet_cases" in summary
    assert "seatbelt_cases" in summary
    assert "red_light_cases" in summary
    print(f"Summary metrics: {summary}")

    print("\nTesting daily trends statistics...")
    daily = analytics_service.get_daily_stats()
    assert isinstance(daily, list)
    assert len(daily) == 7
    assert "date" in daily[0]
    assert "count" in daily[0]
    print(f"Daily data (last 7 days): {daily}")

    print("\nTesting category classification statistics...")
    types = analytics_service.get_type_stats()
    assert isinstance(types, list)
    assert len(types) >= 4
    assert "type" in types[0]
    assert "count" in types[0]
    print(f"Category data: {types}")

    print("\n--- Analytics Service Unit Tests Passed successfully! ---")

if __name__ == "__main__":
    test_analytics_metrics_generation()
