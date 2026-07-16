
HOOKS = {
    "STOP": [],
    "PreToolUse": [],
    "PostToolUse": [],
    "UserPromptSubmit": [],
}

def register_hook(event, callback):
    HOOKS[event].append(callback)

def trigger_hooks(event, *args):
    for callback in HOOKS[event]:
        result = callback(*args)
        if result is not None:
            return result
    return None 

def agent_loop(messages: list):
    while True:
        response = client.messages.create()
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            force = trigger_hooks("STOP", messages)
            if force:
                messages.append({"role":"user", "content": force})
                continue
            return
        
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            blocked = trigger_hooks("PreToolUse", block)
            if blocked:
                results.append({"role": "user", "tool_use_id": block.id, "content": str(blocked)})
                continue
            
            handler = TOOL_HANDLERS.get(block.name)
            output = handler(**block.input) if handler else f"Unknown: {block.name}"

            trigger_hooks("PostToolUse", block, output)

            results.append({"type": "tool_result", "tool_use_id": block.id, "content": output})

        messages.append({"role": "user", "content": results})