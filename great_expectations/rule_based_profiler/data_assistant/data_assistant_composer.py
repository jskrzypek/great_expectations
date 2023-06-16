from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
    Dict,
    Final,
    List,
    Mapping,
)

from great_expectations.core.metric_domain_types import MetricDomainTypes

if TYPE_CHECKING:
    from great_expectations.core.domain import Domain
    from great_expectations.data_context.data_context.abstract_data_context import (
        AbstractDataContext,
    )
    from great_expectations.datasource.fluent.batch_request import BatchRequest
    from great_expectations.rule_based_profiler.data_assistant.data_assistant_runner import (
        DataAssistantRunner,
    )
    from great_expectations.rule_based_profiler.data_assistant_result import (
        DataAssistantResult,
        DomainBuilderDataAssistantResult,
    )
    from great_expectations.rule_based_profiler.rule import Rule

logger = logging.getLogger(__name__)


class DataAssistantComposer:
    TASK_NAME_TO_JOB_CATEGORY_MAP: Final[Dict[str, str]] = {
        "uniqueness": "column_value_uniqueness",
        "nullity": "column_value_nullity",
        "nonnullity": "column_value_nonnullity",
        "categorical_two": "categorical",
        "categorical_very_few": "categorical",
        "numeric": "numeric",
        "text": "text",
    }

    def __init__(
        self,
        batch_request: BatchRequest,
        data_context: AbstractDataContext,
    ) -> None:
        self._batch_request: BatchRequest = batch_request
        self._data_context: AbstractDataContext = data_context

        self._task_name_to_domain_list_map: Mapping[str, List[Domain]] | None = None

    def build_domains(self) -> None:
        data_assistant = self._data_context.assistants.domains._build_data_assistant()
        rules: List[Rule] = data_assistant.get_rules()

        rule: Rule
        rule_names: List[str] = [rule.name for rule in rules]

        data_assistant_result: DomainBuilderDataAssistantResult = (
            self._data_context.assistants.domains.run(
                batch_request=self._batch_request,
            )
        )

        domains: List[Domain] = list(data_assistant_result.metrics_by_domain.keys())

        rule_name: str
        domain: Domain
        domains_by_rule_name = {
            rule_name: list(
                filter(
                    lambda domain: domain.rule_name == rule_name,
                    domains,
                )
            )
            for rule_name in rule_names
        }

        candidate_table_domains: List[Domain] = domains_by_rule_name[
            "table_domain_rule"
        ]
        if candidate_table_domains:
            logger.info(
                f"""Candidate "{MetricDomainTypes.TABLE}" type "Domain" objects:\n{candidate_table_domains}"""
            )
        candidate_column_value_uniqueness_domains: List[Domain] = domains_by_rule_name[
            "column_value_uniqueness_domain_rule"
        ]
        candidate_column_value_nullity_domains: List[Domain] = domains_by_rule_name[
            "column_value_nullity_domain_rule"
        ]
        candidate_column_value_nonnullity_domains: List[Domain] = domains_by_rule_name[
            "column_value_nonnullity_domain_rule"
        ]
        candidate_numeric_columns_domains: List[Domain] = domains_by_rule_name[
            "numeric_columns_domain_rule"
        ]
        candidate_datetime_columns_domains: List[Domain] = domains_by_rule_name[
            "datetime_columns_domain_rule"
        ]
        candidate_text_columns_domains: List[Domain] = domains_by_rule_name[
            "text_columns_domain_rule"
        ]
        candidate_categorical_columns_domains_zero: List[Domain] = domains_by_rule_name[
            "categorical_columns_domain_rule_zero"
        ]
        candidate_categorical_columns_domains_one: List[Domain] = domains_by_rule_name[
            "categorical_columns_domain_rule_one"
        ]
        candidate_categorical_columns_domains_two: List[Domain] = domains_by_rule_name[
            "categorical_columns_domain_rule_two"
        ]
        candidate_categorical_columns_domains_very_few: List[
            Domain
        ] = domains_by_rule_name["categorical_columns_domain_rule_very_few"]
        candidate_categorical_columns_domains_few: List[Domain] = domains_by_rule_name[
            "categorical_columns_domain_rule_few"
        ]
        if candidate_categorical_columns_domains_few:
            logger.info(
                f"""Candidate "{MetricDomainTypes.COLUMN}" type "categorical_values_few" "Domain" objects:\n{candidate_categorical_columns_domains_few}"""
            )
        candidate_categorical_columns_domains_some: List[Domain] = domains_by_rule_name[
            "categorical_columns_domain_rule_some"
        ]
        if candidate_categorical_columns_domains_some:
            logger.info(
                f"""Candidate "{MetricDomainTypes.COLUMN}" type "categorical_values_some" "Domain" objects:\n{candidate_categorical_columns_domains_some}"""
            )

        numeric_columns_domains: List[Domain] = list(
            filter(
                lambda domain: domain.domain_kwargs["column"]
                not in [
                    domain_key.domain_kwargs["column"]
                    for domain_key in (
                        candidate_column_value_nullity_domains
                        + candidate_categorical_columns_domains_zero
                        + candidate_categorical_columns_domains_one
                        + candidate_categorical_columns_domains_two
                        + candidate_categorical_columns_domains_very_few
                    )
                ],
                candidate_numeric_columns_domains,
            )
        )

        datetime_columns_domains: List[Domain] = list(
            filter(
                lambda domain: domain.domain_kwargs["column"]
                not in [
                    domain_key.domain_kwargs["column"]
                    for domain_key in (
                        candidate_column_value_nullity_domains
                        + candidate_categorical_columns_domains_zero
                        + candidate_categorical_columns_domains_one
                        + candidate_categorical_columns_domains_two
                        + candidate_categorical_columns_domains_very_few
                    )
                ],
                candidate_datetime_columns_domains,
            )
        )
        if datetime_columns_domains:
            logger.info(
                f"""Actual "{MetricDomainTypes.COLUMN}" type "datetime" "Domain" objects:\n{datetime_columns_domains}"""
            )

        text_columns_domains: List[Domain] = list(
            filter(
                lambda domain: domain.domain_kwargs["column"]
                not in [
                    domain_key.domain_kwargs["column"]
                    for domain_key in (
                        candidate_column_value_nullity_domains
                        + candidate_categorical_columns_domains_zero
                        + candidate_categorical_columns_domains_one
                        + candidate_categorical_columns_domains_two
                        + candidate_categorical_columns_domains_very_few
                    )
                ],
                candidate_text_columns_domains,
            )
        )

        categorical_columns_domains_two: List[Domain] = list(
            filter(
                lambda domain: domain.domain_kwargs["column"]
                not in [
                    domain_key.domain_kwargs["column"]
                    for domain_key in (candidate_column_value_nullity_domains)
                ],
                candidate_categorical_columns_domains_two,
            )
        )

        categorical_columns_domains_very_few: List[Domain] = list(
            filter(
                lambda domain: domain.domain_kwargs["column"]
                not in [
                    domain_key.domain_kwargs["column"]
                    for domain_key in (candidate_column_value_nullity_domains)
                ],
                candidate_categorical_columns_domains_very_few,
            )
        )

        column_value_uniqueness_domains: List[Domain] = list(
            filter(
                lambda domain: domain.domain_kwargs["column"]
                not in [
                    domain_key.domain_kwargs["column"]
                    for domain_key in (candidate_column_value_nullity_domains)
                ],
                candidate_column_value_uniqueness_domains,
            )
        )

        column_value_nullity_domains: List[
            Domain
        ] = candidate_column_value_nullity_domains

        column_value_nonnullity_domains: List[
            Domain
        ] = candidate_column_value_nonnullity_domains

        self._task_name_to_domain_list_map = {
            "uniqueness": column_value_uniqueness_domains,
            "nullity": column_value_nullity_domains,
            "nonnullity": column_value_nonnullity_domains,
            "categorical_two": categorical_columns_domains_two,
            "categorical_very_few": categorical_columns_domains_very_few,
            "numeric": numeric_columns_domains,
            "text": text_columns_domains,
        }

    def execute_data_assistant(
        self,
        task_name: str,
    ) -> DataAssistantResult:
        domains: list[Domain] = self._task_name_to_domain_list_map[task_name]

        domains: Domain
        include_column_names = [domain.domain_kwargs["column"] for domain in domains]

        job_category: str = DataAssistantComposer.TASK_NAME_TO_JOB_CATEGORY_MAP[
            task_name
        ]
        data_assistant_runner: DataAssistantRunner = getattr(
            self._data_context.assistants, job_category
        )

        data_assistant_result: DataAssistantResult = data_assistant_runner.run(
            batch_request=self._batch_request,
            include_column_names=include_column_names,
        )

        return data_assistant_result
