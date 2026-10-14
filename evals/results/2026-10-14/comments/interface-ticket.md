Move directory export to the canonical source in directory/source.py. Retire the old source implementation. The new source has the same active records in the same order, already normalized to key and label. Preserve the public export_directory result and read_v1 API, CSV wire format, display labels, and tag results. Do not add dependencies.

The public labels_for API now takes only tags. Remove support for the optional explicit buffer argument; callers must not pass it. This request intentionally changes that API contract.
