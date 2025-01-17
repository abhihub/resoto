from resotolib.logger import log
from resotolib.core.model_export import node_from_dict, node_to_dict
from resotolib.types import Json
from typing import Any, Dict, List


def core_tag_tasks_processor(message: Dict[str, Any]) -> Json:
    task_id = message.get("task_id")
    # task_name = message.get("task_name")
    # task_attrs = message.get("attrs", {})
    task_data: Dict[str, Any] = message.get("data", {})
    delete_tags: List[str] = task_data.get("delete", [])
    update_tags: Dict[str, str] = task_data.get("update", {})
    node_data: Dict[str, Any] = task_data.get("node", {})
    result = "done"
    extra_data: Dict[str, Any] = {}

    try:
        node = node_from_dict(node_data, include_select_ancestors=True)
        for delete_tag in delete_tags:
            del node.tags[delete_tag]

        for k, v in update_tags.items():
            node.tags[k] = v

        node_dict = node_to_dict(node)
        extra_data.update({"data": node_dict})
    except Exception as e:
        log.exception("Error while updating tags")
        result = "error"
        extra_data["error"] = str(e)

    reply_message = {
        "task_id": task_id,
        "result": result,
    }
    reply_message.update(extra_data)
    return reply_message
