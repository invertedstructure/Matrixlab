from importlib.util import spec_from_file_location, module_from_spec
import pathlib

p = pathlib.Path("src/matrixlab/cli.py")
spec = spec_from_file_location("cli_module", p)
mod = module_from_spec(spec)
spec.loader.exec_module(mod)
print("module", mod)
print("app_type", type(mod.app))
try:
    cmds = [c.name for c in mod.app.registered_commands]
except Exception as e:
    cmds = f"error: {e}"
print("registered_commands", cmds)
try:
    cmd = mod.app.get_command(None, "run")
    print("get_command", cmd)
except Exception as e:
    print("get_command_error", e)
