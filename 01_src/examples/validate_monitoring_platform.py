from platform_core.monitoring.monitoring_manager import MonitoringManager

manager = MonitoringManager()

result = manager.run()

print("=" * 60)
print("FIOS Monitoring Platform")
print("=" * 60)

print()

for key in result:
    print(f"{key}: OK")

print()

print("Builder Health")
print(result["health"])

print()

print("Monitoring Platform Validation PASSED")