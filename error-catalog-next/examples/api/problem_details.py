from dataclasses import asdict, is_dataclass


def build_problem_payload(problem_spec, error):
    payload = {
        "type": problem_spec.type_uri,
        "code": problem_spec.code,
        "title": problem_spec.title,
        "status": problem_spec.http_status,
    }
    if is_dataclass(error):
        payload["context"] = asdict(error)
    return payload
