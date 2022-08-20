import pytz
import threading
from jira import JIRA
from queue import Queue
from datetime import datetime
from collections import Counter


def get_version_issues(jira: JIRA, project: str, version: str, queue: Queue):
    # Note:
    # 1.Jira search only return 50 rows by default
    # 2.Only return fields by needs, retrun all fields will take much more time with low performance

    jql = "project = {project} AND issuetype = Bug AND affectedVersion = '{version}' order by created DESC"
    jql = jql.format(project=project, version=version)

    # Issue fields: status, priority, label, stage, reason
    fields = "status,created,priority,components,labels,customfield_11200,customfield_11201"
    issues = jira.search_issues(jql, maxResults=1000, fields=fields, expand="changelog")

    version_issues = []
    for issue in issues:
        issue_created = issue.fields.created
        issue_status = issue.fields.status.name
        issue_priority = issue.fields.priority.name or "UNKNOWN"
        issue_module = issue.fields.components[0].name if issue.fields.components else "UNKNOWN"
        issue_labels = issue.fields.labels or ["UNKNOWN"]
        issue_stage = issue.fields.customfield_11200.value if issue.fields.customfield_11200 else "UNKNOWN"
        issue_reason = issue.fields.customfield_11201.value if issue.fields.customfield_11201 else "UNKNOWN"

        issue_status_history = [
            "{}: {} -> {}".format(history.created, item.fromString, item.toString)
            for history in issue.changelog.histories
            for item in history.items
            if item.field == "status"
        ]

        issue_isreopened = True if "Reopened" in str(issue_status_history) else False

        format = "%Y-%m-%dT%H:%M:%S.%f%z"
        created_time = datetime.strptime(issue_created, format)
        if issue_status == "CLOSED":
            closed_time = datetime.strptime(issue_status_history[-1].split(": ")[0], format)
            timespan = closed_time - created_time
        else:
            now = datetime.now(pytz.timezone("Asia/Shanghai"))
            timespan = now - created_time

        issue_duration = timespan.days * 24 * 3600 + timespan.seconds

        version_issue = {
            "key": issue.key,
            "module": issue_module,
            "priority": issue_priority,
            "label": issue_labels,
            "stage": issue_stage,
            "reason": issue_reason,
            "status_history": issue_status_history,
            "isreopened": issue_isreopened,
            "duration": issue_duration,
        }

        version_issues.append(version_issue)

    queue.put({version: version_issues})


def get_issures(jira: JIRA, project_name: str, versions: list = None):

    project = jira.project(id=project_name)

    if not versions:
        # Return the latest 5 released versions if versions is None
        versions = [version.name for version in project.versions if version.released == True][-5:]

    threads = []
    queue = Queue()

    project_issues = {}
    project_issues[project_name] = {}

    for version in versions:
        thread = threading.Thread(target=get_version_issues, args=(jira, project, version, queue))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    version_issues = {key: value for item in queue.queue for key, value in item.items()}

    for version in versions:
        project_issues[project_name][version] = version_issues[version]

    return project_issues


def get_report(project_name: str, issues: dict, type: str):
    """Get issue type by type"""

    type = type.lower()
    report = {"project": project_name, "issues": {}}

    report["issues"]["col"] = []
    report["issues"]["data"] = []

    version_data = []
    for project, versions in issues.items():
        for version, issues in versions.items():
            data = {}
            report["issues"]["col"].append(version)

            count = 0
            if type == "label":
                count = dict(Counter([label for issue in issues for label in issue[type]]))
            else:
                count = dict(Counter([issue[type] for issue in issues]))

            data[version] = count
            version_data.append(data)

    items = []
    for datas in version_data:
        for version, data in datas.items():
            for item in data:
                items.append(item)
    items = list(set(items))
    items.sort()

    # For front-end display
    for item in items:
        temp = {"name": item, "value": []}
        for datas in version_data:
            for version, data in datas.items():
                temp["value"].append(data.get(item, 0))
        report["issues"]["data"].append(temp)

    return report


def get_module_report(project_name: str, issues: dict):
    """Get issue module report"""

    report = get_report(project_name, issues, "module")
    return report


def get_priority_report(project_name: str, issues: dict):
    """Get issue proority report"""

    report = get_report(project_name, issues, "priority")
    return report


def get_label_report(project_name: str, issues: dict):
    """Get issue label report"""

    report = get_report(project_name, issues, "label")
    return report


def get_stage_report(project_name: str, issues: dict):
    """Get issue stage report"""

    report = get_report(project_name, issues, "stage")
    return report


def get_reason_report(project_name: str, issues: dict):
    """Get issue reason report"""

    report = get_report(project_name, issues, "reason")
    return report


def get_analytics_report(project_name: str, issues: dict):
    """Get re-active rate and avg duration"""

    report = {"project": project_name, "issues": {}}

    report["issues"]["col"] = []
    report["issues"]["data"] = []

    for project, versions in issues.items():

        reopen_data = {}
        reopen_data["name"] = "reopen_rate"
        reopen_data["value"] = []
        for version, issues in versions.items():
            report["issues"]["col"].append(version)

            reopen_count = len([issue for issue in issues if issue["isreopened"] == True])
            reopen_rate = "{:.4f}".format(reopen_count / len(issues))

            reopen_data["value"].append(reopen_rate)

        report["issues"]["data"].append(reopen_data)

        duration_data = {}
        duration_data["name"] = "duration"
        duration_data["value"] = []
        for version, issues in versions.items():
            duration_total = sum([issue["duration"] for issue in issues]) / 3600  # Hour
            duration_avg = "{:.2f}".format(duration_total / len(issues))
            duration_data["value"].append(duration_avg)

        report["issues"]["data"].append(duration_data)

    return report
