import json

with open("scratch_specs_parsed.json", "r") as f:
    specs = json.load(f)

unimplemented = [s for s in specs if s["build_status"] == "NOT STARTED"]
untested = [s for s in specs if s["test_status"] == "NO TESTS"]

print(f"Total specs: {len(specs)}")
print(f"Unimplemented specs ({len(unimplemented)}):")
for s in sorted(unimplemented, key=lambda x: x["spec_id"]):
    print(f"  - {s['spec_id']}: produces={s['produces']}, consumes={s['consumes']}")

print("\nUntested specs but implemented:")
implemented_untested = [s for s in specs if s["build_status"] == "IMPLEMENTED" and s["test_status"] == "NO TESTS"]
print(f"Total: {len(implemented_untested)}")
for s in sorted(implemented_untested, key=lambda x: x["spec_id"]):
    print(f"  - {s['spec_id']}: impl_files={[f.split('\\\\')[-1] for f in s['impl_files']]}")

# Find missing dependencies
# If spec consumes a DEP-ID that is not produced by any spec in the system
all_produced = set()
for s in specs:
    for p in s["produces"]:
        all_produced.add(p)

# We can also add some standard system-produced DEP-IDs if they are built-in:
# e.g., DEP-ENG-003, DEP-ENG-004, etc., let's see which consumed DEP-IDs are missing a producer
print("\nConsumed DEP-IDs without any spec marked as producer:")
missing_producers = {}
for s in specs:
    for c in s["consumes"]:
        if c not in all_produced:
            missing_producers.setdefault(c, []).append(s["spec_id"])

for dep, consumer_list in sorted(missing_producers.items()):
    print(f"  - {dep} is consumed by: {', '.join(consumer_list)}")

print("\nProduced DEP-IDs without any consumer:")
unused_producers = {}
all_consumed = set()
for s in specs:
    for c in s["consumes"]:
        all_consumed.add(c)

for s in specs:
    for p in s["produces"]:
        if p not in all_consumed:
            unused_producers.setdefault(p, []).append(s["spec_id"])

for dep, producer_list in sorted(unused_producers.items()):
    print(f"  - {dep} is produced by: {', '.join(producer_list)}")
