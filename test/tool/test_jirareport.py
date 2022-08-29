
import pytest
import logging
from WeTest.tool import jirareport
from WeTest.util.client import JIRA


@pytest.mark.skip
def test_get_specific_versions_issues(jira: JIRA):

    issues = jirareport.get_issures(jira, "PROJECT", ["1.0.0"])
    logging.info(issues)


@pytest.mark.skip
def test_get_leatest5_versions_issues(jira: JIRA):

    issues = jirareport.get_issures(jira, "PROJECT")
    logging.info(issues)


@pytest.mark.skip
def test_get_module_report(jira: JIRA):

    issues = jirareport.get_issures(jira, "PROJECT")
    report = jirareport.get_module_report("PROJECT", issues)
    logging.info(report)


@pytest.mark.skip
def test_get_priority_report(jira: JIRA):

    issues = jirareport.get_issures(jira, "PROJECT")
    report = jirareport.get_priority_report("PROJECT", issues)
    logging.info(report)


@pytest.mark.skip
def test_get_label_report(jira: JIRA):

    issues = jirareport.get_issures(jira, "PROJECT")
    report = jirareport.get_label_report("PROJECT", issues)
    logging.info(report)


@pytest.mark.skip
def test_get_analytics_report(jira: JIRA):

    issues = jirareport.get_issures(jira, "PROJECT")
    report = jirareport.get_analytics_report("PROJECT", issues)
    logging.info(report)


@pytest.mark.skip
def test_get_annual_issues(jira: JIRA):

    jql = "project = PROJECT AND issuetype = Bug AND created >= 2021-01-01 AND created <= 2021-12-31 order by created DESC"

    # Issue Fields: status, created time, priority, components, labels, stage, reason, env
    fields = "status,created,priority,components,labels,customfield_11200,customfield_11201,environment"
    issues = jira.search_issues(jql, maxResults=1000, fields=fields, expand="changelog")
    issues
    # list(set([issue.fields.environment for issue in issues]))
    # len([issue.fields.environment for issue in issues for env in ("None","test","TEST","Test") if env in str(issue.fields.environment)])