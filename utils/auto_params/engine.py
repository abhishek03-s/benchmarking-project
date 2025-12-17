import importlib

def get_auto_params(tool_name: str, sysinfo: dict) -> dict:
    """
    Dynamically load auto-parameter plugin for given tool.
    Example: tool_name="osu" -> utils.auto_params.osu.AutoParams
    """
    try:
        module = importlib.import_module(f"utils.auto_params.{tool_name}")
        cls = getattr(module, "AutoParams")
        instance = cls()
        return instance.compute(sysinfo)
    except ModuleNotFoundError:
        return {}
    except AttributeError:
        return {}
