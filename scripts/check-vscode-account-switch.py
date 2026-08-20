"""Small regression check for VS Code Claude account selection."""

import json
import tempfile
from pathlib import Path
from types import SimpleNamespace

from ai_account_hub import core as L
from ai_account_hub.engine import HubEngine


def main() -> None:
    original_appdata = L.APPDATA_ROOT
    original_run_capture = L.run_capture
    try:
        root = Path(tempfile.mkdtemp(prefix="ai-hub-vscode-check-"))
        L.APPDATA_ROOT = root
        settings = root / "Code" / "User" / "settings.json"
        settings.parent.mkdir(parents=True)
        original = {"claudeCode.environmentVariables": [{"name": "KEEP", "value": "yes"}]}
        settings.write_text(json.dumps(original), encoding="utf-8")

        engine = HubEngine.__new__(HubEngine)
        engine.claude_code_path = "claude"
        first = root / "claude-one"
        second = root / "claude-two"
        for home in (first, second):
            home.mkdir()
            (home / ".credentials.json").write_text("{}", encoding="utf-8")

        authenticated_email = "one@example.com"
        L.run_capture = lambda *args, **kwargs: SimpleNamespace(
            returncode=0,
            stdout=json.dumps({"loggedIn": True, "email": authenticated_email}),
            stderr="",
        )
        first_profile = {
            "provider": "claude", "name": "one", "loginEmail": "one@example.com",
            "claudeConfigDir": str(first), "workspace": str(root / "workspace"),
        }
        second_profile = {
            "provider": "claude", "name": "two", "loginEmail": "two@example.com",
            "claudeConfigDir": str(second), "workspace": str(root / "workspace"),
        }
        ok, _ = engine.action_vscode(first_profile)
        assert ok
        authenticated_email = "wrong@example.com"
        before_mismatch = settings.read_text(encoding="utf-8")
        ok, _ = engine.action_vscode(second_profile)
        assert not ok
        assert settings.read_text(encoding="utf-8") == before_mismatch
        authenticated_email = "two@example.com"
        ok, _ = engine.action_vscode(second_profile)
        assert ok
        current = json.loads(settings.read_text(encoding="utf-8"))
        variables = current["claudeCode.environmentVariables"]
        assert {"name": "KEEP", "value": "yes"} in variables
        selected = [item for item in variables if item["name"] == "CLAUDE_CONFIG_DIR"]
        assert selected == [{"name": "CLAUDE_CONFIG_DIR", "value": str(second)}]
        backup = settings.with_name("settings.ai-account-hub.backup.json")
        assert json.loads(backup.read_text(encoding="utf-8")) == original
    finally:
        L.APPDATA_ROOT = original_appdata
        L.run_capture = original_run_capture


if __name__ == "__main__":
    main()
    print("VS Code account-switch check passed")
