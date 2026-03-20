# -*- coding: utf-8 -*-
"""
DoraSkinWeightTools Python Edition v4.2.0
Based on DoraSkinWeightImpExp.mel v3.8.1 by DoraYuki
Maya 2018-2025 (Python 2.7 / 3.x)
"""
from __future__ import print_function, division, unicode_literals, absolute_import
import sys, os, math, time

PY2 = sys.version_info[0] == 2
if PY2:
    string_types = (str, unicode)
    range = xrange
else:
    string_types = (str,)

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma

VERSION = "4.2.0"
DSW_FORMAT_HEADER = "DoraYuki Skin Weight Format 3.00"

# ============================================================================
# i18n
# ============================================================================
_LANG = "en"

_S = {
    "win_title":        {"en":"Dora SkinWeight Py v{0}", "ja":"Dora SkinWeight Py v{0}"},
    "lang_label":       {"en":"Language :", "ja":"Language /\u8a00\u8a9e:"},
    "how_to_use":       {"en":"How to Use", "ja":"How to Use"},
    "tab_import":       {"en":"Import", "ja":"\u30a4\u30f3\u30dd\u30fc\u30c8"},
    "tab_export":       {"en":"Export", "ja":"\u30a8\u30af\u30b9\u30dd\u30fc\u30c8"},
    "tab_body_fit":     {"en":"Body Fit (BETA)", "ja":"\u4f53\u578b\u5408\u308f\u305b (BETA)"},
    "tab_check":        {"en":"Data Check", "ja":"\u30c7\u30fc\u30bf\u30c1\u30a7\u30c3\u30af"},
    "dsw_list":         {"en":"DSW List", "ja":"DSW \u30ea\u30b9\u30c8"},
    "import_mode":      {"en":"Import Mode", "ja":"\u30a4\u30f3\u30dd\u30fc\u30c8\u30e2\u30fc\u30c9"},
    "vertex_order":     {"en":"Vertex Order", "ja":"\u9802\u70b9\u756a\u53f7\u9806"},
    "xyz_position":     {"en":"XYZ Position", "ja":"XYZ \u5ea7\u6a19"},
    "uv_position":      {"en":"UV Position", "ja":"UV \u5ea7\u6a19"},
    "accuracy":         {"en":"Accuracy", "ja":"\u7cbe\u5ea6"},
    "interpolate":      {"en":"Interpolate", "ja":"\u88dc\u9593"},
    "bind_skin":        {"en":"Bind Skin", "ja":"\u30d0\u30a4\u30f3\u30c9\u30b9\u30ad\u30f3"},
    "edit_jointmap":    {"en":"Edit JointMap", "ja":"\u30b8\u30e7\u30a4\u30f3\u30c8\u30de\u30c3\u30d7\u7de8\u96c6"},
    "import_dsw":       {"en":"Import DSW", "ja":"DSW \u30a4\u30f3\u30dd\u30fc\u30c8"},
    "vtx_paste":        {"en":"Vertex Paste (Selected Vertices Only)",
                         "ja":"\u9802\u70b9\u30da\u30fc\u30b9\u30c8\uff08\u9078\u629e\u9802\u70b9\u306e\u307f\uff09"},
    "export_dsw_name":  {"en":"Export DSW Name", "ja":"\u30a8\u30af\u30b9\u30dd\u30fc\u30c8DSW\u540d"},
    "export_file":      {"en":"Export DSW [File]", "ja":"DSW\u30a8\u30af\u30b9\u30dd\u30fc\u30c8 [File]"},
    "export_object":    {"en":"Export DSW [Object]", "ja":"DSW\u30a8\u30af\u30b9\u30dd\u30fc\u30c8 [Object]"},
    "delete_dsw":       {"en":"Delete Selected DSW", "ja":"\u9078\u629eDSW\u3092\u524a\u9664"},
    "bf_title":         {"en":"Fit Skeleton A to B (BETA)",
                         "ja":"\u30b9\u30b1\u30eb\u30c8\u30f3A\u3092B\u306b\u5408\u308f\u305b (BETA)"},
    "bf_source":        {"en":"A: Source skeleton (joint root):",
                         "ja":"A: \u30bd\u30fc\u30b9\u30b9\u30b1\u30eb\u30c8\u30f3\uff08\u30b8\u30e7\u30a4\u30f3\u30c8\u30eb\u30fc\u30c8\uff09:"},
    "bf_target":        {"en":"B: Target skeleton (joint root):",
                         "ja":"B: \u30bf\u30fc\u30b2\u30c3\u30c8\u30b9\u30b1\u30eb\u30c8\u30f3\uff08\u30b8\u30e7\u30a4\u30f3\u30c8\u30eb\u30fc\u30c8\uff09:"},
    "bf_set_selected":  {"en":"< Set Selected", "ja":"< \u9078\u629e\u3092\u30bb\u30c3\u30c8"},
    "bf_fit":           {"en":"Fit Joints (A -> B)", "ja":"\u30b8\u30e7\u30a4\u30f3\u30c8\u3092\u5408\u308f\u305b (A \u2192 B)"},
    "bf_reset":         {"en":"GoToBindPose", "ja":"GoToBindPose"},
    "bf_help":{"en":"1. Set A (source joint root)\n2. Set B (target joint root)\n3. [Fit Joints] matches by name\n   Unmatched joints are skipped\n4. [Reset Joints] to restore",
               "ja":"1. A(\u30bd\u30fc\u30b9\u306e\u30b8\u30e7\u30a4\u30f3\u30c8\u30eb\u30fc\u30c8)\u3092\u30bb\u30c3\u30c8\n2. B(\u30bf\u30fc\u30b2\u30c3\u30c8\u306e\u30b8\u30e7\u30a4\u30f3\u30c8\u30eb\u30fc\u30c8)\u3092\u30bb\u30c3\u30c8\n3. [\u30b8\u30e7\u30a4\u30f3\u30c8\u3092\u5408\u308f\u305b]\u3067\u540d\u524d\u3067\u30de\u30c3\u30c1\n   \u4e00\u81f4\u3057\u306a\u3044\u9aa8\u306f\u30b9\u30ad\u30c3\u30d7\n4. [\u30ea\u30bb\u30c3\u30c8]\u3067\u5143\u306b\u623b\u3059"},
    "create_set":       {"en":"Create Set SkinJoint", "ja":"\u30b9\u30ad\u30f3\u30b8\u30e7\u30a4\u30f3\u30c8\u30bb\u30c3\u30c8\u4f5c\u6210"},
    "decimal_title":    {"en":"--- Weight Decimal Check ---", "ja":"--- \u30a6\u30a7\u30a4\u30c8\u5c0f\u6570\u70b9\u30c1\u30a7\u30c3\u30af ---"},
    "decimal_desc":     {"en":"Find weights finer than the unit below", "ja":"\u6307\u5b9a\u5358\u4f4d\u3088\u308a\u7d30\u304b\u3044\u30a6\u30a7\u30a4\u30c8\u3092\u691c\u51fa"},
    "check_digit":      {"en":"Check", "ja":"\u30c1\u30a7\u30c3\u30af"},
    "clean_digit":      {"en":"Clean (Round)", "ja":"\u30af\u30ea\u30fc\u30f3\uff08\u4e38\u3081\uff09"},
    "digit_unit":       {"en":"Unit", "ja":"\u5358\u4f4d"},
    "inf_title":        {"en":"--- Influence Count Check ---", "ja":"--- \u30a4\u30f3\u30d5\u30eb\u30a8\u30f3\u30b9\u6570\u30c1\u30a7\u30c3\u30af ---"},
    "inf_desc":         {"en":"Find vertices influenced by more than N joints", "ja":"N\u672c\u3088\u308a\u591a\u3044\u30b8\u30e7\u30a4\u30f3\u30c8\u306e\u5f71\u97ff\u3092\u53d7\u3051\u308b\u9802\u70b9\u3092\u691c\u51fa"},
    "inf_max":          {"en":"Max", "ja":"\u6700\u5927\u6570"},
    "check_inf":        {"en":"Check", "ja":"\u30c1\u30a7\u30c3\u30af"},
    "check_samepos":    {"en":"Check SamePosition Weight", "ja":"\u540c\u4f4d\u7f6e\u30a6\u30a7\u30a4\u30c8\u30c1\u30a7\u30c3\u30af"},
    "jne_title":        {"en":"Edit JointMap", "ja":"\u30b8\u30e7\u30a4\u30f3\u30c8\u30de\u30c3\u30d7\u7de8\u96c6"},
    "jne_joint_name":   {"en":"Joint Name", "ja":"\u30b8\u30e7\u30a4\u30f3\u30c8\u540d"},
    "jne_set":          {"en":"Set JointName", "ja":"\u30b8\u30e7\u30a4\u30f3\u30c8\u540d\u30bb\u30c3\u30c8"},
    "jne_search":       {"en":"Search", "ja":"\u691c\u7d22"},
    "jne_replace":      {"en":"Replace", "ja":"\u7f6e\u63db"},
    "jne_substitution": {"en":"Substitution", "ja":"\u7f6e\u63db\u5b9f\u884c"},
    "jne_prefix":       {"en":"Prefix", "ja":"\u63a5\u982d\u8f9e"},
    "jne_suffix":       {"en":"Suffix", "ja":"\u63a5\u5c3e\u8f9e"},
    "jne_add_ps":       {"en":"Add Prefix/Suffix", "ja":"\u63a5\u982d\u8f9e/\u63a5\u5c3e\u8f9e\u8ffd\u52a0"},
    "jne_reset":        {"en":"Reset", "ja":"\u30ea\u30bb\u30c3\u30c8"},
    "warn_no_dsw":      {"en":"No DSW selected.", "ja":"DSW\u304c\u9078\u629e\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002"},
    "warn_no_name":     {"en":"Please enter an export name.", "ja":"\u30a8\u30af\u30b9\u30dd\u30fc\u30c8\u540d\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002"},
    "warn_no_sel":      {"en":"Nothing selected.", "ja":"\u4f55\u3082\u9078\u629e\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u3002"},
    "warn_set_both":    {"en":"Please set both Source and Target.", "ja":"\u30bd\u30fc\u30b9\u3068\u30bf\u30fc\u30b2\u30c3\u30c8\u306e\u4e21\u65b9\u3092\u30bb\u30c3\u30c8\u3057\u3066\u304f\u3060\u3055\u3044\u3002"},
    "warn_delete_confirm":{"en":"Delete selected DSW?\n{0}", "ja":"\u9078\u629e\u3057\u305fDSW\u3092\u524a\u9664\u3057\u307e\u3059\u304b\uff1f\n{0}"},
    "report_title":     {"en":"Operation Report", "ja":"\u51e6\u7406\u30ec\u30dd\u30fc\u30c8"},
    "htu_title":        {"en":"How to Use", "ja":"\u4f7f\u3044\u65b9"},
    "htu_content":{
        "en":(
            "=== DoraSkinWeight Tools Py v{ver} ===\n\n"
            "--- EXPORT ---\n"
            "1. Select skinned mesh.\n"
            "2. [Export] tab > enter name > [File] or [Object].\n"
            "   [File]: saves to <workspace>/dsw/\n"
            "   [Object]: stores in scene node.\n"
            "3. Use [Delete Selected DSW] to remove entries.\n\n"
            "--- IMPORT ---\n"
            "1. Select skinned mesh.\n"
            "2. [Import] tab > select DSW > choose mode.\n"
            "   XYZ Position (default): world-space match.\n"
            "   Vertex Order: same topology.\n"
            "   UV Position: UV-based match.\n"
            "3. [Import DSW] to apply.\n\n"
            "--- VERTEX PASTE ---\n"
            "Paste weights ONLY to selected vertices.\n"
            "1. Export source weights.\n"
            "2. Select vertices on target mesh.\n"
            "3. Select DSW, click [Vertex Paste].\n\n"
            "--- BODY TRANSFER ---\n"
            "1. [Body Transfer] tab.\n"
            "2. Set Body A (source) and Body B (target).\n"
            "3. Click [Transfer Weights (A->B)].\n\n"
            "--- DATA CHECK ---\n"
            "- Weight Precision: finds weights finer than threshold (default 0.01).\n"
            "- SamePosition: finds overlapping verts with different weights.\n"
            "- Create SkinJoint Set: makes a joint selection set.\n\n"
            "--- TIPS ---\n"
            "- Maya 2018-2025 compatible.\n"
            "- DSW format compatible with original MEL version.\n"),
        "ja":(
            "=== DoraSkinWeight Tools Py v{ver} ===\n\n"
            "--- \u30a8\u30af\u30b9\u30dd\u30fc\u30c8 ---\n"
            "1. \u30b9\u30ad\u30f3\u6e08\u307f\u30e1\u30c3\u30b7\u30e5\u3092\u9078\u629e\u3002\n"
            "2. [\u30a8\u30af\u30b9\u30dd\u30fc\u30c8]\u30bf\u30d6 > \u540d\u524d\u5165\u529b > [File]\u307e\u305f\u306f[Object]\u3002\n"
            "   [File]: <workspace>/dsw/ \u306b\u4fdd\u5b58\u3002\n"
            "   [Object]: \u30b7\u30fc\u30f3\u30ce\u30fc\u30c9\u306b\u4fdd\u5b58\u3002\n"
            "3. [\u9078\u629eDSW\u3092\u524a\u9664]\u3067\u4e0d\u8981\u306a\u30c7\u30fc\u30bf\u3092\u524a\u9664\u3002\n\n"
            "--- \u30a4\u30f3\u30dd\u30fc\u30c8 ---\n"
            "1. \u30b9\u30ad\u30f3\u6e08\u307f\u30e1\u30c3\u30b7\u30e5\u3092\u9078\u629e\u3002\n"
            "2. [\u30a4\u30f3\u30dd\u30fc\u30c8]\u30bf\u30d6 > DSW\u9078\u629e > \u30e2\u30fc\u30c9\u9078\u629e\u3002\n"
            "   XYZ\u5ea7\u6a19(\u30c7\u30d5\u30a9\u30eb\u30c8): \u30ef\u30fc\u30eb\u30c9\u5ea7\u6a19\u3067\u30de\u30c3\u30c1\u3002\n"
            "   \u9802\u70b9\u756a\u53f7\u9806: \u540c\u4e00\u30c8\u30dd\u30ed\u30b8\u30fc\u7528\u3002\n"
            "   UV\u5ea7\u6a19: UV\u3067\u30de\u30c3\u30c1\u3002\n"
            "3. [DSW\u30a4\u30f3\u30dd\u30fc\u30c8]\u3067\u9069\u7528\u3002\n\n"
            "--- \u9802\u70b9\u30da\u30fc\u30b9\u30c8 ---\n"
            "\u9078\u629e\u9802\u70b9\u306e\u307f\u306b\u30a6\u30a7\u30a4\u30c8\u3092\u30da\u30fc\u30b9\u30c8\u3002\n"
            "1. \u30bd\u30fc\u30b9\u306e\u30a6\u30a7\u30a4\u30c8\u3092\u30a8\u30af\u30b9\u30dd\u30fc\u30c8\u3002\n"
            "2. \u30bf\u30fc\u30b2\u30c3\u30c8\u306e\u9802\u70b9\u3092\u9078\u629e\u3002\n"
            "3. DSW\u3092\u9078\u629e\u3057\u3001[\u9802\u70b9\u30da\u30fc\u30b9\u30c8]\u3002\n\n"
            "--- \u4f53\u578b\u8ee2\u9001 ---\n"
            "1. [\u4f53\u578b\u8ee2\u9001]\u30bf\u30d6\u3002\n"
            "2. \u4f53\u578bA(\u30bd\u30fc\u30b9)\u3068\u4f53\u578bB(\u30bf\u30fc\u30b2\u30c3\u30c8)\u3092\u30bb\u30c3\u30c8\u3002\n"
            "3. [\u30a6\u30a7\u30a4\u30c8\u8ee2\u9001(A\u2192B)]\u3002\n\n"
            "--- \u30c7\u30fc\u30bf\u30c1\u30a7\u30c3\u30af ---\n"
            "- \u30a6\u30a7\u30a4\u30c8\u7cbe\u5ea6: \u95be\u5024(\u30c7\u30d5\u30a9\u30eb\u30c80.01)\u3088\u308a\u7d30\u304b\u3044\u30a6\u30a7\u30a4\u30c8\u3092\u691c\u51fa\u3002\n"
            "- \u540c\u4f4d\u7f6e\u30c1\u30a7\u30c3\u30af: \u540c\u3058\u4f4d\u7f6e\u3067\u30a6\u30a7\u30a4\u30c8\u304c\u7570\u306a\u308b\u9802\u70b9\u3092\u691c\u51fa\u3002\n"
            "- \u30b9\u30ad\u30f3\u30b8\u30e7\u30a4\u30f3\u30c8\u30bb\u30c3\u30c8\u4f5c\u6210\u3002\n\n"
            "--- \u30d2\u30f3\u30c8 ---\n"
            "- Maya 2018\uff5e2025\u5bfe\u5fdc\u3002\n"
            "- DSW\u30d5\u30a9\u30fc\u30de\u30c3\u30c8\u306f\u30aa\u30ea\u30b8\u30ca\u30ebMEL\u7248\u3068\u4e92\u63db\u3002\n"),
    },
}

def tr(key, **kw):
    e = _S.get(key, {})
    t = e.get(_LANG, e.get("en", key))
    if kw: t = t.format(**kw)
    return t

def set_language(lang):
    global _LANG; _LANG = lang


# ============================================================================
# Progress Window (custom, in-tool)
# ============================================================================

_PROG_WIN = "DSWPy_ProgressWindow"

def progress_start(title, max_val):
    if cmds.window(_PROG_WIN, exists=True): cmds.deleteUI(_PROG_WIN)
    cmds.window(_PROG_WIN, title=title, wh=(320, 70), sizeable=False, tlb=True)
    cmds.columnLayout(adj=True)
    cmds.text("DSWPy_ProgLabel", label=title, h=20, al="center")
    cmds.progressBar("DSWPy_ProgBar", maxValue=max(max_val, 1), width=300, h=22)
    cmds.showWindow(_PROG_WIN)
    cmds.refresh(force=True)

def progress_update(step=1, label=None):
    if cmds.progressBar("DSWPy_ProgBar", exists=True):
        cmds.progressBar("DSWPy_ProgBar", e=True, step=step)
    if label and cmds.text("DSWPy_ProgLabel", exists=True):
        cmds.text("DSWPy_ProgLabel", e=True, label=label)
    cmds.refresh(force=True)

def progress_end():
    if cmds.window(_PROG_WIN, exists=True): cmds.deleteUI(_PROG_WIN)


# ============================================================================
# Status Line (in-tool message display)
# ============================================================================

_STATUS_CTRL = "DSWPy_StatusText"

def show_status(msg, is_error=False):
    """Show message in the tool's status area and print to script editor."""
    print(msg)
    if cmds.text(_STATUS_CTRL, exists=True):
        color = (0.9, 0.3, 0.3) if is_error else (0.7, 0.9, 0.7)
        cmds.text(_STATUS_CTRL, e=True, label=msg, bgc=color)


def show_check_result(title, found_count, total_count, details=""):
    """Show a dialog with check results."""
    if found_count == 0:
        icon = "information"
        msg = "OK - No problems found.\n\nChecked: {0} vertices".format(total_count)
        if details:
            msg += "\n" + details
    else:
        icon = "warning"
        msg = "Found {0} problem vertices.\n\nChecked: {1} vertices\n{0} vertices selected.".format(
            found_count, total_count)
        if details:
            msg += "\n" + details
    cmds.confirmDialog(title=title, message=msg, button=["OK"], icon=icon)


# ============================================================================
# Report Logger
# ============================================================================

class Report(object):
    """Collects log lines during an operation and shows them in a report window."""
    _WIN = "DSWPy_ReportWin"

    def __init__(self, title=""):
        self.title = title
        self.lines = []
        self.errors = []
        self.start_time = time.time()

    def log(self, msg):
        self.lines.append(msg)
        print("[Report] " + msg)

    def warn(self, msg):
        self.lines.append("[WARN] " + msg)
        print("[Report][WARN] " + msg)

    def error(self, msg):
        self.errors.append(msg)
        self.lines.append("[ERROR] " + msg)
        print("[Report][ERROR] " + msg)

    def summary(self):
        elapsed = time.time() - self.start_time
        self.lines.append("")
        self.lines.append("=== Summary ===")
        self.lines.append("Time: {0:.2f}s".format(elapsed))
        if self.errors:
            self.lines.append("Errors: {0}".format(len(self.errors)))
            for e in self.errors:
                self.lines.append("  - " + e)
        else:
            self.lines.append("Completed successfully.")
        return "\n".join(self.lines)

    def show_window(self):
        """Show report in a scrollable window."""
        if cmds.window(self._WIN, exists=True):
            cmds.deleteUI(self._WIN)
        cmds.window(self._WIN, title=tr("report_title") + " - " + self.title,
                    wh=(500, 400), s=True)
        cmds.columnLayout(adj=True)
        cmds.scrollField(text=self.summary(), ed=False, ww=True, h=360, fn="fixedWidthFont")
        cmds.setParent("..")
        cmds.showWindow(self._WIN)


# ============================================================================
# Utility Functions
# ============================================================================

def vtx_to_uv(vtx):
    try:
        uv_list = cmds.polyListComponentConversion(vtx, fv=True, tuv=True)
        if uv_list:
            return uv_list[0].replace(".map", ".uv") if ".map" in uv_list[0] else uv_list[0]
    except Exception: pass
    return ""

def get_shape(obj):
    """Get non-intermediate mesh shape from obj. Works with transforms, groups, references."""
    def _is_intermediate(node):
        try: return cmds.getAttr(node + ".intermediateObject")
        except Exception: return False

    # Direct children shapes (most common case)
    shapes = cmds.listRelatives(obj, shapes=True, fullPath=True, type="mesh") or []
    for s in shapes:
        if not _is_intermediate(s): return s
    # listHistory fallback (for direct transform with deformers)
    h = cmds.listHistory(obj) or []
    for node in cmds.ls(h, type="mesh") or []:
        if not _is_intermediate(node): return node
    # Group node: search descendants for skinned mesh
    descs = cmds.listRelatives(obj, allDescendents=True, fullPath=True, type="mesh") or []
    for d in descs:
        if _is_intermediate(d): continue
        if get_skin_cluster(d): return d
    # Any non-intermediate descendant mesh
    for d in descs:
        if not _is_intermediate(d): return d
    return ""

def get_skin_cluster(mesh_shape):
    h = cmds.listHistory(mesh_shape)
    if h:
        s = cmds.ls(h, type="skinCluster")
        if s: return s[0]
    return ""

def simple_obj_name(n): return n.split("|")[-1]

def check_overlaps(nl):
    from collections import Counter
    c = Counter(nl); d = {k:v for k,v in c.items() if v>1}
    if not d: return ""
    return ", ".join(["{0}({1})".format(k,v) for k,v in d.items()])

def ext_check(n, ext):
    if not n.lower().endswith(ext.lower()): return n+ext
    return n

def get_joint_list_from_sc(sc):
    return [simple_obj_name(j) for j in (cmds.listConnections(sc+".matrix", type="joint") or [])]

def get_dsw_directory():
    return os.path.join(cmds.workspace(q=True, fn=True), "dsw")


# ============================================================================
# Spatial Index
# ============================================================================

class SpatialIndex(object):
    def __init__(self):
        self.vtx_positions=[]; self.uv_positions=[]
        self._vb={}; self._ub={}
    def clear(self):
        self.vtx_positions=[]; self.uv_positions=[]; self._vb={}; self._ub={}
    @staticmethod
    def _vk(p): return (int(math.floor(p[0]*0.2)),int(math.floor(p[1]*0.2)),int(math.floor(p[2]*0.2)))
    @staticmethod
    def _uk(p): return (int(math.floor(p[0]*20)),int(math.floor(p[1]*20)),0)
    def build_from_shape(self, shape):
        self.clear()
        vc = cmds.polyEvaluate(shape, vertex=True)
        sel=om.MSelectionList(); sel.add(shape)
        dp=om.MDagPath(); sel.getDagPath(0,dp)
        fm=om.MFnMesh(dp); pts=om.MPointArray(); fm.getPoints(pts,om.MSpace.kWorld)
        for i in range(pts.length()):
            p=(pts[i].x,pts[i].y,pts[i].z); self.vtx_positions.append(p)
            bk=self._vk(p); self._vb.setdefault(bk,[]).append(i)
        for i in range(vc):
            vn="{0}.vtx[{1}]".format(shape,i); un=vtx_to_uv(vn); u,v=0.0,0.0
            if un:
                try:
                    uv=cmds.getAttr(un)
                    if isinstance(uv,list) and uv:
                        if isinstance(uv[0],tuple): u,v=uv[0][0],uv[0][1]
                        else: u,v=uv[0],uv[1]
                except Exception: pass
            self.uv_positions.append((u,v))
            bk=self._uk((u,v)); self._ub.setdefault(bk,[]).append(i)
    def get_cand_vtx(self, pos, r=1):
        c=self._vk(pos); res=[]
        for dx in range(-r,r+1):
            for dy in range(-r,r+1):
                for dz in range(-r,r+1):
                    bk=(c[0]+dx,c[1]+dy,c[2]+dz)
                    if bk in self._vb: res.extend(self._vb[bk])
        return res
    def get_cand_uv(self, pos, r=1):
        c=self._uk(pos); res=[]
        for dx in range(-r,r+1):
            for dy in range(-r,r+1):
                bk=(c[0]+dx,c[1]+dy,0)
                if bk in self._ub: res.extend(self._ub[bk])
        return res
    def find_nearest(self, pos, mode="Vtx", used=None, md=0.001):
        cands = self.get_cand_vtx(pos) if mode=="Vtx" else self.get_cand_uv(pos)
        ps = self.vtx_positions if mode=="Vtx" else self.uv_positions
        bi,bd=-1,md
        for idx in cands:
            if used and used[idx]: continue
            p=ps[idx]
            if mode=="Vtx": d=math.sqrt((pos[0]-p[0])**2+(pos[1]-p[1])**2+(pos[2]-p[2])**2)
            else: d=math.sqrt((pos[0]-p[0])**2+(pos[1]-p[1])**2)
            if d<=bd: bd=d; bi=idx
        return bi


# ============================================================================
# DSW Read/Write
# ============================================================================

def read_dsw(dsw_name):
    parts=dsw_name.split(" ",1); mode=parts[0]; name=parts[1] if len(parts)>1 else ""
    dl=[]
    if mode=="[File]":
        fp=os.path.join(get_dsw_directory(),name)
        if not os.path.isfile(fp): show_status("Read DSW File Error: "+fp, True); return []
        with open(fp,"r") as f: c=f.read()
        dl=[l for l in c.replace("\r\n","\n").replace("\r","\n").split("\n") if l]
    elif mode=="[Object]":
        op="dsw|"+name
        if cmds.objExists(op+".dsw_0"):
            i=0
            while cmds.objExists("{0}.dsw_{1}".format(op,i)):
                dl.append(cmds.getAttr("{0}.dsw_{1}".format(op,i))); i+=1
        else:
            np=op+".notes"
            if not cmds.objExists(np): show_status("Read DSW Object Error",True); return []
            c=cmds.getAttr(np)
            dl=[l for l in c.replace("\r\n","\n").replace("\r","\n").split("\n") if l]
    if len(dl)<3: show_status("No DSW Data",True); return []
    if dl[0]!=DSW_FORMAT_HEADER: show_status("Not DSW Format 3.00",True); return []
    if not dl[1]: show_status("No DSW JointData",True); return []
    return dl

def write_dsw_file(fp, lines):
    d=os.path.dirname(fp)
    if not os.path.exists(d): os.makedirs(d)
    with open(fp,"w") as f: f.write("\n".join(lines))

def delete_dsw(dsw_name):
    """Delete a DSW source (file or scene object)."""
    parts=dsw_name.split(" ",1); mode=parts[0]; name=parts[1] if len(parts)>1 else ""
    if mode=="[File]":
        fp=os.path.join(get_dsw_directory(),name)
        if os.path.isfile(fp): os.remove(fp); show_status("Deleted: "+fp)
    elif mode=="[Object]":
        op="dsw|"+name
        if cmds.objExists(op): cmds.delete(op); show_status("Deleted: "+op)


# ============================================================================
# OpenMaya Bulk Weight Helpers
# ============================================================================

def _get_skin_fn(sc_name):
    """Get MFnSkinCluster from skinCluster name."""
    sel = om.MSelectionList(); sel.add(sc_name)
    obj = om.MObject(); sel.getDependNode(0, obj)
    return oma.MFnSkinCluster(obj)

def _get_dag_path(node_name):
    """Get MDagPath from node name."""
    sel = om.MSelectionList(); sel.add(node_name)
    dp = om.MDagPath(); sel.getDagPath(0, dp)
    return dp

def _bulk_get_weights(sc_name, shape_name, vc, num_joints):
    """Get all skin weights as a flat list using OpenMaya API.
    Returns list of lists: weights[vtx_index] = [w0, w1, w2, ...]"""
    try:
        fn = _get_skin_fn(sc_name)
        dp = _get_dag_path(shape_name)
        # Get all vertex components
        fn_comp = om.MFnSingleIndexedComponent()
        comp = fn_comp.create(om.MFn.kMeshVertComponent)
        for i in range(vc):
            fn_comp.addElement(i)
        weights = om.MDoubleArray()
        util = om.MScriptUtil()
        util.createFromInt(0)
        inf_count_ptr = util.asUintPtr()
        fn.getWeights(dp, comp, weights, inf_count_ptr)
        inf_count = om.MScriptUtil.getUint(inf_count_ptr)
        # Convert flat array to per-vertex lists
        result = []
        for i in range(vc):
            vw = []
            for j in range(inf_count):
                vw.append(weights[i * inf_count + j])
            result.append(vw)
        return result
    except Exception as e:
        print("[BulkWeights] API failed, falling back to cmds: {0}".format(e))
        return None

def _bulk_get_positions(shape_name, vc):
    """Get all vertex world positions using OpenMaya API.
    Returns list of (x,y,z) tuples."""
    try:
        dp = _get_dag_path(shape_name)
        fn = om.MFnMesh(dp)
        pts = om.MPointArray()
        fn.getPoints(pts, om.MSpace.kWorld)
        result = []
        for i in range(pts.length()):
            result.append((pts[i].x, pts[i].y, pts[i].z))
        return result
    except Exception as e:
        print("[BulkPositions] API failed: {0}".format(e))
        return None

def _bulk_get_uvs(shape_name, vc):
    """Get first UV coordinate per vertex.
    Returns list of (u,v) tuples (0,0 if no UV)."""
    try:
        result = [(0.0, 0.0)] * vc
        it_sel = om.MSelectionList()
        it_sel.add(shape_name)
        dp = om.MDagPath()
        it_sel.getDagPath(0, dp)
        it = om.MItMeshVertex(dp)
        util_u = om.MScriptUtil(); util_u.createFromDouble(0.0)
        util_v = om.MScriptUtil(); util_v.createFromDouble(0.0)
        while not it.isDone():
            idx = it.index()
            uv_u = om.MScriptUtil(); uv_u.createFromDouble(0.0); ptr_u = uv_u.asFloatPtr()
            uv_v = om.MScriptUtil(); uv_v.createFromDouble(0.0); ptr_v = uv_v.asFloatPtr()
            try:
                it.getUV(ptr_u, ptr_v)
                result[idx] = (om.MScriptUtil.getFloat(ptr_u), om.MScriptUtil.getFloat(ptr_v))
            except Exception:
                pass
            it.next()
        return result
    except Exception as e:
        print("[BulkUVs] API failed: {0}".format(e))
        return None


# ============================================================================
# Export
# ============================================================================

def dsw_export(dsw_name):
    st=time.time()
    sl=cmds.filterExpand(sm=12) or []
    mode=0
    if not sl:
        sl=cmds.filterExpand(sm=31) or []
        if sl: sl=cmds.ls(sl,fl=True)
        if not sl: show_status("No skinned mesh selected",True); return 0
        mode=2
    else: mode=1
    shape=get_shape(sl[0]); sc=get_skin_cluster(shape)
    if not sc: show_status("No skinCluster found",True); return 0
    jl=get_joint_list_from_sc(sc)
    ov=check_overlaps(jl)
    if ov: show_status("JointName Overlaps: "+ov,True); return 0
    vc=cmds.polyEvaluate(shape,vertex=True) if mode==1 else len(sl)
    el=[DSW_FORMAT_HEADER, ",".join(jl)]

    # Bulk fetch all data via OpenMaya
    all_weights = None
    all_pos = None
    all_uvs = None
    if mode == 1:
        all_weights = _bulk_get_weights(sc, shape, vc, len(jl))
        all_pos = _bulk_get_positions(shape, vc)
        all_uvs = _bulk_get_uvs(shape, vc)

    progress_start("Exporting...", vc)
    nuv = 0
    for i in range(vc):
        if i % 500 == 0:
            progress_update(min(500, vc - i), "Export {0}/{1}".format(i, vc))
        wv="{0}.vtx[{1}]".format(shape,i) if mode==1 else sl[i]

        # Weights
        if all_weights and i < len(all_weights):
            wl = all_weights[i]
        else:
            wl = cmds.skinPercent(sc, wv, q=True, v=True)
        ws = ",".join([str(w) for w in wl])

        # Position
        if all_pos and i < len(all_pos):
            wp = all_pos[i]
        else:
            wp = cmds.pointPosition(wv, w=True)
        ps = "{0},{1},{2}".format(wp[0], wp[1], wp[2])

        # UV
        u, v = 0.0, 0.0
        if all_uvs and i < len(all_uvs):
            u, v = all_uvs[i]
        else:
            un = vtx_to_uv(wv)
            if un:
                try:
                    uv = cmds.getAttr(un)
                    if isinstance(uv, list) and uv:
                        if isinstance(uv[0], tuple): u, v = uv[0][0], uv[0][1]
                        else: u, v = uv[0], uv[1]
                except Exception: nuv += 1
            else: nuv += 1

        el.append("{0}|{1}|{2},{3}".format(ws, ps, u, v))

    pts=dsw_name.split(" ",1); em,enp=pts[0],pts[1] if len(pts)>1 else dsw_name; ep=""
    if em=="[File]":
        fp=os.path.join(get_dsw_directory(),ext_check(enp,".dsw")); write_dsw_file(fp,el); ep=fp
    elif em=="[Object]":
        on=os.path.splitext(enp)[0]; op="dsw|"+on
        if not cmds.objExists("dsw"): cmds.group(empty=True,n="dsw")
        if cmds.objExists(op): cmds.delete(op)
        cmds.group(empty=True,n=on,p="dsw")
        for i,ln in enumerate(el):
            cmds.addAttr(op,ln="dsw_{0}".format(i),dt="string")
            cmds.setAttr("{0}.dsw_{1}".format(op,i),ln,type="string")
        ep=op; cmds.select(sl,r=True)
    progress_end()
    t=time.time()-st
    show_status("Export: {0} vtx  {1:.2f}s".format(vc, t))
    # Show detail in report window
    r = Report("Export")
    r.log("DSW: {0}".format(ep))
    r.log("Shape: {0}".format(shape))
    r.log("Vertices: {0}".format(vc))
    r.log("Joints: {0}".format(len(jl)))
    r.log("Time: {0:.2f}s".format(t))
    r.show_window()
    return 1


# ============================================================================
# Import
# ============================================================================

def _build_wp(tj, ei, ui, dj, ws, min_w=0.01):
    w=ws.split(","); pm=[]
    for idx in ei:
        jn=tj[idx]
        for ji,d in enumerate(dj):
            if jn==d and ji<len(w): pm.append((jn,float(w[ji]))); break
    for idx in ui: pm.append((tj[idx],0.0))
    return _quantize_weight_params(pm, min_w)

def _wt_copy(si, di, sc, sh, min_w=0.01):
    j=get_joint_list_from_sc(sc)
    wl=cmds.skinPercent(sc,"{0}.vtx[{1}]".format(sh,si),q=True,v=True)
    tv=[(j[i],wl[i]) for i in range(min(len(j),len(wl)))]
    tv=_quantize_weight_params(tv, min_w)
    if tv: cmds.skinPercent(sc,"{0}.vtx[{1}]".format(sh,di),r=False,transformValue=tv)

def _bind_dsw(obj, dn, jm=None):
    sh=get_shape(obj); sc=get_skin_cluster(sh)
    if sc: cmds.skinCluster(sh,e=True,ub=True)
    dl=read_dsw(dn)
    if not dl: return 0
    jl=[simple_obj_name(j) for j in dl[1].split(",")]
    if jm: jl=[jm.get(j,j) for j in jl]
    cmds.select(jl+[obj],r=True); cmds.skinCluster(tsb=True,n="skinCluster_"+obj); return 1

def dsw_import(dn, im=0, interp=False, imode=1, acc=0.001, bs=False, jm=None, min_w=0.01, show_report=False):
    rpt = Report("Import") if show_report else None
    st=time.time()
    if not dn: return 0
    sl=cmds.filterExpand(sm=12) or []
    if not sl: show_status("No skinned mesh selected",True); return 0
    sh=get_shape(sl[0])
    if rpt: rpt.log("Target: {0}  Shape: {1}".format(sl[0], sh))
    if rpt: rpt.log("DSW: {0}  Mode: {1}  Accuracy: {2}  MinWeight: {3}".format(
        dn, ["VtxOrder","XYZ","UV"][im], acc, min_w))
    if bs: _bind_dsw(sl[0],dn,jm)
    sc=get_skin_cluster(sh)
    if not sc: show_status("No skinCluster found",True); return 0
    tj=get_joint_list_from_sc(sc)
    ov=check_overlaps(tj)
    if ov: show_status("Joint overlaps: "+ov,True); return 0
    dl=read_dsw(dn)
    if not dl: return 0
    vc=cmds.polyEvaluate(sh,vertex=True)
    dj=[simple_obj_name(j) for j in dl[1].split(",")]
    if jm: dj=[jm.get(j,j) for j in dj]
    ei=[s for s,t in enumerate(tj) if t in dj]
    ui=[s for s,t in enumerate(tj) if t not in dj]
    if rpt:
        rpt.log("Target joints: {0}  DSW joints: {1}".format(len(tj), len(dj)))
        rpt.log("Matched: {0}  Unknown: {1}".format(len(ei), len(ui)))
    wsf=[0]*vc; sp=SpatialIndex(); sp.build_from_shape(sh)
    progress_start("Importing...",vc)
    cmds.setAttr(sc+".normalizeWeights",0); cmds.setAttr(sc+".envelope",0)
    ds=2
    nj = len(tj)

    # Build joint index mapping: DSW joint name -> target joint index
    tj_idx = {t: i for i, t in enumerate(tj)}
    dj_to_tj = {}  # dsw joint index -> target joint index
    for di, dn_j in enumerate(dj):
        if dn_j in tj_idx:
            dj_to_tj[di] = tj_idx[dn_j]

    # Buffer: collect weights per vertex as flat array [vc * nj]
    # Initialize with current weights (bulk read)
    bulk_w = _bulk_get_weights(sc, sh, vc, nj)
    if bulk_w:
        weight_buf = []
        for vw in bulk_w:
            weight_buf.append(list(vw))
    else:
        # Fallback: zero init
        weight_buf = [[0.0] * nj for _ in range(vc)]

    def _parse_and_assign(vtx_idx, weight_str):
        """Parse DSW weight string and write into weight_buf."""
        w_vals = weight_str.split(",")
        # Zero out all
        row = [0.0] * nj
        for di, val_s in enumerate(w_vals):
            if di in dj_to_tj:
                row[dj_to_tj[di]] = float(val_s)
        # Quantize
        total = sum(row)
        if total > 0 and min_w > 0:
            places = _unit_to_places(min_w)
            for k in range(nj):
                row[k] = round(row[k], places)
                if row[k] < min_w: row[k] = 0.0
            total2 = sum(row)
            if total2 > 0:
                row = [round(w / total2, places) for w in row]
                diff = 1.0 - sum(row)
                if abs(diff) > 1e-12:
                    mi = row.index(max(row))
                    row[mi] = round(row[mi] + diff, places)
        weight_buf[vtx_idx] = row
        wsf[vtx_idx] = 1

    if im==0:
        for i in range(vc):
            if i % 500 == 0:
                progress_update(min(500, vc - i), "Import {0}/{1}".format(i, vc))
            li=ds+i
            if li>=len(dl): break
            ln=dl[li]
            if not ln: break
            if wsf[i]: continue
            p=ln.split("|")
            _parse_and_assign(i, p[0])
            # Batch same-weight vertices
            for j in range(i+1,vc):
                ji=ds+j
                if ji>=len(dl) or wsf[j]: continue
                if dl[ji].split("|")[0]==p[0]:
                    weight_buf[j] = list(weight_buf[i])
                    wsf[j]=1
    elif im in (1,2):
        r=ds
        while r<len(dl):
            if (r - ds) % 500 == 0:
                progress_update(min(500, len(dl) - r), "Import {0}/{1}".format(r-ds, len(dl)-ds))
            ln=dl[r]
            if not ln: break
            p=ln.split("|"); r+=1
            if im==1:
                xyz=p[1].split(","); pos=(float(xyz[0]),float(xyz[1]),float(xyz[2]))
                mi=sp.find_nearest(pos,"Vtx",wsf,acc)
            else:
                uv=p[2].split(","); pos=(float(uv[0]),float(uv[1]))
                mi=sp.find_nearest(pos,"UV",wsf,acc)
            if mi==-1: continue
            _parse_and_assign(mi, p[0])

    # Interpolation: copy nearest matched vertex weights
    if interp:
        for i in range(vc):
            if wsf[i]: continue
            if i % 200 == 0:
                progress_update(min(200, vc - i), "Interpolate {0}/{1}".format(i, vc))
            bi,bd=-1,float('inf')
            for j in range(vc):
                if i==j or wsf[j]!=1: continue
                if imode==1:
                    pi,pj=sp.vtx_positions[i],sp.vtx_positions[j]
                    d=(pi[0]-pj[0])**2+(pi[1]-pj[1])**2+(pi[2]-pj[2])**2
                else:
                    pi,pj=sp.uv_positions[i],sp.uv_positions[j]
                    d=(pi[0]-pj[0])**2+(pi[1]-pj[1])**2
                if d<bd: bd=d; bi=j
            if bi==-1: break
            weight_buf[i] = list(weight_buf[bi])
            wsf[i]=2

    # Bulk write all weights via OpenMaya
    progress_update(1, "Writing weights...")
    try:
        fn = _get_skin_fn(sc)
        dp = _get_dag_path(sh)
        fn_comp = om.MFnSingleIndexedComponent()
        comp = fn_comp.create(om.MFn.kMeshVertComponent)
        for i in range(vc):
            fn_comp.addElement(i)
        # Build flat MDoubleArray
        weights = om.MDoubleArray(vc * nj, 0.0)
        for i in range(vc):
            for j in range(nj):
                weights[i * nj + j] = weight_buf[i][j]
        # Influence indices
        inf_indices = om.MIntArray(nj, 0)
        for i in range(nj):
            inf_indices[i] = i
        fn.setWeights(dp, comp, inf_indices, weights, False)
    except Exception as e:
        # Fallback: write per-vertex via cmds
        print("[BulkWrite] API failed, fallback to cmds: {0}".format(e))
        for i in range(vc):
            if wsf[i] == 0: continue
            tv = [(tj[j], weight_buf[i][j]) for j in range(nj) if weight_buf[i][j] > 0]
            if tv:
                cmds.skinPercent(sc, "{0}.vtx[{1}]".format(sh, i), r=False, transformValue=tv)

    cmds.setAttr(sc+".envelope",1)
    cmds.skinPercent(sc,sh,normalize=True)
    cmds.setAttr(sc+".normalizeWeights",1)
    progress_end()
    s1,s2=wsf.count(1),wsf.count(2)
    t=time.time()-st
    show_status("Import: {0}({1}) vtx  {2:.2f}s".format(s1+s2, s2, t))
    # Always show detail in report window
    if not rpt:
        rpt = Report("Import")
    rpt.log("Shape: {0}".format(sh))
    rpt.log("DSW: {0}".format(dn))
    rpt.log("Direct match: {0}  Interpolated: {1}  Total: {2}".format(s1, s2, vc))
    rpt.log("Time: {0:.2f}s".format(t))
    rpt.show_window()
    return 1


# ============================================================================
# Vertex Paste (was Face Paste - now works on selected vertices directly)
# ============================================================================

def vertex_paste_weights(dn, im=0, acc=0.001, jm=None, min_w=0.01):
    st=time.time()
    vtx_sel = cmds.filterExpand(sm=31) or []
    face_sel = cmds.filterExpand(sm=34) or []
    if face_sel and not vtx_sel:
        vtx_sel = cmds.ls(cmds.polyListComponentConversion(face_sel, ff=True, tv=True) or [], fl=True)
    if not vtx_sel:
        show_status("No vertices or faces selected.", True); return 0
    vtx_sel = cmds.ls(vtx_sel, fl=True)
    obj = vtx_sel[0].split(".")[0]; sh=get_shape(obj); sc=get_skin_cluster(sh)
    if not sc: show_status("No skinCluster on selection.",True); return 0
    tj=get_joint_list_from_sc(sc)
    tvi=set()
    for v in vtx_sel: tvi.add(int(v.split("[")[-1].rstrip("]")))
    dl=read_dsw(dn)
    if not dl: return 0
    dj=[simple_obj_name(j) for j in dl[1].split(",")]
    if jm: dj=[jm.get(j,j) for j in dj]
    ei=[s for s,t in enumerate(tj) if t in dj]
    ui=[s for s,t in enumerate(tj) if t not in dj]
    tv=cmds.polyEvaluate(sh,vertex=True); wsf=[0]*tv
    progress_start("Vertex Paste...",len(tvi))
    cmds.setAttr(sc+".normalizeWeights",0); cmds.setAttr(sc+".envelope",0)
    ds=2; cnt=0
    if im==0:
        for i in sorted(tvi):
            progress_update(1,"Paste {0}/{1}".format(cnt+1,len(tvi)))
            li=ds+i
            if li>=len(dl): continue
            ln=dl[li]
            if not ln: continue
            p=ln.split("|")
            pm=_build_wp(tj,ei,ui,dj,p[0],min_w)
            if not pm: continue
            cmds.skinPercent(sc,"{0}.vtx[{1}]".format(sh,i),r=False,transformValue=pm)
            wsf[i]=1; cnt+=1
    elif im in (1,2):
        spa=SpatialIndex(); spa.build_from_shape(sh)
        rf=[1]*tv
        for idx in tvi: rf[idx]=0
        r=ds
        while r<len(dl):
            progress_update(1,"Paste {0}".format(cnt))
            ln=dl[r]
            if not ln: break
            p=ln.split("|"); r+=1
            if im==1:
                xyz=p[1].split(","); pos=(float(xyz[0]),float(xyz[1]),float(xyz[2]))
                mi=spa.find_nearest(pos,"Vtx",rf,acc)
            else:
                uv=p[2].split(","); pos=(float(uv[0]),float(uv[1]))
                mi=spa.find_nearest(pos,"UV",rf,acc)
            if mi==-1: continue
            pm=_build_wp(tj,ei,ui,dj,p[0],min_w)
            if not pm: continue
            cmds.skinPercent(sc,"{0}.vtx[{1}]".format(sh,mi),r=False,transformValue=pm)
            rf[mi]=1; wsf[mi]=1; cnt+=1
    cmds.setAttr(sc+".envelope",1)
    cmds.skinPercent(sc,sh,normalize=True)
    cmds.setAttr(sc+".normalizeWeights",1)
    progress_end()
    cmds.select(vtx_sel,r=True)
    t=time.time()-st
    show_status("Vertex Paste: {0}/{1} vtx  {2:.2f}s".format(cnt, len(tvi), t))
    return 1


# ============================================================================
# Body Fit (BETA) - Fit skeleton A to body B shape
# ============================================================================

# Stores original joint positions for reset
_body_fit_original = {}
_body_fit_dup_root = None

def _is_intermediate_shape(node):
    try: return cmds.getAttr(node + ".intermediateObject")
    except Exception: return False

def _strip_ns(name):
    """Strip namespace: 'NS:joint1' -> 'joint1'"""
    return name.split(":")[-1] if ":" in name else name


def _get_all_joints_from_group(root):
    """Get all joints from skinClusters under root group."""
    def _is_intermediate(n):
        try: return cmds.getAttr(n + ".intermediateObject")
        except Exception: return False

    meshes = cmds.listRelatives(root, allDescendents=True, fullPath=True, type="mesh") or []
    all_joints = set()
    for m in meshes:
        if _is_intermediate(m): continue
        sc = get_skin_cluster(m)
        if sc:
            for j in (cmds.skinCluster(sc, q=True, inf=True) or []):
                lr = cmds.ls(j, long=True)
                if lr: all_joints.add(lr[0])
    return sorted(all_joints)


def _get_all_joints(root):
    """Get all joints under root. Root can be a joint, transform, or group.
    Returns list of long-name joint paths."""
    if not cmds.objExists(root):
        return []
    node_type = cmds.nodeType(root)
    joints = set()
    # If root itself is a joint, include it
    if node_type == "joint":
        lr = cmds.ls(root, long=True)
        if lr: joints.add(lr[0])
    # Get all descendant joints
    descs = cmds.listRelatives(root, allDescendents=True, fullPath=True, type="joint") or []
    for j in descs:
        lr = cmds.ls(j, long=True)
        if lr: joints.add(lr[0])
    return sorted(joints)


def body_fit_joints(src, tgt):
    """Fit A's skeleton to match B's skeleton by joint name.
    Input: root joints or groups containing joints.
    Matched joints are moved to B's position.
    Unmatched joints (e.g. extra swing bones) are skipped.
    Stores originals for reset."""
    global _body_fit_original, _body_fit_dup_root
    _body_fit_dup_root = None
    rpt = Report("Body Fit")
    rpt.log("Source (A): {0}".format(src))
    rpt.log("Target (B): {0}".format(tgt))
    st = time.time()

    if not cmds.objExists(src):
        rpt.error("A not found: " + src); rpt.show_window(); return 0
    if not cmds.objExists(tgt):
        rpt.error("B not found: " + tgt); rpt.show_window(); return 0

    # Get joints from A and B (works with joint roots, groups, or mesh groups)
    a_joints = _get_all_joints(src)
    if not a_joints:
        # Fallback: try skinCluster-based search
        a_joints = _get_all_joints_from_group(src)
    if not a_joints:
        rpt.error("No joints found under A."); rpt.show_window(); return 0

    b_joints = _get_all_joints(tgt)
    if not b_joints:
        b_joints = _get_all_joints_from_group(tgt)
    if not b_joints:
        rpt.error("No joints found under B."); rpt.show_window(); return 0

    rpt.log("A joints: {0}".format(len(a_joints)))
    rpt.log("B joints: {0}".format(len(b_joints)))

    # Read positions
    a_pos = {}
    for j in a_joints:
        try: a_pos[j] = cmds.xform(j, q=True, ws=True, t=True)
        except Exception: pass

    b_pos = {}
    for j in b_joints:
        try: b_pos[j] = cmds.xform(j, q=True, ws=True, t=True)
        except Exception: pass

    # Store originals for reset
    _body_fit_original = {}
    for j, p in a_pos.items():
        _body_fit_original[j] = list(p)

    # Build B lookup by bare name
    b_by_bare = {}
    for j, p in b_pos.items():
        bare = _strip_ns(simple_obj_name(j))
        b_by_bare[bare] = p

    # Match A joints to B by bare name
    matched = {}     # A_joint -> B_position
    unmatched = []
    for j in a_joints:
        a_bare = _strip_ns(simple_obj_name(j))
        if a_bare in b_by_bare:
            matched[j] = b_by_bare[a_bare]
        else:
            unmatched.append(j)

    rpt.log("Matched: {0}  Skipped: {1}".format(len(matched), len(unmatched)))
    if unmatched:
        rpt.log("Skipped joints (no match in B):")
        for u in unmatched[:15]:
            rpt.log("  - {0}".format(_strip_ns(simple_obj_name(u))))
        if len(unmatched) > 15:
            rpt.log("  ... and {0} more".format(len(unmatched) - 15))

    # Disable skinCluster envelopes connected to A's joints
    skin_clusters = set()
    for j in a_joints:
        conns = cmds.listConnections(j, type="skinCluster") or []
        for skc in conns:
            skin_clusters.add(skc)
    env_off = 0
    for skc in skin_clusters:
        try:
            cmds.setAttr(skc + ".envelope", 0)
            env_off += 1
        except Exception:
            pass
    if skin_clusters:
        rpt.log("Envelopes disabled: {0}/{1}".format(env_off, len(skin_clusters)))

    # Move matched A joints to B positions
    progress_start("Fitting joints...", len(matched))
    moved = 0
    failed = 0
    for j in sorted(matched.keys(), key=_jnt_depth):
        progress_update(1)
        new_pos = matched[j]
        try:
            cmds.xform(j, ws=True, t=new_pos)
            actual = cmds.xform(j, q=True, ws=True, t=True)
            dist = sum((actual[a] - new_pos[a])**2 for a in range(3))**0.5
            if dist < 0.5:
                moved += 1
            else:
                failed += 1
        except Exception:
            failed += 1
    progress_end()

    # Re-enable envelopes
    for skc in skin_clusters:
        try: cmds.setAttr(skc + ".envelope", 1)
        except Exception: pass

    elapsed = time.time() - st
    rpt.log("")
    rpt.log("Moved: {0}/{1} matched  Skipped: {2}  Failed: {3}".format(
        moved, len(matched), len(unmatched), failed))
    rpt.log("Time: {0:.2f}s".format(elapsed))
    if moved == 0:
        rpt.error("No joints could be moved.")

    if rpt.errors:
        show_status("Body Fit errors - see report", True)
    else:
        show_status("Body Fit: {0} moved, {1} skipped ({2:.1f}s)".format(
            moved, len(unmatched), elapsed))
    rpt.show_window()
    return 1


def body_fit_reset():
    """Reset skeleton to bind pose using GoToBindPose MEL command."""
    global _body_fit_original, _body_fit_dup_root

    if _body_fit_dup_root and cmds.objExists(_body_fit_dup_root):
        cmds.delete(_body_fit_dup_root)
        _body_fit_dup_root = None

    _body_fit_original = {}

    try:
        mel.eval("GoToBindPose;")
        show_status("GoToBindPose done.")
    except Exception as e:
        show_status("GoToBindPose failed: {0}".format(e), True)
        return 0
    return 1



def _jnt_depth(j):
    d = 0
    p = cmds.listRelatives(j, parent=True, type='joint', fullPath=True)
    while p:
        d += 1; p = cmds.listRelatives(p[0], parent=True, type='joint', fullPath=True)
    return d


# ============================================================================
# Data Check Functions
# ============================================================================

def create_skin_joint_set():
    sl=cmds.filterExpand(sm=12) or []
    if not sl: show_status("No skinned mesh selected",True); return 0
    sh=get_shape(sl[0]); sc=get_skin_cluster(sh)
    if not sc: show_status("No skinCluster",True); return 0
    jl=cmds.listConnections(sc+".matrix",type="joint") or []
    cmds.sets(jl,name="SkinJointSet_"+sl[0])
    show_status("Created SkinJointSet for "+sl[0]); return 1

def check_weight_digit(unit=0.01):
    """Find vertices with weights finer than unit. Bulk-optimized via OpenMaya."""
    max_places = _unit_to_places(unit)
    sl=cmds.filterExpand(sm=12) or []
    if not sl: show_status("No skinned mesh selected",True); return 0
    sh=get_shape(sl[0]); sc=get_skin_cluster(sh)
    if not sc: show_status("No skinCluster",True); return 0
    st=time.time()
    jl=get_joint_list_from_sc(sc)
    vc=cmds.polyEvaluate(sh,vertex=True); sv=[]

    # Bulk fetch weights
    all_weights = _bulk_get_weights(sc, sh, vc, len(jl))
    progress_start("Checking decimals...", vc)
    for i in range(vc):
        if i % 1000 == 0:
            progress_update(min(1000, vc - i), "Check {0}/{1}".format(i, vc))
        if all_weights:
            wl = all_weights[i]
        else:
            wl = cmds.skinPercent(sc, "{0}.vtx[{1}]".format(sh,i), q=True, v=True)
        for w in wl:
            ws = "{0:.10f}".format(w).rstrip("0")
            if "." in ws and len(ws.split(".")[1]) > max_places:
                sv.append("{0}.vtx[{1}]".format(sh,i)); break
    progress_end()
    elapsed = time.time() - st
    if sv:
        cmds.select(sv, r=True)
        show_status("Found {0} vertices finer than {1}".format(len(sv), unit))
    else:
        show_status("Check Pass (unit: {0})".format(unit))
    show_check_result("Weight Decimal Check", len(sv), vc,
                      "Unit: {0}\nTime: {1:.2f}s".format(unit, elapsed))
    return 1


def _unit_to_places(unit):
    """Convert a unit value like 0.01 to number of decimal places (2)."""
    us = "{0:.10f}".format(unit).rstrip("0")
    mp = len(us.split(".")[1]) if "." in us else 0
    return max(mp, 1)


def clean_weight_digit(unit=0.01):
    """Round all skin weights to the specified unit and remove values below it."""
    places = _unit_to_places(unit)
    sl=cmds.filterExpand(sm=12) or []
    if not sl: show_status("No skinned mesh selected",True); return 0
    sh=get_shape(sl[0]); sc=get_skin_cluster(sh)
    if not sc: show_status("No skinCluster",True); return 0
    joints = get_joint_list_from_sc(sc)
    if not joints: show_status("No joints",True); return 0
    st=time.time()
    vc=cmds.polyEvaluate(sh,vertex=True); fixed=0
    progress_start("Cleaning weights...",vc)
    cmds.setAttr(sc+".normalizeWeights",0)
    for i in range(vc):
        progress_update(1,"Clean {0}/{1}".format(i+1,vc))
        vt="{0}.vtx[{1}]".format(sh,i)
        wl=cmds.skinPercent(sc,vt,q=True,v=True)
        new_w = []
        needs_fix = False
        for w in wl:
            rw = round(w, places)
            if rw < unit: rw = 0.0
            if abs(rw - w) > 1e-12: needs_fix = True
            new_w.append(rw)
        if not needs_fix: continue
        total = sum(new_w)
        if total > 0:
            new_w = [w / total for w in new_w]
            new_w = [round(w, places) for w in new_w]
            diff = 1.0 - sum(new_w)
            if abs(diff) > 1e-12:
                max_i = new_w.index(max(new_w))
                new_w[max_i] = round(new_w[max_i] + diff, places)
        else:
            new_w[0] = 1.0
        tv = [(joints[j], new_w[j]) for j in range(min(len(joints), len(new_w)))]
        cmds.skinPercent(sc, vt, r=False, transformValue=tv)
        fixed += 1
    cmds.setAttr(sc+".normalizeWeights",1)
    progress_end()
    elapsed=time.time()-st
    show_status("Cleaned {0}/{1} vertices (unit: {2})".format(fixed, vc, unit))
    cmds.confirmDialog(title="Weight Clean", 
                       message="Cleaned {0} / {1} vertices.\nUnit: {2}\nTime: {3:.2f}s".format(fixed, vc, unit, elapsed),
                       button=["OK"], icon="information")
    return 1


def _quantize_weight_params(params, unit=0.01):
    """Filter and round a transformValue list. Weights below unit become 0, then re-normalize."""
    if not params or unit <= 0: return params
    places = _unit_to_places(unit)
    rounded = []
    for jname, w in params:
        rw = round(w, places)
        if rw < unit: rw = 0.0
        rounded.append((jname, rw))
    total = sum(w for _, w in rounded)
    if total > 0:
        rounded = [(j, round(w / total, places)) for j, w in rounded]
        # Fix rounding drift
        diff = 1.0 - sum(w for _, w in rounded)
        if abs(diff) > 1e-12:
            max_i = max(range(len(rounded)), key=lambda i: rounded[i][1])
            j, w = rounded[max_i]
            rounded[max_i] = (j, round(w + diff, places))
    return rounded

def check_same_position():
    sl=cmds.filterExpand(sm=12) or []
    if not sl: show_status("No skinned mesh selected",True); return 0
    sh=get_shape(sl[0]); sc=get_skin_cluster(sh)
    if not sc: show_status("No skinCluster",True); return 0
    st=time.time()
    cmds.select(cl=True)
    vc=cmds.polyEvaluate(sh,vertex=True); spa=SpatialIndex(); spa.build_from_shape(sh)
    cf=[0]*vc; pv=[]
    progress_start("Checking positions...",vc)
    for i in range(vc):
        progress_update(1,"Check {0}/{1}".format(i+1,vc))
        if cf[i]: continue
        cf[i]=1; pi=spa.vtx_positions[i]; cands=spa.get_cand_vtx(pi)
        vg=["{0}.vtx[{1}]".format(sh,i)]
        wi=",".join([str(w) for w in cmds.skinPercent(sc,vg[0],q=True,v=True)])
        hit=False
        for ci in cands:
            if cf[ci]: continue
            pc=spa.vtx_positions[ci]
            if math.sqrt((pi[0]-pc[0])**2+(pi[1]-pc[1])**2+(pi[2]-pc[2])**2)<0.001:
                cf[ci]=1; vc2="{0}.vtx[{1}]".format(sh,ci); vg.append(vc2)
                wc=",".join([str(w) for w in cmds.skinPercent(sc,vc2,q=True,v=True)])
                if wi!=wc: hit=True
        if hit: pv.extend(vg)
    progress_end()
    elapsed=time.time()-st
    if pv: cmds.select(pv,r=True); show_status("Found {0} problem vertices".format(len(pv)))
    else: show_status("Check Pass - no same-position conflicts")
    show_check_result("Same Position Check", len(pv), vc,
                      "Time: {0:.2f}s".format(elapsed))
    return 1


def check_influence_count(max_inf=4):
    """Find vertices influenced by more than max_inf joints. Bulk-optimized via OpenMaya."""
    sl=cmds.filterExpand(sm=12) or []
    if not sl: show_status("No skinned mesh selected",True); return 0
    sh=get_shape(sl[0]); sc=get_skin_cluster(sh)
    if not sc: show_status("No skinCluster",True); return 0
    st=time.time()
    jl=get_joint_list_from_sc(sc)
    vc=cmds.polyEvaluate(sh,vertex=True); sv=[]

    all_weights = _bulk_get_weights(sc, sh, vc, len(jl))
    progress_start("Checking influences...", vc)
    for i in range(vc):
        if i % 1000 == 0:
            progress_update(min(1000, vc - i), "Check {0}/{1}".format(i, vc))
        if all_weights:
            wl = all_weights[i]
        else:
            wl = cmds.skinPercent(sc, "{0}.vtx[{1}]".format(sh,i), q=True, v=True)
        inf_count = sum(1 for w in wl if abs(w) > 1e-10)
        if inf_count > max_inf:
            sv.append("{0}.vtx[{1}]".format(sh,i))
    progress_end()
    elapsed = time.time() - st
    if sv:
        cmds.select(sv,r=True)
        show_status("Found {0} vertices with >{1} influences".format(len(sv),max_inf))
    else:
        show_status("Check Pass (max {0} influences)".format(max_inf))
    show_check_result("Influence Count Check", len(sv), vc,
                      "Max influences: {0}\nTime: {1:.2f}s".format(max_inf, elapsed))
    return 1


# ============================================================================
# DSW List
# ============================================================================

def get_dsw_list():
    items=[]
    dd=get_dsw_directory()
    if os.path.isdir(dd):
        for f in sorted(os.listdir(dd)):
            if f.lower().endswith(".dsw"): items.append("[File] "+f)
    for o in (cmds.ls("dsw|*") or []): items.append("[Object] "+o)
    return items


# ============================================================================
# GUI
# ============================================================================

class DoraSkinWeightUI(object):
    WIN = "DSWPy_Win"
    JNE_WIN = "DSWPy_JNE"
    HTU_WIN = "DSWPy_HTU"

    def __init__(self):
        self.import_mode = 1  # default: XYZ
        self._jno=[]; self._jnn=[]

    def show(self):
        if cmds.window(self.WIN,exists=True): cmds.deleteUI(self.WIN)
        cmds.window(self.WIN, title=tr("win_title").format(VERSION), wh=(360,560), s=True)
        root=cmds.columnLayout(adj=True)

        # === Header ===
        cmds.rowLayout(nc=4, adj=2, h=30, bgc=(0.22,0.22,0.22),
                       cat=[(1,'left',6),(3,'right',4),(4,'right',6)], cw=[(1,100),(3,80),(4,80)])
        cmds.text(label=tr("lang_label"), fn="smallPlainLabelFont")
        self.lang_menu=cmds.optionMenu(h=22,w=80,cc=self._on_lang)
        cmds.menuItem(label="English"); cmds.menuItem(label="\u65e5\u672c\u8a9e")
        if _LANG=="ja": cmds.optionMenu(self.lang_menu,e=True,sl=2)
        cmds.text(label="")
        cmds.button(label=tr("how_to_use"),h=22,w=80,c=lambda*a:self._htu())
        cmds.setParent(root)

        # === Status bar ===
        cmds.text(_STATUS_CTRL, label="Ready", h=20, al="center", bgc=(0.25,0.25,0.25))

        # === Tabs ===
        self.tabs=cmds.tabLayout("DSWPy_Tabs")

        # ---- Import ----
        ifl=cmds.formLayout()
        il=cmds.text(label=tr("dsw_list"),al="left",h=20)
        self.il=cmds.textScrollList("DSWPy_IL",h=80,sc=self._imp_sel)
        self.inf=cmds.textField("DSWPy_INF",vis=False)
        iml=cmds.text(label=tr("import_mode"),h=20)
        self.irc=cmds.radioCollection()
        r1=cmds.radioButton(label=tr("vertex_order"),h=20,onc=lambda*a:self._sim(0))
        r2=cmds.radioButton(label=tr("xyz_position"),sl=True,h=20,onc=lambda*a:self._sim(1))
        r3=cmds.radioButton(label=tr("uv_position"),h=20,onc=lambda*a:self._sim(2))
        al=cmds.text(label=tr("accuracy"),h=20)
        self.af=cmds.floatField(v=0.001,pre=6,w=80,h=20)
        self.icb=cmds.checkBox(label=tr("interpolate"),v=False,h=20,
                               onc=lambda*a:self._iic(True),ofc=lambda*a:self._iic(False))
        self.iirc=cmds.radioCollection()
        self.ir1=cmds.radioButton(label="XYZ",sl=True,en=False,h=20)
        self.ir2=cmds.radioButton(label="UV",en=False,h=20)
        self.bcb=cmds.checkBox(label=tr("bind_skin"),v=False,h=20)
        bj=cmds.button(label=tr("edit_jointmap"),h=24,w=130,c=lambda*a:self._jne())
        bi=cmds.button(label=tr("import_dsw"),h=28,c=lambda*a:self._do_imp())
        sp=cmds.separator(h=8,st="in")
        bv=cmds.button(label=tr("vtx_paste"),h=28,bgc=(0.4,0.6,0.4),c=lambda*a:self._do_vp())
        cmds.formLayout(ifl,e=True,
            af=[(il,"top",8),(il,"left",4),(il,"right",4),(self.il,"left",4),(self.il,"right",4),
                (iml,"left",4),(r1,"left",4),(r2,"left",4),(r3,"left",4),(al,"left",4),
                (self.icb,"left",4),(self.bcb,"left",4),(bj,"left",4),
                (bi,"left",4),(bi,"right",4),(sp,"left",4),(sp,"right",4),
                (bv,"left",4),(bv,"right",4),(bv,"bottom",4)],
            ac=[(self.il,"top",2,il),(self.il,"bottom",4,iml),
                (iml,"bottom",0,r1),(r1,"bottom",0,r2),(r2,"bottom",0,r3),(r3,"bottom",6,al),
                (al,"bottom",6,self.icb),(self.af,"left",8,al),(self.af,"bottom",6,self.icb),
                (self.icb,"bottom",6,self.bcb),
                (self.ir1,"left",8,self.icb),(self.ir1,"bottom",6,self.bcb),
                (self.ir2,"left",4,self.ir1),(self.ir2,"bottom",6,self.bcb),
                (self.bcb,"bottom",6,bj),(bj,"bottom",6,bi),(bi,"bottom",4,sp),(sp,"bottom",4,bv)])
        cmds.setParent("..")

        # ---- Export ----
        efl=cmds.formLayout()
        el2=cmds.text(label=tr("dsw_list"),al="left",h=20)
        self.el=cmds.textScrollList("DSWPy_EL",h=100,sc=self._exp_sel)
        enl=cmds.text(label=tr("export_dsw_name"),al="left",h=20)
        self.enf=cmds.textField("DSWPy_ENF",h=20,tx="1st")
        bef=cmds.button(label=tr("export_file"),h=28,c=lambda*a:self._do_exp("[File]"))
        beo=cmds.button(label=tr("export_object"),h=28,c=lambda*a:self._do_exp("[Object]"))
        spe=cmds.separator(h=8,st="in")
        bdel=cmds.button(label=tr("delete_dsw"),h=28,bgc=(0.6,0.3,0.3),c=lambda*a:self._do_del())
        cmds.formLayout(efl,e=True,
            af=[(el2,"top",8),(el2,"left",4),(el2,"right",4),
                (self.el,"left",4),(self.el,"right",4),(enl,"left",4),
                (self.enf,"left",4),(self.enf,"right",4),
                (bef,"left",4),(bef,"right",4),(beo,"left",4),(beo,"right",4),
                (spe,"left",4),(spe,"right",4),
                (bdel,"left",4),(bdel,"right",4),(bdel,"bottom",4)],
            ac=[(self.el,"top",2,el2),(self.el,"bottom",4,enl),
                (enl,"bottom",2,self.enf),(self.enf,"bottom",8,bef),
                (bef,"bottom",4,beo),(beo,"bottom",8,spe),(spe,"bottom",4,bdel)])
        cmds.setParent("..")

        # ---- Body Fit (BETA) ----
        btfl=cmds.formLayout()
        btt=cmds.text(label=tr("bf_title"),al="center",h=24,fn="boldLabelFont")
        bsl=cmds.text(label=tr("bf_source"),al="left",h=20)
        self.bsf=cmds.textField(h=24)
        bsb=cmds.button(label=tr("bf_set_selected"),h=24,w=110,c=lambda*a:self._sbt("s"))
        btl=cmds.text(label=tr("bf_target"),al="left",h=20)
        self.btf=cmds.textField(h=24)
        btb=cmds.button(label=tr("bf_set_selected"),h=24,w=110,c=lambda*a:self._sbt("t"))
        bf_sep=cmds.separator(h=8,st="in")
        btn_fit=cmds.button(label=tr("bf_fit"),h=36,bgc=(0.5,0.35,0.6),c=lambda*a:self._do_bf_fit())
        bf_sep2=cmds.separator(h=6,st="in")
        btn_rst=cmds.button(label=tr("bf_reset"),h=30,bgc=(0.55,0.35,0.35),c=lambda*a:self._do_bf_reset())
        bth=cmds.text(label=tr("bf_help"),al="left",h=90,ww=True)
        cmds.formLayout(btfl,e=True,
            af=[(btt,"top",8),(btt,"left",4),(btt,"right",4),(bsl,"left",4),
                (self.bsf,"left",4),(bsb,"right",4),(btl,"left",4),
                (self.btf,"left",4),(btb,"right",4),
                (bf_sep,"left",4),(bf_sep,"right",4),
                (btn_fit,"left",4),(btn_fit,"right",4),
                (bf_sep2,"left",4),(bf_sep2,"right",4),
                (btn_rst,"left",4),(btn_rst,"right",4),
                (bth,"left",8),(bth,"right",8),(bth,"bottom",8)],
            ac=[(bsl,"top",8,btt),(self.bsf,"top",2,bsl),(self.bsf,"right",4,bsb),(bsb,"top",2,bsl),
                (btl,"top",12,self.bsf),(self.btf,"top",2,btl),(self.btf,"right",4,btb),(btb,"top",2,btl),
                (bf_sep,"top",12,self.btf),
                (btn_fit,"top",8,bf_sep),
                (bf_sep2,"top",8,btn_fit),
                (btn_rst,"top",4,bf_sep2),
                (bth,"top",12,btn_rst)])
        cmds.setParent("..")

        # ---- Data Check ----
        cfl=cmds.formLayout()

        # Section 1: Weight Decimal Check
        dt1=cmds.text(label=tr("decimal_title"),al="left",h=18,fn="boldLabelFont")
        dd1=cmds.text(label=tr("decimal_desc"),al="left",h=16,fn="smallPlainLabelFont")
        ctl=cmds.text(label=tr("digit_unit"),h=20)
        self.ctf=cmds.floatField(v=0.01,pre=4,w=70,h=20)
        b_dig=cmds.button(label=tr("check_digit"),h=22,w=70,c=lambda*a:self._do_chk_dig())
        b_cln=cmds.button(label=tr("clean_digit"),h=22,w=100,bgc=(0.4,0.55,0.7),c=lambda*a:self._do_clean_dig())

        sep_c1=cmds.separator(h=10,st="in")

        # Section 2: Influence Count Check
        it1=cmds.text(label=tr("inf_title"),al="left",h=18,fn="boldLabelFont")
        id1=cmds.text(label=tr("inf_desc"),al="left",h=16,fn="smallPlainLabelFont")
        iml=cmds.text(label=tr("inf_max"),h=20)
        self.inf_f=cmds.intField(v=4,min=1,max=20,w=40,h=20)
        b_inf=cmds.button(label=tr("check_inf"),h=22,w=70,c=lambda*a:self._do_chk_inf())

        sep_c2=cmds.separator(h=10,st="in")

        # Section 3: Same Position Check
        b_same=cmds.button(label=tr("check_samepos"),h=28,c=lambda*a:check_same_position())

        sep_c3=cmds.separator(h=10,st="in")

        # Section 4: Create Joint Set
        b_set=cmds.button(label=tr("create_set"),h=28,c=lambda*a:create_skin_joint_set())

        cmds.formLayout(cfl,e=True,
            af=[(dt1,"top",8),(dt1,"left",4),(dt1,"right",4),
                (dd1,"left",4),(dd1,"right",4),
                (ctl,"left",4),(self.ctf,"left",4),
                (b_cln,"right",4),
                (sep_c1,"left",4),(sep_c1,"right",4),
                (it1,"left",4),(it1,"right",4),
                (id1,"left",4),(id1,"right",4),
                (iml,"left",4),
                (sep_c2,"left",4),(sep_c2,"right",4),
                (b_same,"left",4),(b_same,"right",4),
                (sep_c3,"left",4),(sep_c3,"right",4),
                (b_set,"left",4),(b_set,"right",4)],
            ac=[(dd1,"top",2,dt1),
                (ctl,"top",4,dd1),
                (self.ctf,"top",4,dd1),(self.ctf,"left",6,ctl),
                (b_dig,"top",4,dd1),(b_dig,"left",6,self.ctf),
                (b_cln,"top",4,dd1),(b_cln,"left",4,b_dig),
                (sep_c1,"top",8,ctl),
                (it1,"top",8,sep_c1),
                (id1,"top",2,it1),
                (iml,"top",4,id1),
                (self.inf_f,"top",4,id1),(self.inf_f,"left",6,iml),
                (b_inf,"top",4,id1),(b_inf,"left",6,self.inf_f),
                (sep_c2,"top",8,iml),
                (b_same,"top",8,sep_c2),
                (sep_c3,"top",8,b_same),
                (b_set,"top",8,sep_c3)])
        cmds.setParent("..")

        cmds.tabLayout(self.tabs,e=True,
            tabLabel=[(ifl,tr("tab_import")),(efl,tr("tab_export")),
                      (btfl,tr("tab_body_fit")),(cfl,tr("tab_check"))],
            cc=self._rl)
        cmds.setParent("..")
        self._rl()
        cmds.showWindow(self.WIN)
        print("Dora SkinWeight Tools Py v"+VERSION)

    # -- Language --
    def _on_lang(self, v):
        set_language("ja" if v=="\u65e5\u672c\u8a9e" else "en")
        cmds.evalDeferred(self.show)

    # -- How To Use --
    def _htu(self):
        if cmds.window(self.HTU_WIN,exists=True): cmds.deleteUI(self.HTU_WIN)
        cmds.window(self.HTU_WIN,title=tr("htu_title"),wh=(520,500),s=True)
        cmds.columnLayout(adj=True)
        cmds.scrollField(text=tr("htu_content",ver=VERSION),ed=False,ww=True,h=460,fn="fixedWidthFont")
        cmds.showWindow(self.HTU_WIN)

    # -- Lists --
    def _rl(self,*a):
        items=get_dsw_list()
        cmds.textScrollList(self.il,e=True,ra=True)
        cmds.textScrollList(self.el,e=True,ra=True)
        for it in items:
            cmds.textScrollList(self.il,e=True,a=it)
            cmds.textScrollList(self.el,e=True,a=it)
    def _imp_sel(self,*a):
        s=cmds.textScrollList(self.il,q=True,si=True) or []
        if s: cmds.textField(self.inf,e=True,tx=s[0])
    def _exp_sel(self,*a):
        s=cmds.textScrollList(self.el,q=True,si=True) or []
        if s:
            p=s[0].split(" ",1)
            cmds.textField(self.enf,e=True,tx=p[1] if len(p)>1 else p[0])
    def _sim(self,m):
        self.import_mode=m; cmds.floatField(self.af,e=True,en=(m!=0))
    def _iic(self,on):
        cmds.radioButton(self.ir1,e=True,en=on); cmds.radioButton(self.ir2,e=True,en=on)
    def _sbt(self,w):
        s=cmds.ls(sl=True) or []
        if not s: show_status(tr("warn_no_sel"),True); return
        if w=="s": cmds.textField(self.bsf,e=True,tx=s[0])
        else: cmds.textField(self.btf,e=True,tx=s[0])
    def _gjm(self):
        jm=None
        if self._jno and self._jnn:
            jm={o:n for o,n in zip(self._jno,self._jnn) if o!=n}
        return jm if jm else None

    # -- Actions --
    def _do_imp(self):
        dn=cmds.textField(self.inf,q=True,tx=True)
        if not dn: show_status(tr("warn_no_dsw"),True); return
        ip=cmds.checkBox(self.icb,q=True,v=True)
        iim=1 if cmds.radioButton(self.ir1,q=True,sl=True) else 2
        ac=cmds.floatField(self.af,q=True,v=True)
        bs=cmds.checkBox(self.bcb,q=True,v=True)
        mw=cmds.floatField(self.ctf,q=True,v=True) if cmds.floatField(self.ctf,exists=True) else 0.01
        dsw_import(dn,self.import_mode,ip,iim,ac,bs,self._gjm(),min_w=mw,show_report=True); self._rl()

    def _do_exp(self, mode):
        n=cmds.textField(self.enf,q=True,tx=True)
        if not n:
            show_status(tr("warn_no_name"),True); return
        dsw_export("{0} {1}".format(mode,n)); self._rl()

    def _do_del(self):
        s=cmds.textScrollList(self.el,q=True,si=True) or []
        if not s: show_status(tr("warn_no_dsw"),True); return
        r=cmds.confirmDialog(title="Delete DSW", message=tr("warn_delete_confirm").format(s[0]),
                             button=["OK","Cancel"], defaultButton="Cancel", cancelButton="Cancel")
        if r=="OK":
            delete_dsw(s[0]); self._rl()

    def _do_vp(self):
        dn=cmds.textField(self.inf,q=True,tx=True)
        if not dn: show_status(tr("warn_no_dsw"),True); return
        ac=cmds.floatField(self.af,q=True,v=True)
        mw=cmds.floatField(self.ctf,q=True,v=True) if cmds.floatField(self.ctf,exists=True) else 0.01
        vertex_paste_weights(dn,self.import_mode,ac,self._gjm(),min_w=mw)

    def _do_bf_fit(self):
        s=cmds.textField(self.bsf,q=True,tx=True)
        t=cmds.textField(self.btf,q=True,tx=True)
        if not s or not t: show_status(tr("warn_set_both"),True); return
        body_fit_joints(s, t)

    def _do_bf_reset(self):
        body_fit_reset()

    def _do_chk_dig(self):
        u=cmds.floatField(self.ctf,q=True,v=True)
        check_weight_digit(u)

    def _do_clean_dig(self):
        u=cmds.floatField(self.ctf,q=True,v=True)
        clean_weight_digit(u)

    def _do_chk_inf(self):
        n=cmds.intField(self.inf_f,q=True,v=True)
        check_influence_count(n)

    # -- Joint Editor --
    def _jne(self):
        dn=cmds.textField(self.inf,q=True,tx=True)
        if not dn: show_status(tr("warn_no_dsw"),True); return
        dl=read_dsw(dn)
        if not dl: return
        self._jno=[simple_obj_name(j) for j in dl[1].split(",")]
        self._jnn=list(self._jno)
        if cmds.window(self.JNE_WIN,exists=True): cmds.deleteUI(self.JNE_WIN)
        cmds.window(self.JNE_WIN,title=tr("jne_title"),wh=(450,400),s=True)
        mf=cmds.formLayout()
        inf=cmds.text(label="{0} - {1} joints".format(dn,len(self._jno)),h=20)
        self.jl=cmds.textScrollList("DSWPy_JL",h=200,ams=True,sc=self._jne_sel)
        cl=cmds.columnLayout(adj=True,w=160)
        cmds.text(label=tr("jne_joint_name"),h=18); self.jnf=cmds.textField(h=24)
        cmds.button(label=tr("jne_set"),h=24,c=lambda*a:self._jne_sn()); cmds.separator(h=8)
        cmds.text(label=tr("jne_search"),h=18); self.jsf=cmds.textField(h=24)
        cmds.text(label=tr("jne_replace"),h=18); self.jrf=cmds.textField(h=24)
        cmds.button(label=tr("jne_substitution"),h=24,c=lambda*a:self._jne_sub()); cmds.separator(h=8)
        cmds.text(label=tr("jne_prefix"),h=18); self.jpf=cmds.textField(h=24)
        cmds.text(label=tr("jne_suffix"),h=18); self.jxf=cmds.textField(h=24)
        cmds.button(label=tr("jne_add_ps"),h=24,c=lambda*a:self._jne_aps()); cmds.separator(h=8)
        cmds.button(label=tr("jne_reset"),h=24,c=lambda*a:self._jne_rst())
        cmds.setParent("..")
        cmds.formLayout(mf,e=True,
            af=[(inf,"top",8),(inf,"left",4),(self.jl,"left",4),(self.jl,"bottom",4),
                (cl,"right",4),(cl,"top",30)],
            ac=[(self.jl,"top",4,inf),(self.jl,"right",4,cl)])
        self._jne_upd(); cmds.showWindow(self.JNE_WIN)

    def _jne_upd(self):
        cmds.textScrollList(self.jl,e=True,ra=True)
        for o,n in zip(self._jno,self._jnn):
            cmds.textScrollList(self.jl,e=True,a="[{0}] -> [{1}]".format(o,n))
    def _jne_sel(self,*a):
        s=cmds.textScrollList(self.jl,q=True,sii=True) or []
        if s: cmds.textField(self.jnf,e=True,tx=self._jnn[s[0]-1])
    def _jne_sn(self):
        s=cmds.textScrollList(self.jl,q=True,sii=True) or []
        nn=cmds.textField(self.jnf,q=True,tx=True)
        for i in s: self._jnn[i-1]=nn
        self._jne_upd()
    def _jne_sub(self):
        sr=cmds.textField(self.jsf,q=True,tx=True); rp=cmds.textField(self.jrf,q=True,tx=True)
        s=cmds.textScrollList(self.jl,q=True,sii=True) or []
        for i in s: self._jnn[i-1]=self._jnn[i-1].replace(sr,rp)
        self._jne_upd()
    def _jne_aps(self):
        px=cmds.textField(self.jpf,q=True,tx=True); sx=cmds.textField(self.jxf,q=True,tx=True)
        s=cmds.textScrollList(self.jl,q=True,sii=True) or []
        for i in s: self._jnn[i-1]=px+self._jnn[i-1]+sx
        self._jne_upd()
    def _jne_rst(self):
        self._jnn=list(self._jno); self._jne_upd()


# ============================================================================
# Entry Point
# ============================================================================
_ui=None
def launch():
    global _ui; _ui=DoraSkinWeightUI(); _ui.show()
def DoraSkinWeightToolsPy(): launch()
if __name__=="__main__": launch()
