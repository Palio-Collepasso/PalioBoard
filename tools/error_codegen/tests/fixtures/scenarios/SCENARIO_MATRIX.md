# Scenario matrix

| Outcome | Level | Scenario | Input files | Expected files |
|---|---|---:|---:|---:|
| failure | simple | `doc_injection_missing_heading` | 1 | 1 |
| failure | simple | `example_has_extra_context` | 2 | 1 |
| failure | simple | `example_missing_required_context` | 2 | 1 |
| failure | simple | `invalid_code_format` | 2 | 1 |
| failure | simple | `invalid_http_status` | 2 | 1 |
| failure | simple | `invalid_type_slug` | 2 | 1 |
| failure | medium | `duplicate_code_across_modules` | 3 | 1 |
| failure | medium | `duplicate_type_slug_across_modules` | 3 | 1 |
| failure | medium | `invalid_nested_context_example` | 2 | 1 |
| failure | medium | `key_mismatch_and_missing_translation_key` | 2 | 1 |
| failure | complex | `combined_catalog_conflicts` | 3 | 1 |
| failure | complex | `split_catalog_multiple_cross_file_collisions` | 4 | 1 |
| success | simple | `single_error_minimal` | 2 | 6 |
| success | simple | `single_error_with_optional_context` | 2 | 6 |
| success | simple | `single_error_with_required_context` | 2 | 6 |
| success | medium | `multiple_errors_one_module` | 2 | 6 |
| success | medium | `nested_context_one_error` | 2 | 6 |
| success | medium | `split_catalog_two_modules` | 3 | 9 |
| success | complex | `full_catalog_multi_module` | 5 | 15 |
| success | complex | `mixed_statuses_and_modules` | 5 | 15 |
| success | complex | `rich_context_arrays_and_nested` | 3 | 9 |
