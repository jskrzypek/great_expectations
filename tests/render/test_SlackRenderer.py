import pytest

from great_expectations.core import RunIdentifier
from great_expectations.core.batch import BatchDefinition, IDDict
from great_expectations.core.expectation_validation_result import (
    ExpectationSuiteValidationResult,
)
from great_expectations.render.renderer import SlackRenderer

# module level markers
pytestmark = pytest.mark.unit


@pytest.fixture
def failed_expectation_suite_validation_result():
    return ExpectationSuiteValidationResult(
        results=[
            {
                "exception_info": {
                    "raised_exception": False,
                    "exception_traceback": None,
                    "exception_message": None,
                },
                "success": False,
                "meta": {},
                "result": {"observed_value": 8565},
                "expectation_config": {
                    "meta": {},
                    "kwargs": {
                        "column": "my_column",
                        "max_value": 10000,
                        "min_value": 10000,
                        "batch_id": "b9e06d3884bbfb6e3352ced3836c3bc8",
                    },
                    "expectation_type": "expect_column_values_to_be_between",
                },
            }
        ],
        success=False,
        statistics={
            "evaluated_expectations": 0,
            "successful_expectations": 0,
            "unsuccessful_expectations": 0,
            "success_percent": None,
        },
        meta={
            "great_expectations_version": "v0.8.0__develop",
            "batch_kwargs": {"data_asset_name": "x/y/z"},
            "data_asset_name": {
                "datasource": "x",
                "generator": "y",
                "generator_asset": "z",
            },
            "expectation_suite_name": "default",
            "run_id": RunIdentifier(
                run_name="test_100", run_time="2019-09-25T060538.829112Z"
            ),
        },
    )


@pytest.fixture
def success_expectation_suite_validation_result():
    return ExpectationSuiteValidationResult(
        results=[],
        success=True,
        statistics={
            "evaluated_expectations": 0,
            "successful_expectations": 0,
            "unsuccessful_expectations": 0,
            "success_percent": None,
        },
        meta={
            "great_expectations_version": "v0.8.0__develop",
            "batch_kwargs": {"data_asset_name": "x/y/z"},
            "data_asset_name": {
                "datasource": "x",
                "generator": "y",
                "generator_asset": "z",
            },
            "expectation_suite_name": "default",
            "run_id": RunIdentifier(
                run_name="test_100", run_time="2019-09-25T060538.829112Z"
            ),
        },
    )


def test_SlackRenderer_validation_results_with_datadocs(
    success_expectation_suite_validation_result,
):
    validation_result_suite = success_expectation_suite_validation_result

    rendered_output = SlackRenderer().render(
        validation_result=validation_result_suite,
        checkpoint_name="checkpoint_name_testing",
        name="testing",
    )

    expected_output = {
        "blocks": [
            {
                "text": {
                    "text": "testing - checkpoint_name_testing - Success "
                    ":white_check_mark:",
                    "type": "plain_text",
                },
                "type": "header",
            },
            {
                "text": {"text": "Runtime: 2019/09/25 06:05 AM", "type": "plain_text"},
                "type": "section",
            },
            {
                "text": {
                    "text": "*Asset*: x/y/z  *Expectation Suite*: default",
                    "type": "mrkdwn",
                },
                "type": "section",
            },
            {"type": "divider"},
        ]
    }
    print(rendered_output)
    print(expected_output)
    assert rendered_output == expected_output

    data_docs_pages = {"local_site": "file:///localsite/index.html"}
    notify_with = ["local_site"]
    rendered_output = SlackRenderer().render(
        validation_result=validation_result_suite,
        data_docs_pages=data_docs_pages,
        notify_with=notify_with,
        name="hello",
        checkpoint_name="checkpoint_name",
    )

    expected_output = {
        "blocks": [
            {
                "text": {
                    "text": "hello - checkpoint_name - Success " ":white_check_mark:",
                    "type": "plain_text",
                },
                "type": "header",
            },
            {
                "text": {"text": "Runtime: 2019/09/25 06:05 AM", "type": "plain_text"},
                "type": "section",
            },
            {
                "text": {
                    "text": "*Asset*: x/y/z  *Expectation Suite*: default",
                    "type": "mrkdwn",
                },
                "type": "section",
            },
            {
                "text": {
                    "text": "*DataDocs* can be found here: "
                    "`file:///localsite/index.html` \n"
                    " (Please copy and paste link into a browser to "
                    "view)\n",
                    "type": "mrkdwn",
                },
                "type": "section",
            },
            {"type": "divider"},
        ]
    }
    assert rendered_output == expected_output

    # not configured
    notify_with = ["fake_site"]
    rendered_output = SlackRenderer().render(
        validation_result=validation_result_suite,
        data_docs_pages=data_docs_pages,
        notify_with=notify_with,
        name="hello",
        checkpoint_name="checkpoint_name",
    )

    expected_output = {
        "blocks": [
            {
                "text": {
                    "text": "hello - checkpoint_name - Success " ":white_check_mark:",
                    "type": "plain_text",
                },
                "type": "header",
            },
            {
                "text": {"text": "Runtime: 2019/09/25 06:05 AM", "type": "plain_text"},
                "type": "section",
            },
            {
                "text": {
                    "text": "*Asset*: x/y/z  *Expectation Suite*: default",
                    "type": "mrkdwn",
                },
                "type": "section",
            },
            {
                "text": {
                    "text": "*ERROR*: Slack is trying to provide a link to "
                    "the following DataDocs: `fake_site`, but it is "
                    "not configured under `data_docs_sites` in the "
                    "`great_expectations.yml`\n",
                    "type": "mrkdwn",
                },
                "type": "section",
            },
            {"type": "divider"},
        ]
    }

    assert rendered_output == expected_output


def test_SlackRenderer_checkpoint_validation_results_with_datadocs():
    batch_definition = BatchDefinition(
        datasource_name="test_datasource",
        data_connector_name="test_dataconnector",
        data_asset_name="test_data_asset",
        batch_identifiers=IDDict({"id": "my_id"}),
    )
    validation_result_suite = ExpectationSuiteValidationResult(
        results=[],
        success=True,
        statistics={
            "evaluated_expectations": 0,
            "successful_expectations": 0,
            "unsuccessful_expectations": 0,
            "success_percent": None,
        },
        meta={
            "great_expectations_version": "v0.8.0__develop",
            "active_batch_definition": batch_definition,
            "expectation_suite_name": "default",
            "run_id": RunIdentifier(
                run_name="test_100", run_time="2019-09-25T060538.829112Z"
            ),
        },
    )

    rendered_output = SlackRenderer().render(
        validation_result=validation_result_suite,
        name="hello",
        checkpoint_name="testing",
    )

    expected_output = {
        "blocks": [
            {
                "text": {
                    "text": "hello - testing - Success :white_check_mark:",
                    "type": "plain_text",
                },
                "type": "header",
            },
            {
                "text": {"text": "Runtime: 2019/09/25 06:05 AM", "type": "plain_text"},
                "type": "section",
            },
            {
                "text": {
                    "text": "*Asset*: test_data_asset  *Expectation Suite*: " "default",
                    "type": "mrkdwn",
                },
                "type": "section",
            },
            {"type": "divider"},
        ]
    }
    print(rendered_output)
    print(expected_output)
    assert rendered_output == expected_output

    data_docs_pages = {"local_site": "file:///localsite/index.html"}
    notify_with = ["local_site"]
    rendered_output = SlackRenderer().render(
        validation_result=validation_result_suite,
        data_docs_pages=data_docs_pages,
        notify_with=notify_with,
        name="hello",
        checkpoint_name="testing",
    )

    expected_output = {
        "blocks": [
            {
                "text": {
                    "text": "hello - testing - Success :white_check_mark:",
                    "type": "plain_text",
                },
                "type": "header",
            },
            {
                "text": {"text": "Runtime: 2019/09/25 06:05 AM", "type": "plain_text"},
                "type": "section",
            },
            {
                "text": {
                    "text": "*Asset*: test_data_asset  *Expectation Suite*: " "default",
                    "type": "mrkdwn",
                },
                "type": "section",
            },
            {
                "text": {
                    "text": "*DataDocs* can be found here: "
                    "`file:///localsite/index.html` \n"
                    " (Please copy and paste link into a browser to "
                    "view)\n",
                    "type": "mrkdwn",
                },
                "type": "section",
            },
            {"type": "divider"},
        ]
    }
    assert rendered_output == expected_output

    # not configured
    notify_with = ["fake_site"]
    rendered_output = SlackRenderer().render(
        validation_result=validation_result_suite,
        data_docs_pages=data_docs_pages,
        notify_with=notify_with,
        name="hello",
        checkpoint_name="testing",
    )

    expected_output = {
        "blocks": [
            {
                "text": {
                    "text": "hello - testing - Success :white_check_mark:",
                    "type": "plain_text",
                },
                "type": "header",
            },
            {
                "text": {"text": "Runtime: 2019/09/25 06:05 AM", "type": "plain_text"},
                "type": "section",
            },
            {
                "text": {
                    "text": "*Asset*: test_data_asset  *Expectation Suite*: " "default",
                    "type": "mrkdwn",
                },
                "type": "section",
            },
            {
                "text": {
                    "text": "*ERROR*: Slack is trying to provide a link to "
                    "the following DataDocs: `fake_site`, but it is "
                    "not configured under `data_docs_sites` in the "
                    "`great_expectations.yml`\n",
                    "type": "mrkdwn",
                },
                "type": "section",
            },
            {"type": "divider"},
        ]
    }

    assert rendered_output == expected_output


def test_SlackRenderer_get_report_element():
    slack_renderer = SlackRenderer()

    # these should all be caught
    assert slack_renderer._get_report_element(docs_link=None) is None
    assert slack_renderer._get_report_element(docs_link=1) is None
    assert slack_renderer._get_report_element(docs_link=slack_renderer) is None

    # this should work
    assert slack_renderer._get_report_element(docs_link="i_should_work") is not None


def test_SlackRenderer_get_failed_expectation_domain_table():
    slack_renderer = SlackRenderer()
    result = slack_renderer.get_failed_expectation_domain(
        "expect_table_columns_to_be_unique", {}
    )
    assert result == "Table"


def test_SlackRenderer_get_failed_expectation_domain_column_pair():
    slack_renderer = SlackRenderer()
    result = slack_renderer.get_failed_expectation_domain(
        "expect_column_pair_to_be_equal", {"column_A": "first", "column_B": "second"}
    )
    assert result == "first, second"


def test_SlackRenderer_get_failed_expectation_domain_column():
    slack_renderer = SlackRenderer()
    result = slack_renderer.get_failed_expectation_domain(
        "expect_column_pair_to_be_equal", {"column": "first"}
    )
    assert result == "first"


def test_SlackRenderer_get_failed_expectation_domain_column_list():
    slack_renderer = SlackRenderer()
    result = slack_renderer.get_failed_expectation_domain(
        "expect_multicolumn_sum_to_be_equal", {"column_list": ["col_a", "col_b"]}
    )
    assert result == "['col_a', 'col_b']"


def test_SlackRenderer_get_failed_expectation_domain_no_domain():
    slack_renderer = SlackRenderer()
    result = slack_renderer.get_failed_expectation_domain(
        "expect_column_pair_to_be_equal", {"date_column": "kpi_date"}
    )
    assert result is None


def test_create_failed_expectations_text():
    validation_result = [
        {
            "exception_info": {
                "raised_exception": False,
                "exception_traceback": None,
                "exception_message": None,
            },
            "success": False,
            "meta": {},
            "result": {"observed_value": 8565},
            "expectation_config": {
                "meta": {},
                "kwargs": {
                    "max_value": 10000,
                    "min_value": 10000,
                    "batch_id": "b9e06d3884bbfb6e3352ced3836c3bc8",
                },
                "expectation_type": "expect_table_row_count_to_be_between",
            },
        }
    ]
    slack_renderer = SlackRenderer()
    result = slack_renderer.create_failed_expectations_text(validation_result)
    assert (
        result
        == """
*Failed Expectations*:
:x:expect_table_row_count_to_be_between (Table)
"""
    )


def test_slack_renderer_shows_gx_cloud_url(failed_expectation_suite_validation_result):
    slack_renderer = SlackRenderer()
    cloud_url = "app.greatexpectations.io/?validationResultId=123-456-789"
    rendered_msg = slack_renderer.render(
        validation_result=failed_expectation_suite_validation_result,
        show_failed_expectations=True,
        validation_result_urls=[cloud_url],
        name="hello",
        checkpoint_name="testing",
    )

    assert (
        ""
        "<app.greatexpectations.io/?validationResultId=123-456-789|View Results>"
        "" in rendered_msg["blocks"][2]["text"]["text"]
    )
