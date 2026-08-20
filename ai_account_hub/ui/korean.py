"""Small runtime Korean UI layer for the Windows build.

The upstream app does not expose Qt translation catalogs.  Keep provider and
model identifiers intact while translating user-facing Qt text in one place.
"""

from __future__ import annotations

import re

from PySide6.QtCore import QEvent, QLocale, QObject, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QAbstractButton, QComboBox, QGroupBox, QLabel, QLineEdit, QMenu,
    QPlainTextEdit, QTableWidget, QTabWidget, QTextEdit, QWidget,
)


TEXT = {
    # Window chrome and menus
    "File": "파일", "Reload profiles": "프로필 다시 불러오기",
    "Refresh all": "모두 새로고침", "Open profile folder": "프로필 폴더 열기",
    "Local data...": "로컬 데이터...", "Exit": "종료",
    "Edit": "편집", "Add account": "계정 추가", "Edit selected": "선택 계정 편집",
    "Rename selected": "선택 계정 이름 변경", "Delete selected": "선택 계정 삭제",
    "Community sharing...": "커뮤니티 공유...", "Window": "창",
    "Accounts": "계정", "Statistics": "통계", "Minimize": "최소화",
    "Show Best Next": "다음 추천 보기", "Widget settings...": "위젯 설정...",
    "Notification settings...": "알림 설정...", "Maximize / Restore": "최대화 / 복원",
    "Theme": "테마", "Dark mode": "다크 모드", "Light mode": "라이트 모드",
    "Help": "도움말", "Open README": "README 열기", "Account setup": "계정 설정 안내",
    "View demo (sample data)": "데모 보기 (샘플 데이터)", "About": "정보",
    "AI Account Hub — Demo": "AI Account Hub — 데모",
    "Sample data — not your real accounts": "샘플 데이터 — 실제 계정 아님",
    "Accounts, limits and usage history": "계정·한도·사용 기록",
    "Refreshing…": "새로고침 중…", "Reload": "다시 불러오기",
    "Automatically refresh all accounts on a timer": "설정한 주기마다 모든 계정 자동 새로고침",

    # Accounts workspace
    "Profiles": "계정 목록", "Search profiles": "계정 검색", "View": "보기",
    "+ Add": "+ 추가", "Rename": "이름 변경", "Delete": "삭제",
    "All visible accounts": "표시된 모든 계정", "Month tokens": "이번 달 토큰",
    "This month": "이번 달", "Month active": "이번 달 사용 시간",
    "Pool tokens": "누적 토큰", "All recorded history": "전체 기록",
    "Reset markers": "한도 초기화", "Select an account": "계정을 선택하세요",
    "Usage records": "사용 기록", "Resets available": "사용 가능한 초기화",
    "Account": "계정", "Plan": "요금제", "Capability": "기능",
    "Desktop": "데스크톱", "Weekly left": "주간 잔여량",
    "Weekly reset": "주간 초기화", "Session left": "5시간 잔여량",
    "Session reset": "5시간 초기화", "Path": "경로",
    "SESSION": "실행", "AUTH": "인증", "DIAGNOSTICS & RESET": "진단 및 초기화",
    "Open Desktop": "데스크톱 열기", "Open CLI": "CLI 열기",
    "Apply to VS Code": "VS Code 적용", "Login": "로그인",
    "Device": "기기 인증", "Logout": "로그아웃", "Desktop Login": "데스크톱 로그인",
    "Status": "상태 확인", "Doctor": "진단", "Refresh": "새로고침",
    "Online": "온라인", "Dry run": "사전 점검", "Restore": "복원",
    "Use reset": "초기화 사용", "Set 5h": "5시간 타이머",
    "Clear timer": "타이머 해제", "Open home": "계정 폴더 열기",
    "Seed config": "기본 설정 생성", "ACTIVITY LOG": "작업 기록",
    "No activity yet.": "아직 작업 없음.", "WEEKLY USAGE LEFT": "주간 잔여량",
    "5H SESSION LEFT": "5시간 잔여량", "In use": "사용 중",
    "Ready": "사용 가능", "Not ready": "사용 불가", "Login required": "로그인 필요",
    "Refresh error": "새로고침 오류", "Verifying Codex reset": "Codex 초기화 확인 중",
    "Manual": "수동", "Name": "이름", "Provider": "서비스", "State": "상태",
    "Last refresh": "마지막 새로고침", "Balanced": "균형형", "Compact": "간결형",
    "Identity": "계정 중심", "Usage First": "사용량 중심", "Plan Chips": "요금제 중심",
    "LIMIT RESETS": "한도 초기화", "USAGE BY ACCOUNT": "계정별 사용량",
    "Close": "닫기", "No usage recorded for this day.": "이 날짜의 사용 기록 없음.",
    "Day detail": "일별 상세",

    # Add/edit account
    "Add profile": "계정 추가", "Edit profile": "계정 편집",
    "Register a coding account or a switchable Desktop-only account.":
        "Claude/Codex 계정을 등록합니다. 계정별 인증은 분리 저장됩니다.",
    "Display name": "표시 이름", "Account email": "계정 이메일",
    "Profile path": "프로필 경로", "Workspace": "작업 폴더",
    "Online browser": "온라인 브라우저", "Isolated account browser": "계정 전용 브라우저",
    "System browser": "시스템 브라우저", "Custom command": "사용자 명령",
    "Cancel": "취소", "Save": "저장", "e.g. Codex Client Work": "예: Codex 업무용",
    "Optional label, e.g. name@example.com": "선택 사항: name@example.com",
    "Browser command": "브라우저 명령", "Custom links": "사용자 링크",
    "Print timeout": "출력 제한 시간", "Claude access": "Claude 권한",
    "Claude Code (paid)": "Claude Code (유료)", "Claude Desktop (free)": "Claude Desktop (무료)",
    "Claude Desktop test profile": "Claude Desktop 테스트 계정",
    "Code identity missing": "Claude Code 신원 없음",
    "Login metadata": "로그인 정보",
    "First run Login and Status, then use Desktop Login.":
        "최초 1회 로그인과 상태 확인 후 데스크톱 로그인을 사용하세요.",
    "Optional browser executable/command": "브라우저 실행 파일/명령 (선택)",
    "Label | https://example.com (one per line)": "이름 | https://example.com (한 줄에 하나)",
    "Paid Claude account: use Login for Claude Code, then Desktop Login for Claude Desktop. Both are one-time setup steps.":
        "유료 Claude 계정: Claude Code는 로그인, Claude Desktop은 데스크톱 로그인을 각각 최초 1회 진행하세요.",
    "The Hub keeps this provider's profile state separate from other accounts.":
        "이 서비스의 계정 상태는 다른 계정과 분리 저장됩니다.",

    # Dialogs and common states
    "No account": "계정 없음", "Select an account first.": "먼저 계정을 선택하세요.",
    "Action failed": "작업 실패", "Result": "결과", "Delete account": "계정 삭제",
    "Rename account": "계정 이름 변경", "New name:": "새 이름:",
    "Demo mode": "데모 모드", "This window is already showing sample demo data.": "이미 샘플 데모 데이터를 표시 중입니다.",
    "Demo actions are disabled.": "데모에서는 계정 작업을 사용할 수 없습니다.",
    "VS Code account switching is available for Claude Code profiles only.":
        "VS Code 계정 전환은 Claude Code 계정에서만 사용할 수 있습니다.",
    "Log in to this Claude Code profile first, then apply it to VS Code.":
        "먼저 이 Claude Code 계정에 로그인한 뒤 VS Code에 적용하세요.",
    "VS Code user settings were not found.": "VS Code 사용자 설정을 찾지 못했습니다.",
    "VS Code user settings must be a JSON object.":
        "VS Code 사용자 설정은 JSON 객체 형식이어야 합니다.",
    "claudeCode.environmentVariables must be a list.":
        "VS Code의 Claude 환경변수 설정 형식이 올바르지 않습니다.",
    "Duplicate profile path": "중복 프로필 경로",
    "Use a unique display name so each account keeps separate authentication.":
        "계정별 인증이 분리되도록 서로 다른 표시 이름을 사용하세요.",
    "Enter this Claude account's email in Edit before logging in.":
        "로그인 전에 편집에서 이 Claude 계정의 이메일을 입력하세요.",
    "Wrong Claude account is logged in for this profile.":
        "이 프로필에 다른 Claude 계정이 로그인되어 있습니다.",
    "Claude login identity could not be verified.":
        "Claude 로그인 계정을 확인할 수 없습니다.",
    "&Yes": "예", "Yes": "예", "&No": "아니요", "No": "아니요",
    "&OK": "확인", "OK": "확인", "Open": "열기",

    # Statistics workspace
    "Account scope": "계정 범위", "Range": "기간", "Aggregation": "집계 방식",
    "7 days": "7일", "30 days": "30일", "90 days": "90일",
    "180 days": "180일", "365 days": "365일", "Combined totals": "합계",
    "Average per provider account": "서비스 계정당 평균",
    "Waiting for account data": "계정 데이터 대기 중", "Refresh analytics": "통계 새로고침",
    "Overview": "개요", "Usage, coding activity, and limits at a glance": "사용량·코딩 활동·한도 요약",
    "Usage summary": "사용량 요약", "Attributed tokens": "귀속 토큰",
    "Models used": "사용 모델", "Context reuse": "컨텍스트 재사용",
    "Completed tasks": "완료 작업", "5h usage movement": "5시간 사용량 변화",
    "Weekly usage movement": "주간 사용량 변화", "Chart": "차트",
    "Reset": "초기화", "Focus": "크게 보기", "Export CSV": "CSV 내보내기",
    "Export PNG": "PNG 내보내기", "Model summary": "모델 요약",
    "Recent work": "최근 작업", "Totals by base model; reasoning settings stay visible": "기본 모델별 합계와 추론 설정",
    "Model": "모델", "Reasoning": "추론", "Work tokens": "작업 토큰",
    "Cache reuse": "캐시 재사용", "Tasks": "작업", "Edits": "수정",
    "Unique files": "고유 파일", "Tests": "테스트", "Commands": "명령",
    "Active": "사용 시간", "5h burn": "5시간 소진", "Weekly burn": "주간 소진",
    "Day": "날짜", "Shape": "형태", "Task tokens": "작업 토큰",
    "Files": "파일", "Tests / commands": "테스트 / 명령",
    "Models": "모델", "Choose a model, then filter or sort its observed reasoning settings": "모델 선택 후 관측된 추론 설정 필터·정렬",
    "Sort": "정렬", "Usage high to low": "사용량 높은 순", "Model name": "모델 이름",
    "Productivity": "생산성", "Coding activity observed alongside tokens, active time, and limit use": "토큰·사용 시간·한도와 함께 본 코딩 활동",
    "Compare": "비교", "Compare two to four observed models against one clear baseline": "기준 모델과 2~4개 모델 비교",
    "Comparison roster": "비교 모델 목록", "Compare reasoning": "추론 설정 비교",
    "+ Add model": "+ 모델 추가", "Head-to-head detail": "상세 비교",
    "Community": "커뮤니티", "All visible accounts": "표시된 모든 계정",
    "All Codex accounts": "모든 Codex 계정", "All Claude accounts": "모든 Claude 계정",
    "Scanning history...": "사용 기록 분석 중...", "Analytics unavailable": "통계 사용 불가",
    "All base models": "모든 기본 모델", "All reasoning": "모든 추론 설정",
    "Recent observed work": "최근 관측 작업", "Reset view": "화면 초기화",
    "Selected model": "선택 모델", "Normalize by": "정규화 기준",
    "Raw totals": "원본 합계", "Per 1M work tokens": "작업 토큰 100만당",
    "Per 10 weekly points": "주간 10%p당", "Per active hour": "사용 1시간당",
    "No model activity in this range": "이 기간의 모델 활동 없음",
}

_LOGIC_COMBO_VALUES = (
    "Manual", "Name", "Provider", "State", "Session left", "Weekly left",
    "Last refresh", "Balanced", "Compact", "Identity", "Usage First",
    "Plan Chips", "All reasoning",
)
SOURCE_TEXT = {TEXT[source]: source for source in _LOGIC_COMBO_VALUES}


PATTERNS = (
    (
        re.compile(
            r"^Applied (.+) to new Claude conversations in VS Code\.\n"
            r"Keep the VS Code window open, start a new Claude conversation, then use /resume if needed\.$"
        ),
        lambda m: (
            f"{m[1]} 계정을 VS Code의 새 Claude 대화에 적용했습니다.\n"
            "VS Code 창은 그대로 두고 새 Claude 대화를 연 다음, 필요하면 /resume을 사용하세요."
        ),
    ),
    (
        re.compile(r"^Opened Claude Code login for (.+)\.$"),
        lambda m: f"{m[1]} 계정의 Claude Code 로그인 창을 열었습니다.",
    ),
    (
        re.compile(r"^Opened Claude Code CLI for (.+)\.$"),
        lambda m: f"{m[1]} 계정의 Claude Code CLI를 열었습니다.",
    ),
    (
        re.compile(r"^Opened Claude logout for (.+)\.$"),
        lambda m: f"{m[1]} 계정의 Claude 로그아웃 창을 열었습니다.",
    ),
    (
        re.compile(r"^Could not verify this Claude login: (.+)$", re.DOTALL),
        lambda m: f"Claude 로그인 확인에 실패했습니다: {m[1]}",
    ),
    (
        re.compile(r"^Could not safely update VS Code settings: (.+)$", re.DOTALL),
        lambda m: f"VS Code 설정을 안전하게 변경할 수 없습니다: {m[1]}",
    ),
    (
        re.compile(r"^Could not update VS Code settings: (.+)$", re.DOTALL),
        lambda m: f"VS Code 설정 변경에 실패했습니다: {m[1]}",
    ),
    (
        re.compile(
            r"^(.+) needs a Claude Code identity before Desktop login can be captured safely\. "
            r"Run Claude Login/Status first for (.+), then try Desktop Login again\.$"
        ),
        lambda m: (
            f"{m[1]} 계정의 Claude Code 로그인이 먼저 필요합니다.\n\n"
            f"로그인 → 상태 확인을 완료한 뒤 데스크톱 로그인을 다시 누르세요.\n"
            f"인증 경로: {m[2]}"
        ),
    ),
    (re.compile(r"^Total (\d+)$"), lambda m: f"총 {m[1]}개"),
    (re.compile(r"^(\d+)/(\d+) ready$"), lambda m: f"{m[1]}/{m[2]} 사용 가능"),
    (re.compile(r"^(\d+) ready · (\d+) not ready$"), lambda m: f"사용 가능 {m[1]} · 사용 불가 {m[2]}"),
    (re.compile(r"^Auto Refresh · (On|Off)$"), lambda m: f"자동 새로고침 · {'켜짐' if m[1] == 'On' else '꺼짐'}"),
    (re.compile(r"^Updated (.+)$"), lambda m: f"업데이트 {m[1]}"),
    (re.compile(r"^(\d+) profiles$"), lambda m: f"계정 {m[1]}개"),
    (re.compile(r"^(\d+) history records$"), lambda m: f"기록 {m[1]}개"),
    (re.compile(r"^(\d+) accounts$"), lambda m: f"계정 {m[1]}개"),
    (re.compile(r"^(\d+) contributors$"), lambda m: f"참여자 {m[1]}명"),
    (re.compile(r"^(\d+) observed tasks$"), lambda m: f"관측 작업 {m[1]}개"),
    (re.compile(r"^(\d{2})\n(.+)$"), lambda m: f"{m[1]}\n{translate(m[2])}"),
)


def translate(value: object) -> str:
    text = str(value)
    translated = TEXT.get(text)
    if translated is not None:
        return translated
    for pattern, render in PATTERNS:
        match = pattern.fullmatch(text)
        if match:
            return render(match)
    return text


def source_text(value: object) -> str:
    """Return stable upstream value for logic that uses combo display text."""
    return SOURCE_TEXT.get(str(value), str(value))


def _patch_text_method(cls, name: str) -> None:
    original = getattr(cls, name)

    def localized(self, text, *args, **kwargs):
        return original(self, translate(text), *args, **kwargs)

    setattr(cls, name, localized)


def _patch_combo_method(cls, name: str) -> None:
    original = getattr(cls, name)

    def localized(self, *args):
        values = list(args)
        index = 0 if values and isinstance(values[0], str) else 1
        if len(values) > index and isinstance(values[index], str):
            values[index] = translate(values[index])
        return original(self, *values)

    setattr(cls, name, localized)


def localize(root: QObject) -> None:
    """Translate existing text, including text set inside Qt constructors."""
    try:
        objects = [root, *root.findChildren(QObject)]
    except RuntimeError:
        return
    for obj in objects:
        try:
            if isinstance(obj, QLabel) or isinstance(obj, QAbstractButton):
                obj.setText(translate(obj.text()))
            if isinstance(obj, QWidget):
                obj.setWindowTitle(translate(obj.windowTitle()))
                obj.setToolTip(translate(obj.toolTip()))
            if isinstance(obj, QGroupBox):
                obj.setTitle(translate(obj.title()))
            if isinstance(obj, (QLineEdit, QPlainTextEdit, QTextEdit)):
                obj.setPlaceholderText(translate(obj.placeholderText()))
            if isinstance(obj, QComboBox):
                for index in range(obj.count()):
                    obj.setItemText(index, translate(obj.itemText(index)))
            if isinstance(obj, QTabWidget):
                for index in range(obj.count()):
                    obj.setTabText(index, translate(obj.tabText(index)))
            if isinstance(obj, QTableWidget):
                for column in range(obj.columnCount()):
                    item = obj.horizontalHeaderItem(column)
                    if item is not None:
                        item.setText(translate(item.text()))
            if isinstance(obj, QMenu):
                obj.setTitle(translate(obj.title()))
            if isinstance(obj, QAction):
                obj.setText(translate(obj.text()))
                obj.setToolTip(translate(obj.toolTip()))
        except RuntimeError:
            continue


class _KoreanUiFilter(QObject):
    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.Show:
            QTimer.singleShot(0, lambda obj=watched: localize(obj))
        return False


def install(app) -> None:
    if getattr(app, "_korean_ui_installed", False):
        return
    QLocale.setDefault(QLocale(QLocale.Language.Korean, QLocale.Country.SouthKorea))
    for cls, name in (
        (QLabel, "setText"), (QAbstractButton, "setText"),
        (QWidget, "setWindowTitle"), (QWidget, "setToolTip"),
        (QGroupBox, "setTitle"), (QLineEdit, "setPlaceholderText"),
        (QPlainTextEdit, "setPlaceholderText"), (QTextEdit, "setPlaceholderText"),
        (QAction, "setText"), (QAction, "setToolTip"), (QMenu, "setTitle"),
        (QTabWidget, "setTabText"),
    ):
        _patch_text_method(cls, name)
    for name in ("addItem", "insertItem"):
        _patch_combo_method(QComboBox, name)
    original_add_items = QComboBox.addItems
    QComboBox.addItems = lambda self, texts: original_add_items(self, [translate(text) for text in texts])
    original_current_text = QComboBox.currentText
    original_item_text = QComboBox.itemText
    original_set_current_text = QComboBox.setCurrentText
    original_find_text = QComboBox.findText
    QComboBox.currentText = lambda self: source_text(original_current_text(self))
    QComboBox.itemText = lambda self, index: source_text(original_item_text(self, index))
    QComboBox.setCurrentText = lambda self, text: original_set_current_text(self, translate(text))
    QComboBox.findText = lambda self, text, *args: original_find_text(self, translate(text), *args)
    ui_filter = _KoreanUiFilter(app)
    app.installEventFilter(ui_filter)
    app._korean_ui_filter = ui_filter
    app._korean_ui_installed = True


if __name__ == "__main__":
    assert translate("Open CLI") == "CLI 열기"
    assert translate("3/5 ready") == "3/5 사용 가능"
    assert translate("Auto Refresh · Off") == "자동 새로고침 · 꺼짐"
    identity_error = (
        "Claude Account 2 needs a Claude Code identity before Desktop login can be captured safely. "
        r"Run Claude Login/Status first for C:\Accounts\Claude2, then try Desktop Login again."
    )
    assert "로그인 → 상태 확인" in translate(identity_error)
    vscode_success = (
        "Applied Claude Account 1 to new Claude conversations in VS Code.\n"
        "Keep the VS Code window open, start a new Claude conversation, then use /resume if needed."
    )
    assert "VS Code 창은 그대로" in translate(vscode_success)
    assert translate("Opened Claude Code login for Claude Account 2.").startswith("Claude Account 2 계정")
    assert translate("02\nModels") == "02\n모델"
    assert source_text(translate("Weekly left")) == "Weekly left"
    from PySide6.QtWidgets import QApplication
    check_app = QApplication.instance() or QApplication([])
    install(check_app)
    check_combo = QComboBox()
    check_combo.addItems(["Manual", "Weekly left"])
    check_combo.setCurrentText("Weekly left")
    assert check_combo.currentText() == "Weekly left"
    model_index = check_combo.model().index(check_combo.currentIndex(), 0)
    assert check_combo.model().data(model_index) == "주간 잔여량"
    print("Korean UI translation checks passed")
